from django.db import models


class test(models.Model):
    Question = models.TextField()
    Answer = models.TextField()
    CorrectAnswer = models.TextField()


class Planet(models.Model):
    name = models.CharField(max_length=20)


class candidat(models.Model):
    planet = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    NumberPoints = models.IntegerField()
    AnswersTest = models.TextField()


class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()


class djedai(models.Model):
    name = models.CharField(max_length=50)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    NumberPadawans = models.IntegerField()
    MaxNumberPadawans = models.IntegerField()
