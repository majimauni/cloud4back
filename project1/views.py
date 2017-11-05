# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from project1.models import Video, Concurso, Usuario
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from django.core import serializers
from django.http import QueryDict
#from django.conf import settings
#from django.core.files.storage import FileSystemStorage
#from bson import ObjectId
from bson.json_util import dumps
import boto3
#import boto
#from boto.s3.key import Key
#import memcache
import redis
awsregion = "us-west-2"
sqs = boto3.client('sqs',region_name=awsregion)
#mc = memcache.Client(['concursos.0kxuhu.0001.usw2.cache.amazonaws.com:11211'])
#import pylibmc
#mc = pylibmc.Client(["concursos.0kxuhu.cfg.usw2.cache.amazonaws.com:11211"])
#print mc.set('foo','bar')
#print mc.get('foo')
r = redis.StrictRedis(host='concursosinfos-001.0kxuhu.0001.usw2.cache.amazonaws.com', port=6379, db=0)
r.delete('aaaa')
# Create your views here.
#s3 = boto3.client('s3')
#c = boto.connect_s3()
#b = c.get_bucket('smarttoolsg12') # substitute your bucket name here

def index(request):
    return HttpResponse("WELCOME TO SMARTOOLS")


def administrador_new(request):
    context={}
    #return render(request, 'administrador_new.html', context)
    return HttpResponse("PRUEBA")

@csrf_exempt
def administrador_create(request):
    context={}
    return render(request, 'administrador_create.html', context)


def usuarios(request, id=-1):
    metodo = request.method

    if metodo == 'GET':
        # print(request.scheme)
        # print(request.GET.__getitem__('key'))
        # print(id)
        #
        key = request.META['HTTP_TOKEN']
        print key
        try:
            user = Usuario.objects.get(_token=key)
        except (KeyError, Usuario.DoesNotExist):
            return JsonResponse({'error': 'Token invalido'})
        else:
            # print('val')
            try:
                if id > -1:
                    userToGet = [Usuario.objects(id=id)]
                else:
                    userToGet = Usuario.objects.all()
            except (KeyError, Usuario.DoesNotExist):
                return JsonResponse({'error': 'Usuario no existe'})
            else:
                data = serializers.serialize('json', userToGet, fields=('nombres','apellidos','email'))
                return JsonResponse(data, safe=False)


    if metodo == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print body
        user_email = body['email']

        try:
            user = Usuario.objects.get(email=user_email)
        except (KeyError, Usuario.DoesNotExist):
            # save user
            user = Usuario(nombres=body['nombres'], apellidos=body['apellidos'],email=body['email'],_token=body["token"])
            user.save()
            return JsonResponse({'mensaje': 'Usuario guardado'})
        else:
            # return error
            return JsonResponse({'error': 'Ya existe el Usuario'})

    if metodo == 'DELETE':
        # print(QueryDict(request.get_full_path().split("?")[1]).get('key'))
        print(id)
        _sessionToken = QueryDict(request.get_full_path().split("?")[1]).get('key')

        try:
            user = Usuario.objects(_token=_sessionToken).first
        except (KeyError, Usuario.DoesNotExist):
            return JsonResponse({'error': 'Token invalido'})
        else:
            try:
                userToDel = Usuario.objects.get(id=id)
            except (KeyError, Usuario.DoesNotExist):
                return JsonResponse({'error': 'Usuario no existe'})
            else:
                userToDel.delete()
                return JsonResponse({'mensaje':'Usuario Borrado'})


    if metodo == 'PUT':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user_id= body['id']

        try:
            user = Usuario.objects.get(id=user_id)

        except (KeyError, Usuario.DoesNotExist):
            # save user

            return JsonResponse({'mensaje': 'Usuario no encontrado'})
        else:
            # return error
            user = Usuario(**body)
            user.save()
            return JsonResponse({'correcto': ' Usuario modificado'})


