# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mongoengine import *
# Create your models here.
class Usuario(Document):
	nombres = StringField(max_length=50)
	apellidos = StringField(max_length=20)
	email = EmailField(max_length=50)
	_token = StringField(max_length=50,primary_key=True)



class Concurso(Document):
	nombreconcu = StringField(max_length=100)
	imagenurl = StringField(max_length=100)
	imagenconcu = StringField(max_length=200)
	urlconcu =StringField(max_length=100)
	feini =DateTimeField()
	fefin =DateTimeField()
	premio = StringField(max_length=200)
	administraconcu= StringField(max_length=200)



class Video(Document):
	fechasub = DateTimeField()
	estado = StringField(max_length=50)
	videoSubido =StringField(max_length=200)
	videoPublicado =StringField(max_length=200)
	descrip = StringField(max_length=200)
	particoncu = StringField(max_length=200)
	nombreconcursante= StringField(max_length=50)
	apellidoconcursante= StringField(max_length=50)
	emailconcursante= EmailField(max_length=50)
