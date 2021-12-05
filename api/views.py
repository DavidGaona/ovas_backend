from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse, request

from ovas_backend.api.models import Score, Ova


def score_create(request, pk, pk_ova):
    score = Score(user_id=pk, ova_id=pk_ova)
    score.save()
    return HttpResponse({"status": 200}, content_type='application/json')


def get_ova_score(request, pk):
    from django.db.models import Avg
    score_ova = Score.objects.filter(ova_id=pk).aggregate(Avg('score'))
    return HttpResponse({"status": 200, "payload": score_ova}, content_type='application/json')


def get_ova(request, pk):
    ova = Ova.objects.filter(id=pk)
    return HttpResponse({"status": 200, "payload": ova}, content_type='application/json')
