from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import Person
from .models import candidat
from .models import Planet
from .models import djedai
from .models import test
from django.conf import settings
from django.core.mail import send_mail


def djedaif(request):
    djed = request.POST.get("IdMasterDjedai")
    listdjed = djedai.objects.get(id=djed).planet.name
    master = djedai.objects.get(id=djed)
    people = candidat.objects.all()
    filterf = request.POST.get("count")
    FilterName = request.POST.get("NameFilter")
    if not filterf:
        filterf = 0
    elif not FilterName:
        FilterName = ""
    return render(request, "djedai.html", {"spis": djed, "people": people, 'djedd': listdjed,
                                           'master': master, "FilterAge": int(filterf), "FilterName": str(FilterName)})


def masterdjedaif(request):
    if request.method == "POST":
        filterf = request.POST.get("count")
        djeda = djedai.objects.all()
        return render(request, "masterdjedai.html", {"djedai": djeda, "filter": int(filterf)})


def masterdjedai(request):
    if request.method == "POST":
        djed = request.POST.get("djedais")
        listdjed = djedai.objects.get(id=djed).planet.name
        master = djedai.objects.get(id=djed)
        people = candidat.objects.all()
        return render(request, "djedai.html", {"spis": djed, "people": people, 'djedd': listdjed,
                                               'master': master, "FilterAge": 0, "FilterName": ""})
    djeda = djedai.objects.all()
    return render(request, "masterdjedai.html", {"djedai": djeda, "filter": 0})


def watchtest(request, id):
    try:
        opentest = test.objects.all()
        return render(request, "watctest.html", {"test": opentest, "people": candidat.objects.get(id=id)})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Ошибка</h2>")


def tests(request):
    if request.method == "POST":
        nameplayer = request.POST.get("name")
        listtest = candidat.objects.get(id=int(nameplayer))
        listtest.AnswersTest = ""
        i = 0
        for qtest in test.objects.all():
            vartest = request.POST.get(str(qtest.id))
            listtest.AnswersTest += vartest + " "
            listtest.save()
            if vartest in str(qtest.CorrectAnswer):
                i = i + 1
        if i < 1:
            candidattest = candidat.objects.get(id=int(nameplayer))
            candidattest.delete()
        else:
            candidattest = candidat.objects.get(id=int(nameplayer))
            candidattest.NumberPoints = i
            candidattest.save()
        return render(request, "index.html")


def candidate(request):
    if request.method == "POST":
        tom = candidat()
        tom.planet = request.POST.get("planet")
        tom.email = request.POST.get("email")
        tom.name = request.POST.get("name")
        tom.age = request.POST.get("age")
        tom.AnswerTrue = 0
        tom.save()
        starttest = test.objects.all()
        return render(request, "test.html", {"test": starttest, "player": tom.id})
    planet = Planet.objects.all()
    return render(request, "candidate.html", {"planet": planet})


def djedais(request):
    people = candidat.objects.all()
    return render(request, "djedai.html", {"people": people})


# получение данных из бд
def index(request):
    people = Person.objects.all()
    return render(request, "index.html", {"people": people})


def send(request, master, id):
    persons = candidat.objects.get(id=id)
    padavadjed = djedai.objects.get(name=master)
    padavadjed.NumberPadawans += 1
    padavadjed.save()
    letter = 'Мастер Джедай {0} взял к себе в ученики. Количество баллов за тест {1}. ' \
                 'Поздравляю с вступление в орден и желаем дальнейших успехов'\
            .format(master, test)
    send_mail('Вы приняты в орден', letter, settings.EMAIL_HOST_USER, [persons.email])
    candidattest = candidat.objects.get(id=id)
    candidattest.delete()
    return HttpResponseNotFound("<h2>{0}, взял в падаваны {1}</h2>".format(master, persons.name))


#def delete(request, email):
    #try:
        #person = candidat.objects.get(email=email)
        #send_mail('Тестовое сообщение', 'Все работает', settings.EMAIL_HOST_USER, ['Stalker74369@yandex.ru'])
        #return HttpResponseNotFound("<h2>{}</>".format(person))
    #except Person.DoesNotExist:
        #return HttpResponseNotFound("<h2>Person not found</>")




