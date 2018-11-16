from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import TestQuestion
from .models import TestAnswer
from .models import Planet
from .models import CandidateAnswer
from .models import Candidate
from .models import Jedi
from django.conf import settings
from django.core.mail import send_mail


def JedaiF(request):
    djed = request.POST.get("IdMasterDjedai")
    jedi_planet = Jedi.objects.get(id=djed).planet.name
    master_jedi = Jedi.objects.get(id=djed)
    list_candidate = Candidate.objects.all()
    filterf = request.POST.get("count")
    FilterName = request.POST.get("NameFilter")
    if not filterf:
        filterf = 0
    elif not FilterName:
        FilterName = ""
    return render(request, "djedai.html", {'list_candidate': list_candidate,
                                           'jedi_planet': jedi_planet,
                                           'master_jedi': master_jedi,
                                           "spis": djed,
                                           "FilterAge": int(filterf),
                                           "FilterName": str(FilterName)})


def MasterdJediF(request):
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
    return render(request, "masterdjedai.html", {"list_jedi": list_jedi,
                                                 "list_pupils": list_pupils,
                                                 "jedi_select": jedi_select,
                                                 "count_filter": min_pupils})


def SendMessage(request, name, id):
    list_pupils = Candidate.objects.all()
    persons = Candidate.objects.get(id=id)
    jedi = Jedi.objects.get(id=name)
    cound_pupils = 0
    for pupils in list_pupils:
        if jedi == pupils.jedi:
            cound_pupils += 1

    if cound_pupils < jedi.max_number_pupils:
        test_list = CandidateAnswer.objects.all()
        answer = 0
        Question = 0
        for test in test_list:
            if test.candidate_answer.id == id:
                Question += 1
                if test.test_answer.correct_answer:
                    answer += 1
        persons.jedi = jedi
        persons.save()
        letter = (
            'Мастер Джедай {0} взял к себе в ученики. Количество правильных '
            'ответов за тест {1} из {2} вопросов. Поздравляю с вступление в '
            'орден и желаем дальнейших успехов').format(jedi.name, answer,
                                                        Question)
        send_mail('Вы приняты в орден', letter, settings.EMAIL_HOST_USER,
                  [persons.email])
        return HttpResponseNotFound("<h2>{0}, взял в падаваны {1}</h2>".
                                    format(jedi.name, persons.name))
    else:
        return HttpResponseNotFound(
            "<h2>У вас максимум учеников</h2>")


def Watchtest(request, id):
    test_list = CandidateAnswer.objects.all()
    candidate_name = Candidate.objects.get(id=id)
    answer = 0
    Question = 0
    for test in test_list:
        if test.candidate_answer.id == id:
            Question += 1
            if test.test_answer.correct_answer:
                answer += 1
    return render(request, "watctest.html", {"test_list": test_list, "id": id,
                                             "name": candidate_name.name,
                                             "answer": answer,
                                             "question": Question})


def MasterJediMain(request):
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
    return render(request, "masterdjedai.html", {"list_jedi": list_jedi,
                                                 "list_pupils": list_pupils,
                                                 "jedi_select": list_jedi})


def TestMain(request):
    if request.method == "POST":
        nameplayer = request.POST.get("name")
        candidat = Candidate.objects.get(id=int(nameplayer))
        for qtest in TestQuestion.objects.all():
            vartest = request.POST.get(str(qtest.id))
            atest = TestAnswer.objects.get(id=int(vartest))
            CandidateAnswer.objects.create(
                test_question=qtest, test_answer=atest,
                candidate_answer=candidat)
        return render(request, "Main.html")


def CandidateMain(request):
    if request.method == "POST":
        candidat = Candidate()
        candidat.planet = request.POST.get("planet")
        candidat.email = request.POST.get("email")
        candidat.name = request.POST.get("name")
        candidat.age = request.POST.get("age")
        candidat.save()
        test_question = TestQuestion.objects.all()
        test_answer = TestAnswer.objects.all()
        return render(request, "Test.html",
                      {"player": candidat.id, "Question": test_question,
                       "Answer": test_answer})
    planet = Planet.objects.all()
    return render(request, "Candidate.html", {"planet": planet})


def index(request):
    return render(request, "Main.html")





