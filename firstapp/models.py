from django.db import models


class TestQuestion(models.Model):
    text = models.TextField()


class Planet(models.Model):
    name = models.CharField(max_length=20)


class Jedi(models.Model):
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    max_number_pupils = models.IntegerField()


class Candidate(models.Model):
    jedi = models.ForeignKey(Jedi, blank=True, null=True,
                             on_delete=models.SET_NULL)
    planet = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    age = models.IntegerField()


class TestAnswer(models.Model):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.BooleanField()


class CandidateAnswer(models.Model):
    test_question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    test_answer = models.ForeignKey(TestAnswer, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
