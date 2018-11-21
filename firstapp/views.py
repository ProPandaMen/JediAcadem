from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import TestQuestion
from .models import TestAnswer
from .models import Planet
from .models import CandidateAnswer
from .models import Candidate
from .models import Jedi
from django.conf import settings
from django.core.mail import send_mail


def jedi_filter(request):
    jedi = request.POST.get("IdMasterDjedai")
    jedi_planet = Jedi.objects.get(id=jedi).planet.name
    master_jedi = Jedi.objects.get(id=jedi)
    list_candidate = Candidate.objects.all()
    filter_age = request.POST.get("count")
    filter_name = request.POST.get("NameFilter")
    if not filter_age:
        filter_age = 0
    elif not filter_name:
        filter_name = ""
    return render(request, "djedai.html", {'list_candidate': list_candidate,
                                           'jedi_planet': jedi_planet,
                                           'master_jedi': master_jedi,
                                           "spis": jedi,
                                           "FilterAge": int(filter_age),
                                           "FilterName": str(filter_name)})


def master_jedi_filter(request):
    min_pupils = request.POST.get("count")
    if not min_pupils:
        min_pupils = 0
    for_jedi = Jedi.objects.all()
    for_candidate = Candidate.objects.all()
    list_jedi = []
    for jedi in for_jedi:
        i = 0
        for candidate in for_candidate:
            if candidate.jedi == jedi:
                i = i + 1
                if int(min_pupils) <= i:
                    list_jedi.append(jedi)
    list_pupils = Candidate.objects.all()
    jedi_select = for_jedi
    if int(min_pupils) <= 0:
        list_jedi = for_jedi
    return render(request, "master_jedai.html", {"list_jedi": list_jedi,
                                                 "list_pupils": list_pupils,
                                                 "jedi_select": jedi_select,
                                                 "count_filter": min_pupils})


def send_message(request, name, id):
    list_pupils = Candidate.objects.all()
    persons = Candidate.objects.get(id=id)
    jedi = Jedi.objects.get(id=name)
    number_of_students = 0
    for pupils in list_pupils:
        if jedi == pupils.jedi:
            number_of_students += 1

    if number_of_students < jedi.max_number_pupils:
        test_list = CandidateAnswer.objects.all()
        answer = 0
        question = 0
        for test in test_list:
            if test.candidate_answer.id == id:
                question += 1
                if test.test_answer.correct_answer:
                    answer += 1
        persons.jedi = jedi
        persons.save()
        letter = (
            'Мастер Джедай {0} взял к себе в ученики. Количество правильных '
            'ответов за тест {1} из {2} вопросов. Поздравляю с вступление в '
            'орден и желаем дальнейших успехов'
        ).format(jedi.name, answer, question)
        send_mail('Вы приняты в орден', letter, settings.EMAIL_HOST_USER,
                  [persons.email])
        return render(request, "info.html", {
            "text": "{0}, взял в падаваны {1}".format(jedi.name,
                                                      persons.name)})
    else:
        return render(request, "info.html", {
            "text": "У вас максимум учеников".format(jedi.name,
                                                     persons.name)})


def watch_test(request, id):
    test_list = CandidateAnswer.objects.all()
    candidate_name = Candidate.objects.get(id=id)
    answer = 0
    question = 0
    for test in test_list:
        if test.candidate_answer.id == id:
            question += 1
            if test.test_answer.correct_answer:
                answer += 1
    return render(request, "watch_test.html", {"test_list": test_list,
                                               "id": id,
                                               "name": candidate_name.name,
                                               "answer": answer,
                                               "question": question})


def master_jedi_main(request):
    if request.method == "POST":
        jedi = request.POST.get("selected_jedi")
        jedi_planet = Jedi.objects.get(id=jedi).planet.name
        master_jedi = Jedi.objects.get(id=jedi)
        list_candidate = Candidate.objects.all()
        return render(
            request, "djedai.html", {'list_candidate': list_candidate,
                                     'jedi_planet': jedi_planet,
                                     'master_jedi': master_jedi,
                                     "spis": jedi, "FilterAge": 0,
                                     "FilterName": ""})
    list_jedi = Jedi.objects.all()
    list_pupils = Candidate.objects.all()
    return render(request, "master_jedai.html", {"list_jedi": list_jedi,
                                                 "list_pupils": list_pupils,
                                                 "jedi_select": list_jedi})


def test_main(request):
    if request.method == "POST":
        name_candidate = request.POST.get("name")
        for test_question in TestQuestion.objects.all():
            selected_option = request.POST.get(str(test_question.id))
            test_answer = TestAnswer.objects.get(id=int(selected_option))
            CandidateAnswer.objects.create(
                test_question=test_question, test_answer=test_answer,
                candidate_answer=name_candidate)
        return render(request, "main.html")


def candidate_main(request):
    if request.method == "POST":
        candidate = Candidate()
        candidate.planet = request.POST.get("planet")
        candidate.email = request.POST.get("email")
        candidate.name = request.POST.get("name")
        candidate.age = request.POST.get("age")
        candidate.save()
        test_question = TestQuestion.objects.all()
        test_answer = TestAnswer.objects.all()
        return render(request, "test.html",
                      {"player": candidate.id, "Question": test_question,
                       "Answer": test_answer})
    planet = Planet.objects.all()
    return render(request, "candidate.html", {"planet": planet})


def index(request):
    return render(request, "main.html")
