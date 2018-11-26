from django.shortcuts import render
from .models import TestQuestion
from .models import TestAnswer
from .models import Planet
from .models import CandidateAnswer
from .models import Candidate
from .models import Jedi
from django.conf import settings
from django.core.mail import send_mail


def jedi_from(request):
    filter_name = request.POST.get("name_filter")
    filter_age = request.POST.get("age_filter")
    jedi = request.POST.get("selected_jedi")
    if not filter_name:
        filter_name = ""
    if not filter_age:
        filter_age = 0
    jedi_planet = Jedi.objects.get(id=jedi).planet.name
    list_candidate = Candidate.objects.all().filter(
        name__icontains=filter_name,
        age__gte=filter_age,
        planet__icontains=jedi_planet,
        jedi__exact=None
    )
    return render(request, "djedai.html", {'list_candidate': list_candidate,
                                           'master_jedi': jedi,
                                           'FilterName': filter_name,
                                           'FilterAge': filter_age})


def master_jedi_from(request):
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
    if int(min_pupils) <= 0:
        list_jedi = for_jedi
    return render(request, "master_jedai.html", {"list_jedi": list_jedi,
                                                 "list_pupils": list_pupils,
                                                 "jedi_select": for_jedi,
                                                 "count_filter": min_pupils})


def send_message(request, jedi_id, candidate_id):
    list_pupils = Candidate.objects.all()
    candidate = Candidate.objects.get(id=candidate_id)
    jedi = Jedi.objects.get(id=jedi_id)
    number_of_students = 0
    for pupils in list_pupils:
        if jedi == pupils.jedi:
            number_of_students += 1

    if number_of_students < jedi.max_number_pupils:
        test_list = CandidateAnswer.objects.all()
        question = test_list.count()
        answer = test_list.filter(test_answer__correct_answer__exact=
                                  True).count()
        candidate.jedi = jedi
        candidate.save()
        letter = (
            'Мастер Джедай {0} взял к себе в ученики. Количество правильных '
            'ответов за тест {1} из {2} вопросов. Поздравляю с вступление в '
            'орден и желаем дальнейших успехов'
        ).format(jedi.name, answer, question)
        send_mail('Вы приняты в орден', letter, settings.EMAIL_HOST_USER,
                  [candidate.email])
        return render(request, "info.html", {
            "text": "{0}, взял в падаваны: {1}".format(jedi.name,
                                                       candidate.name)})
    else:
        return render(request, "info.html", {
            "text": "У вас максимум учеников".format(jedi.name,
                                                     candidate.name)})


def watch_test(request, candidate_id):
    test_list = CandidateAnswer.objects.all().filter(candidate=candidate_id)
    candidate_name = Candidate.objects.get(id__exact=candidate_id)
    question = test_list.count()
    answer = test_list.filter(test_answer__correct_answer__exact=True).count()
    return render(request, "watch_test.html", {"test_list": test_list,
                                               "id": candidate_id,
                                               "name": candidate_name.name,
                                               "answer": answer,
                                               "question": question})


def test_main(request):
    if request.method == "POST":
        name_candidate = request.POST.get("name")
        id_candidate = Candidate.objects.get(id=name_candidate)
        for test_question in TestQuestion.objects.all():
            selected_option = request.POST.get(str(test_question.id))
            test_answer = TestAnswer.objects.get(id=int(selected_option))
            CandidateAnswer.objects.create(
                test_question=test_question, test_answer=test_answer,
                candidate=id_candidate)
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
                      {"player": candidate.id, "Questions": test_question,
                       "Answers": test_answer})
    planet = Planet.objects.all()
    return render(request, "candidate.html", {"planet": planet})


def index(request):
    return render(request, "main.html")
