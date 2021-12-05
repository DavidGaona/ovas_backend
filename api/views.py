from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse, request
from .models import Score, Ova


def score_create(request, pk, pk_ova):
    import json
    try:
        score = Score(user_id=pk, ova_id=pk_ova)
        score.save()
        json_response_default = {"payload": []}

        if score.id:
            respuesta = {"payload": list('Creado')}
            json_response = json.dumps(respuesta)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response


def get_ova_score(request, pk):
    import json
    from django.db.models import Avg
    try:
        score_ova = Score.objects.filter(ova_id=pk).aggregate(Avg('score'))
        json_response_default = {"payload": []}

        if len(list(score_ova)):
            respuesta = {"payload": list(score_ova)}
            json_response = json.dumps(respuesta)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response


def get_ova(request, pk):
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    try:
        ova = Ova.objects.filter(id=pk).values('id', 'contributor', 'coverage', 'creator', 'date', 'description',
                                               'format', 'language', 'publisher', 'relation', 'rights',
                                               'source', 'subject', 'title', 'type', 'uploader', 'link')

        json_response_default = {"payload": []}
        if len(list(ova)):
            respuesta = {"payload": list(ova)}
            json_response = json.dumps(respuesta, cls=DjangoJSONEncoder)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response


def get_list_ova_per_subject(request, subject):
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    try:
        ova = Ova.objects.filter(subject__icontains=subject, active=True).\
            values('id', 'creator', 'date', 'description', 'format',
                   'language', 'subject', 'title', 'uploader', 'link')

        json_response_default = {"payload": []}
        if len(list(ova)):
            respuesta = {"payload": list(ova)}
            json_response = json.dumps(respuesta, cls=DjangoJSONEncoder)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response


def get_list_ova_per_title(request, title):
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    try:
        ova = Ova.objects.filter(title__icontains=title, active=True).\
            values('id', 'creator', 'date', 'description', 'format',
                   'language', 'subject', 'title', 'uploader', 'link')

        json_response_default = {"payload": []}
        if len(list(ova)):
            respuesta = {"payload": list(ova)}
            json_response = json.dumps(respuesta, cls=DjangoJSONEncoder)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response


def get_list_ova(request):
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    try:
        ova = Ova.objects.filter(active=True).\
            values('id', 'creator', 'date', 'description', 'format',
                   'language', 'subject', 'title', 'uploader', 'link')

        json_response_default = {"payload": []}
        if len(list(ova)):
            respuesta = {"payload": list(ova)}
            json_response = json.dumps(respuesta, cls=DjangoJSONEncoder)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response