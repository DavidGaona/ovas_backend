from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import Score, Ova, Subject, UserSubject, OvaUser


@csrf_exempt
def score_create(request):
    import json
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = OvaUser.objects.get(id=body['user_id'])
        ova = Ova.objects.get(id=body['ova_id'])
        score_update = body['value']

        if score_update > 5:
            score_update = 5
        elif score_update < 0:
            score_update = 0

        score_existe_filter = Score.objects.filter(user_id=usuario, ova_id=ova)
        se_creo = False
        if score_existe_filter:
            score_existe = Score.objects.get(user_id=usuario, ova_id=ova)
            score_existe.score = score_update
            score_existe.save()
        else:
            score = Score(user_id=usuario, ova_id=ova, score=score_update)
            score.save()
            se_creo = True
        json_response_default = {"payload": []}

        if se_creo or score_existe_filter:
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


@csrf_exempt
def user_create(request):
    import json
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = OvaUser(first_name=body['first_name'], last_name=body['last_name'], email=body['email'],
                          cedula=body['cedula'], is_active=True)
        usuario.set_password(body['password'])
        usuario.save()

        json_response_default = {"payload": []}

        if usuario.id:
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


@csrf_exempt
def update_password(request):
    import json
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        json_response_default = {"payload": []}

        usuario = OvaUser.objects.get(id=body['id'])

        if usuario.check_password(body['old_password']):
            usuario.set_password(body['password'])
            usuario.save()
            if usuario.id:
                respuesta = {"payload": 'Actualizado'}
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
            respuesta = {"payload": score_ova['score__avg']}
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

        user_subject_existe = UserSubject.objects.filter(user_id=usuario, subject_id=subject)
        se_creo = False
        if not user_subject_existe:
            user_subject = UserSubject(user_id=usuario, ova_id=subject)
            user_subject.save()
            se_creo = True

        json_response_default = {"payload": []}

        if se_creo or user_subject_existe:
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


def get_score_user_ova(request, user, ova):
    import json

    try:
        json_response_default = {"payload": []}
        score = Score.objects.filter(user_id_id=user, ova_id_id=ova).values()

        if list(score):
            respuesta = {"payload": list(score)}
            json_response = json.dumps(respuesta)
            response = HttpResponse(json_response, content_type='application/json', status=200)
            return response
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=404)
        return response
    except:
        json_response_default = {"payload": []}
        response = HttpResponse(json.dumps(json_response_default), content_type='application/json', status=500)
        return response


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk
        })