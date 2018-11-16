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


def SendMessage(request, name, id):
    persons = Candidate.objects.get(id=id)
    jedi = Jedi.objects.get(id=name)
    persons.jedi = jedi
    persons.save()
    letter = ('Мастер Джедай {0} взял к себе в ученики. Количество баллов за '
              'тест. Поздравляю с вступление в орден и желаем дальнейших '
              'успехов').format(jedi.name)
    send_mail('Вы приняты в орден', letter, settings.EMAIL_HOST_USER,
              [persons.email])
    return HttpResponseNotFound(
        "<h2>{0}, взял в падаваны {1}</h2>".format(jedi.name, persons.name))

def Watchtest(request, id):
    test_list = CandidateAnswer.objects.all()
    candidate_name = Candidate.objects.get(id=id)
    return render(request, "watctest.html", {"test_list": test_list, "id": id,
                                             "name": candidate_name.name})

def MasterJediMain(request):
    if request.method == "POST":
        jedi = request.POST.get("selected_jedi")
        jedi_planet = Jedi.objects.get(id=jedi).planet.name
        master_jedi = Jedi.objects.get(id=jedi)
        list_candidate = Candidate.objects.all()
        return render(
            request, "djedai.html", {'list_candidate': list_candidate,
                                     'jedi_planet': jedi_planet,
                                     'master_jedi': master_jedi})
    list_jedi = Jedi.objects.all()
    return render(request, "masterdjedai.html", {"list_jedi": list_jedi})


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





