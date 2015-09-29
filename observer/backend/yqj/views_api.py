# -*- coding: utf-8 -*-
import cPickle
import os
import pytz
from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from django.utils import timezone
from django.db import models, connection, IntegrityError
from django.db.models import Count

from base import authenticate, login_required, set_logo
from base.models import save_user, hash_password, User, Area
from django.conf import settings

def login_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400)

    user = authenticate(username, password)
    if user.is_authenticated():
        response = JsonResponse({'status': True})
        response.set_cookie('pass_id', user.id)
        response.set_cookie('name', user.username)
        print response
        return response
    else:
        print '###'
        return JsonResponse({'status': False})

@api_view(['POST'])
def registe_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400)
    users = User.objects.filter(username=username)
    if users:
        return JsonResponse({'status': False})
    try:
        area = Area.objects.get(name=u'武汉')
        save_user(username, password, area)
    except :
        return JsonResponse({'status': False})

    return JsonResponse ({'status': True})

@login_required
def upload_image(request):
    user = request.myuser
    try:
        f = request.FILES['image']
    except KeyError:
        return HttpResponseRedirect('/settings/')

    media_path = settings.MEDIA_ROOT
    filename = str(user.id) + os.path.splitext(f.name)[1]
    file_list = os.listdir(media_path)
    name_list =  map(lambda x: x.split('.')[0], file_list)

    count = 0
    for i in name_list :
        if i == str(user.id):
            os.remove(media_path + '/' + file_list[count])
        count += 1

    try:
        new_file = open(os.path.join(media_path, filename), 'w')
        for chunk in f.chunks():
            new_file.write(chunk)
    except OSError:
        return HttpResponseRedirect('/settings/')
    finally:
        new_file.close()

    return HttpResponseRedirect('/settings/')

@login_required
def change_passwd(request):
    user = request.myuser
    try:
        old_passwd = request.POST['oldPassword']
        new_passwd = request.POST['newPassword']
        username = request.POST['username']
    except KeyError:
        return HttpResponse(status=400)
    if username != user.username:
        return JsonResponse({'status': False})

    coded = hash_password(old_passwd, user.salt)
    #authencate success
    if user.password == coded:
        user.password = hash_password(new_passwd, user.salt)
        user.save(using='master')
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})

@login_required
def reset_passwd(request):
    try:
        reseted_user_ids = request.POST['id'].split(',')
        reseted_id_list = map(lambda x: int(x), reseted_user_ids)
    except (KeyError, ValueError):
        return HttpResponse(status=400)

    admin_user = request.myuser
    group_users = admin_user.group.user_set.all()
    group_user_ids = list(map(lambda x: x.id, group_users))

    for user_id in reseted_id_list:
        if user_id in group_user_ids:
            user = User.objects.get(id=user_id)
            user.password = hash_password('123456', user.salt)
            user.save(using='master')
    return JsonResponse({'status': True})

@login_required
def delete_user_view(request):
    try:
        reseted_user_ids = request.POST['id'].split(',')
        reseted_id_list = map(lambda x: int(x), reseted_user_ids)
    except (KeyError, ValueError):
        return HttpResponse(status=400)

    admin_user = request.myuser
    group_users = admin_user.group.user_set.all()
    group_user_ids = list(map(lambda x: x.id, group_users))

    for user_id in reseted_id_list:
        if user_id in group_user_ids and user_id != admin_user.id:
            delete_user = User.objects.get(id=user_id)
            delete_user.delete(using='master')
    return JsonResponse({'status': True})

@login_required
def add_user_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400)

    myuser = request.myuser
    if not myuser.isAdmin:
        return HttpResponse(status=401)

    if User.objects.filter(username=username):
        return JsonResponse({'status': False})
    else:
        save_user(username, password, myuser.area, myuser.group)
        return JsonResponse({'status': True})

def get_count_feeling(start_d, end_d, feeling_type):
    feeling_limit = ''
    if feeling_type == 'positive':
        feeling_limit = 'feeling_factor >= 0.9'
    elif feeling_type == 'negative':
        feeling_limit = 'feeling_factor <= 0.1 and feeling_factor >= 0'
    else:
        feeling_limit = 'feeling_factor > 0.1  and feeling_factor < 0.9 or feeling_factor = -1'
    with connection.cursor() as c:
        sql_str = "SELECT Date(pubtime), COUNT(*) FROM article where Date(pubtime) >= '{0}' and Date(pubtime) < '{1}' and {2} group by Date(pubtime)".format(start_d, end_d, feeling_limit)
        c.execute(sql_str)
        rows = c.fetchall()

        d =  dict(rows)
        a = [i[0] for i in rows]
        result = []
        day = start_d
        while day < end_d:
            num = d[day] if day in d else 0
            result.append(num)
            day = day + timedelta(days=1)
        return result

@login_required
def chart_line_index_view(request):
    today = timezone.now()
    today = today.astimezone(pytz.utc).date()
    start_d = today - timedelta(days=6)
    end_d = today + timedelta(days=1)

    data = {}
    data['date'] = [(today - timedelta(days=x)).strftime("%m-%d") for x in reversed(range(7))]
    data['positive'] = get_count_feeling(start_d, end_d, 'positive')
    data['neutral'] = get_count_feeling(start_d, end_d, 'netrual')
    data['negative'] = get_count_feeling(start_d, end_d, 'negative')

    return JsonResponse(data)

@login_required
def chart_pie_index_view(request):
    area = request.myuser.area
    locations = Area.objects.filter(parent=area)
    name = [item.name for item in locations]
    values = []
    for item in locations:
        values.append({'name': item.name, 'value': item.article_set.all().count()})
        #values.append({'name': item.name, 'value': 80})
    values = [item for item in values if item['value']]
    return JsonResponse({'name': name, "value": values})

def map_view(request):
    data = cPickle.load(file(os.path.join(settings.BASE_DIR, "yqj/jobs/minutely/map.json"), "r"))
    risk_data = data["regionData"]
    return JsonResponse({"regionData": risk_data })