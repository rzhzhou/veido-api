from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.db import models
from yqj.models import (Article, Area, Weixin, Topic, RealtedData)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
#from api.serializers import ArticleSerializer,NotificationSerializer,InsightSerializer,EventSerializer,NewsSerializer,InspectionSerializer
from general.decorators import login_required
from django.db.models import Q
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.db.models import get_model
from rest_framework.views import APIView
from django.db.models import Count
import datetime

# Create your views here.

@api_view(['GET'])
def article_view(request, id, **kwargs):
    try:
        article_id = int(id)
        article = Article.objects.get(id=article_id)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ArticleSerializer(article)
    return Response(serializer.data)
