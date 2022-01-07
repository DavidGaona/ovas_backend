from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse, request
from django.views.decorators.csrf import csrf_exempt

from .models import Score, Ova, Subject, UserSubject, OvaUser


@csrf_exempt
def score_create(request):
    import json
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = OvaUser.objects.get(id=body['user_id'])
        ova = Ova.objects.get(id=body['ova_id'])

        score_existe = Score.objects.get(user_id=usuario, ova_id=ova)
        se_creo = False
        if score_existe.id:
            score_existe.score = body['value']
            score_existe.save()
        else:
            score = Score(user_id=usuario, ova_id=ova, score=body['value'])
            score.save()
            se_creo = True
        json_response_default = {"payload": []}

        if se_creo or score_existe.id:
            respuesta = {"payload": 'Creado'}
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
        subjects = Subject.objects.filter(name__icontains=subject).values('id')

        lista_ids = [item['id'] for item in subjects]

        ova = Ova.objects.filter(subject__in=lista_ids, active=True).\
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


def get_subject(request, pk):
    import json

    try:
        subject = Subject.objects.filter(id=pk)
        json_response_default = {"payload": []}

        if len(list(subject)):
            respuesta = {"payload": list(subject)}
            json_response = json.dumps(respuesta)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response


def get_subjects(request):
    import json

    try:
        subject = Subject.objects.filter()
        json_response_default = {"payload": []}

        if len(list(subject)):
            respuesta = {"payload": list(subject)}
            json_response = json.dumps(respuesta)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response


def get_user_subject_user(request, user):
    import json

    try:
        user_subjects = UserSubject.objects.filter(user_id=user)
        json_response_default = {"payload": []}

        if len(list(user_subjects)):
            respuesta = {"payload": list(user_subjects)}
            json_response = json.dumps(respuesta)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response


def get_user_subject_subject(request, subject):
    import json

    try:
        user_subjects = UserSubject.objects.filter(subject_id=subject)
        json_response_default = {"payload": []}

        if len(list(user_subjects)):
            respuesta = {"payload": list(user_subjects)}
            json_response = json.dumps(respuesta)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response


def assign_subject_to_user(request):
    import json

    try:

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = OvaUser.objects.get(id=body['user_id'])
        subject = Subject.objects.get(id=body['subject_id'])

        user_subject_existe = UserSubject.objects.get(user_id=usuario, subject_id=subject)
        se_creo = False
        if not user_subject_existe.id:
            user_subject = UserSubject(user_id=usuario, ova_id=subject)
            user_subject.save()
            se_creo = True

        json_response_default = {"payload": []}

        if se_creo or user_subject_existe.id:
            respuesta = {"payload": 'Creado'}
            json_response = json.dumps(respuesta)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response


def unassign_subject_to_user(request, user, subject_id):
    import json

    try:

        usuario = OvaUser.objects.get(id=user)
        subject = Subject.objects.get(id=subject_id)

        user_subject_existe = UserSubject.objects.get(user_id=usuario, subject_id=subject)
        existe = user_subject_existe.id
        if existe:
            user_subject_existe.delete()

        json_response_default = {"payload": []}

        if existe:
            respuesta = {"payload": 'Desasignado'}
            json_response = json.dumps(respuesta)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response

        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response