def concursos(request, id=-1):
    metodo = request.method

    if metodo == 'GET':
        # print(request.scheme)
        # print(request.GET.__getitem__('key'))
        # print(id)
        key = request.META['HTTP_TOKEN']
        url = request.META['HTTP_URL']
        isurl = request.META['HTTP_ISURL']
        #print key
        #print url
        #print isurl
        if isurl != 'true':
            try:
                usuario = Usuario.objects.get(_token=key)
            except (KeyError, Usuario.DoesNotExist):
                  return JsonResponse({'error1': 'Token invalido'})
            else:
                try:
                    if id > -1:
                        concursoToGet = [Concurso.objects(administraconcu=key)]
                    else:
                        concursoToGet = Concurso.objects(administraconcu=key)
                except (KeyError, Concurso.DoesNotExist):
                        return JsonResponse({'error2': 'Concurso no existe'})
                else:
                    arr = []
                    for conc in concursoToGet:
                        #print "conc"
                        #print conc.nombreconcu
                       # print 'a'
                        concurso = {'id':conc.id,'nombreconcu':conc.nombreconcu, 'imagenurl' :conc.imagenurl, 'imagenconcu':conc.imagenconcu,
                                             'urlconcu':conc.urlconcu,
                                             'feini': conc.feini,
                                             'fefin':conc.fefin,
                                             'premio':conc.premio,
                                             'administraconcu' :conc.administraconcu}

                        print concurso
                        arr.append(concurso)
                    data  = dumps(arr)
                    return HttpResponse(data)


        else:
            try:
                if id > -1:
                    concursoToGet = [Concurso.objects.get(administraconcu=key)]
                else:
                    llave = url
                    concursoToGet = r.get(llave)
                    print dumps(concursoToGet)
		    cache = None
                    if concursoToGet is None:
			cache = 1
                        print "no habia concurso"
                        concursoToGet = Concurso.objects.get(urlconcu=url)
			conc = concursoToGet
			concurso = {'id': conc.id, 'nombreconcu': conc.nombreconcu, 'imagenurl': conc.imagenurl,
                            'imagenconcu': conc.imagenconcu,
                            'urlconcu': conc.urlconcu,
                            'feini': conc.feini,
                            'fefin': conc.fefin,
                            'premio': conc.premio,
                            'administraconcu': conc.administraconcu}
                        print r.set(llave, dumps(concurso))
                        obj = r.get(llave)
                        print dumps(obj)

            except (KeyError, Concurso.DoesNotExist):
                return JsonResponse({'error2': 'Concurso no existe'})
            else:
		if cache is 1:
			print "sin cache"
                	conc = concursoToGet
                	concurso = {'id': conc.id, 'nombreconcu': conc.nombreconcu, 'imagenurl': conc.imagenurl,
                        	    'imagenconcu': conc.imagenconcu,
                            	'urlconcu': conc.urlconcu,
                            	'feini': conc.feini,
                            	'fefin': conc.fefin,
                            	'premio': conc.premio,
                            	'administraconcu': conc.administraconcu}


                	data = dumps(concurso)
                	return HttpResponse(data)
		else:
			print "con cache"
			data = concursoToGet
			return HttpResponse(data)


    if metodo == 'POST' and request.FILES['imagen']:
        print request.POST
        imagenurl = request.POST['imagenurl']
        concurso_url = request.POST['urlconcu']
        #myfile = request.FILES['imagen']
        #fs = FileSystemStorage(location='/media')
        #filename = fs.save(myfile.name, myfile)
        #uploaded_file_url = fs.url(filename)
        #print filename
        #k = Key(b)
        #k.key = 'images/{}'.format(filename)
        #k.set_contents_from_filename(fs.url(filename))
        #s3.Bucket('smarttoolsg12').put_object(Key='images/{}'.format(filename), Body=myfile.)
        #s3.upload_file('..'+fs.url(filename),'smarttoolsg12', 'images/{}'.format(filename))
        #print uploaded_file_url
        data = request.POST
        try:
            concurso_ = [Concurso.objects.get(urlconcu=concurso_url)]
        except (KeyError, Concurso.DoesNotExist):
            # save user
            concurso_ = Concurso(nombreconcu = data['nombreconcu'],imagenurl = imagenurl,imagenconcu = imagenurl,urlconcu = concurso_url,feini = datetime.datetime.strptime(data['feini'], '%d/%m/%Y'),fefin = datetime.datetime.strptime(data['fefin'], '%d/%m/%Y'),premio = data['premio'],administraconcu =data['admin'])
            concurso_.save()
            print "concurso guradado"
            return JsonResponse({'mensaje': 'Concurso guardado'})
        else:
            # return error
            print "ERROR"
            return JsonResponse({'error': 'Ya existe el Concurso'})


    if metodo == 'DELETE':

        key = request.META['HTTP_TOKEN']
        pk = request.META['HTTP_PK']
        print pk

        try:
            usuario = Usuario.objects.get(_token= key)
        except (KeyError, Usuario.DoesNotExist):
            return JsonResponse({'error': 'Usuario invalido'})
        else:
            try:
                if id > -1:
                    concursoToDel = Concurso.objects.get(id=pk)
                else:
                    concursoToDel = Concurso.objects.get(id=pk)

            except (KeyError, Concurso.DoesNotExist):
                return JsonResponse({'error': 'Concurso no existe'})
            else:
                concursoToDel.delete()
                return JsonResponse({'mensaje':'Concurso Borrado'})


    if metodo == 'PUT':
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        concurso_id= data['id']
        print data
        try:
            concurso= Concurso.objects.get(id=concurso_id)

        except (KeyError, Concurso.DoesNotExist):
            # save user

            return JsonResponse({'mensaje': 'Concurso no encontrado'})
        else:
            # return error
            concurso= Concurso.objects.get(pk=concurso_id)
            concurso.nombreconcu = data['nombreconcu']
            concurso.urlconcu = data['urlconcu']
            concurso.feini = datetime.datetime.strptime(data['feini'], '%d/%m/%Y')
            concurso.fefin = datetime.datetime.strptime(data['fefin'], '%d/%m/%Y')
            concurso.premio = data['premio']
            concurso.save()
            return JsonResponse({'correcto': ' Concurso modificado'})

