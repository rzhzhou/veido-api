from itertools import chain
from django.contrib.auth.models import User, Group

from datetime import date, timedelta, datetime
from django.core.exceptions import ObjectDoesNotExist

from observer.base.service.abstract import Abstract

class UserData(Abstract):  # 获取系统用户

    def __init__(self, user):
        self.user = user

    def get_all(self):
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_active')

        if self.user.is_active:
            group_ids = Group.objects.filter(user=self.user).values_list('id', flat=True)

            # 如果当前操作的是'超级管理员'
            if 2 in group_ids:
                queryset = User.objects.exclude(id=self.user.id).values(*fields)
            # 如果当前操作的是'管理员'
            elif 3 in group_ids:
                group_list = list(group_ids)
                group_list.remove(3)
                queryset = User.objects.filter(groups__in=group_list).exclude(id=self.user.id).values(*fields)
            # 如果当前操作的是普通用户
            else:
                queryset = User.objects.filter(username=self.user).exclude(id=self.user.id).values(*fields)

            return queryset

        else:
            return 202


class UserAdd(Abstract):  # 添加用户

    def __init__(self, user, params={}):
        super(UserAdd, self).__init__(params)
        self.user = user

    def add_user(self):
        username = getattr(self, 'username')
        password = getattr(self, 'password')
        re_password = getattr(self, 're_password')
        last_name = getattr(self, 'last_name', '')
        first_name = getattr(self, 'first_name', '')
        email = getattr(self, 'email', '')
        group_name = getattr(self, 'group_name', '')

        if password != re_password:
            return 201

        if len(password) < 8:
            return 202

        if not self.user.is_active:
            return 203

        if not self.user.is_superuser:
            return 204

        group_names = Group.objects.filter(user=self.user).values_list('name', flat=True)

        # 如果当前操作的是'超级管理员'
        if '超级管理员' in group_names:
            try:
                User.objects.get(username=username)
                return 205
            except ObjectDoesNotExist:
                user = User(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    is_staff=False,
                    is_active=True,
                    is_superuser=True,
                    last_login=datetime.now(),
                    date_joined=datetime.now(),
                )
                user.set_password(password)
                user.save()
                if not Group.objects.filter(name=group_name).exists():
                    group = Group(name=group_name)
                    group.save()
                    user.groups.add(group)
                else:
                    group = Group.objects.get(name=group_name)
                    user.groups.add(group)
                user.groups.add(Group.objects.filter(name='管理员')[0])
                return 200
            except Exception as e:
                print(e)
                return 206
        # 如果当前操作的是'管理员'
        elif '管理员' in group_names:
            group_list = list(group_names)
            group_list.remove('管理员')
            try:
                User.objects.get(username=username)
                return 205
            except ObjectDoesNotExist:
                user = User(
                    username=str(self.user)+'@'+str(username),
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    is_staff=False,
                    is_active=True,
                    is_superuser=False,
                    last_login=datetime.now(),
                    date_joined=datetime.now(),
                )
                user.set_password(password)
                user.save()

                group = Group.objects.get(name=group_list[0])
                user.groups.add(group)
                return 200
            except Exception as e:
                print(e)
                return 206


class UserEdit(Abstract):  # 修改用户

    def __init__(self, user, params={}):
        super(UserEdit, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_id = cid
        old_password = getattr(self, 'old_password', None)
        new_password = getattr(self, 'new_password', None)
        re_password = getattr(self, 're_password', None)

        user = User.objects.get(id=edit_id)

        if not old_password or not new_password or not re_password:
            return 201

        if not user.check_password(old_password):
            return 202

        if new_password != re_password:
            return 203

        user.set_password(new_password)
        user.save()

        return 200

class UserDelete(Abstract): # 删除用户

    def __init__(self, user):
        self.user = user

    def delete(self, cid):
        del_ids = cid

        for id in del_ids.split(","):
            user = User.objects.get(id=id)

            if user == self.user:
                return 201

            user.delete()

        return 200