from django.shortcuts import render
from rest_framework.views import APIView


class TableAPIView(APIView):
    def __init__(self, request=None):
        self.request = request


class LineTableView(TableAPIView):
    def get(self, request ):
        pass


class PieTypeTableView(TableAPIView):
    def get(self, request):
        pass


class PieFeelingTableView(TableAPIView):
    def get(self, request):
        pass


class PieAreaTableView(TableAPIView):
    def get(self, request):
        pass