def videos(request, id=-1):
    metodo = request.method

    if metodo == 'GET':
        # print(request.scheme)
        # print(request.GET.__getitem__('key'))
        # print(id)
        key = request.META['HTTP_TOKEN']
        try:
            #válida si el usuario tiene acceso a data
            concurso = Concurso.objects.get(id=key)

        except (KeyError, Usuario.DoesNotExist):

            return JsonResponse({'error1': 'concurso no existe invalido'})
        else:
            # print('val')

            try:
                if id > -1:
                    videoToGet = [Video.objects.get(id=id)]
                else:
                    videoToGet = Video.objects(particoncu=key)

            except (KeyError, Video.DoesNotExist):
                return JsonResponse({'error2': 'Video no existe'})
            else:
                arr = []
                for vide in videoToGet:
                    video = { 'fechasub':vide.fechasub,
                                        'estado':vide.estado,
                                        'videoSubido':vide.videoSubido,
                                        'videoPublicado':vide.videoPublicado,
                                        'descrip': vide.descrip,
                                        'particoncu': vide.particoncu,
                                        'nombreconcursante':vide.nombreconcursante,
                                        'apellidoconcursante':vide.apellidoconcursante,
                                        'emailconcursante':vide.emailconcursante
                    }

                    arr.append(video)
                data = dumps(arr)
                return HttpResponse(data)

    if metodo == 'POST' and request.FILES['video']:

        myfile = request.FILES['video']
        videourl = request.POST['videourl']
        # fs = FileSystemStorage()

        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        # print uploaded_file_url
        #fs = FileSystemStorage(location = '/media')
        #filename = fs.save(myfile.name, myfile)
        #uploaded_file_url = fs.url(filename)
        #print filename
        #s3.upload_file(fs.url(filename), 'smarttoolsg12', 'videosSubidos/{}'.format(filename))
        data = request.POST

        try:
            concurso_ = Concurso.objects.get(pk=data['pk'])
            # video_ = Video(**body)
            #if data['formato'] == 'mp4':
            #    video_ = Video(fechasub=datetime.datetime.strptime(data['fecha'],'%d/%m/%Y'),estado='Convertido',videoSubido=videourl,videoPublicado=videourl,descrip=data['mensaje'],particoncu=concurso_,nombreconcursante=data['nombres'],apellidoconcursante=data['apellidos'],emailconcursante=data['email'])

            #else:
            video_ = Video(fechasub=datetime.datetime.strptime(data['fecha'],'%d/%m/%Y'),estado='Pendiente',videoSubido=videourl,descrip=data['mensaje'],particoncu=data['pk'],nombreconcursante=data['nombres'],apellidoconcursante=data['apellidos'],emailconcursante=data['email'])
            video_.save()
            #data = video_.id.__dict__
            print ('{}'.format(videourl))
            response = sqs.send_message(
                QueueUrl='https://sqs.us-west-2.amazonaws.com/614556672057/videosToConvert.fifo',
                MessageBody='{}'.format(videourl),
                MessageAttributes={
                    'video': { 'StringValue': '{}'.format(videourl),
                               'DataType': 'String'
                    }
                },
                MessageGroupId='videos'
            )
            print response
            return JsonResponse({'mensaje': 'Video guardado'})


        except (KeyError, Concurso.DoesNotExist):
            # save user

            return JsonResponse({'mensaje': 'Video no guardado'})


    if metodo == 'PUT':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        video_id= body['id']

        try:
            video_ = Video.objects.get(id=video_id)

        except (KeyError, Concurso.DoesNotExist):

            return JsonResponse({'mensaje': 'Video no encontrado'})

        else:
            # return error
            video_ = Video(**body)
            video_.save()
            return JsonResponse({'correcto': ' Video modificado'})


    if metodo == 'DELETE':
        # print(QueryDict(request.get_full_path().split("?")[1]).get('key'))
        print(id)
        _sessionToken = QueryDict(request.get_full_path().split("?")[1]).get('key')

        try:
            usuario = Usuario.objects.get(_token=_sessionToken)
        except (KeyError, Usuario.DoesNotExist):
            return JsonResponse({'error': 'Usuario invalido'})
        else:
            try:
                if id > -1:
                    videoToDel = Video.objects.get(id=id)
                else:
                    return JsonResponse({'error': 'Concurso no encontrado'})

            except (KeyError, Video.DoesNotExist):
                return JsonResponse({'error': 'Video no existe'})
            else:
                videoToDel.delete()
                return JsonResponse({'mensaje':'Video Borrado'})
