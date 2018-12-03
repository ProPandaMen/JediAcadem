from django.db.models import Count
from django.shortcuts import render
from .models import TestQuestion
from .models import TestAnswer
from .models import Planet
from .models import CandidateAnswers
from .models import Candidate
from .models import Jedi
from django.conf import settings
from django.core.mail import send_mail


def jedi_from(request):
    filter_name = request.POST.get("name_filter", "")
    filter_age = request.POST.get("age_filter", 0)
    jedi = request.POST.get("selected_jedi")
    jedi_planet = Jedi.objects.get(id=jedi).planet
    list_candidate = Candidate.objects.all().filter(
        name__icontains=filter_name,
        age__gte=filter_age,
        planet=jedi_planet,
        jedi__isnull=True
    )
    return render(request, "djedai.html", {'list_candidate': list_candidate,
                                           'master_jedi': jedi,
                                           'filter_name': filter_name,
                                           'filter_age': filter_age})


def master_jedi_from(request):
    """
    Выводится список джедаев и их учеников.
    Если через фильтр указано мин. кол-во учеников, то выводятся только такие
    джедаи.
    """
    min_pupils = request.POST.get('count', 0)
    all_jedi = Jedi.objects.all()
    list_jedi = Jedi.objects.annotate(Count('candidate')).filter(
        candidate__count__gte=min_pupils
    )
    return render(request, 'master_jedai.html', {'list_jedi': list_jedi,
                                                 'all_jedi': all_jedi,
                                                 'count_filter': min_pupils})


def send_message(request, jedi_id, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    jedi = Jedi.objects.get(id=jedi_id)
    number_of_candidate = Jedi.objects.filter(id=jedi_id).aggregate(
        Count('candidate'))

    if number_of_candidate['candidate__count'] < jedi.max_number_pupils:
        test_list = CandidateAnswers.objects.all()
        number_of_questions = test_list.filter(candidate_id=candidate_id
                                               ).count()
        number_of_answers = test_list.filter(test_answer__is_correct_answer=
                                             True, candidate__id=candidate_id
                                             ).count()
        candidate.jedi = jedi
        candidate.save()
        letter = (
            'Мастер Джедай {0} взял к себе в ученики. Количество правильных '
            'ответов за тест {1} из {2} вопросов. Поздравляю с вступление в '
            'орден и желаем дальнейших успехов'
        ).format(jedi.name, number_of_answers, number_of_questions)
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
    """
    Выводит ответы за тест выбранного кандидата, количество правильных ответов
    и количество вопросов
    """
    test_list = CandidateAnswers.objects.all().filter(candidate=candidate_id)
    candidate = Candidate.objects.get(id__exact=candidate_id)
    number_of_questions = test_list.count()
    number_of_answer = test_list.filter(test_answer__is_correct_answer__exact=
                              True).count()
    return render(request, "watch_test.html", {"test_list": test_list,
                                               "candidate_name":
                                                   candidate.name,
                                               "number_of_answer":
                                                   number_of_answer,
                                               "number_of_questions":
                                                   number_of_questions}
                  )


def test_main(request):
    """
    Выводит перед кандидатов список вопроов с вариантами ответов
    """
    id_candidate = request.POST.get("candidate_id")
    for test_question in TestQuestion.objects.all():
        selected_option = request.POST.get(str(test_question.id))
        test_answer = TestAnswer.objects.get(id=int(selected_option))
        CandidateAnswers.objects.create(test_question=test_question,
                                        test_answer=test_answer,
                                        candidate_id=id_candidate)
    return render(request, "main.html")


def candidate_main(request):
    """
    Выводит на экран 4 поля: планета, email, имя, возраст. После заполнения
    всех пополей и нажатия на кнопку Далее, открывает окно теста, где написанны
    вопросы и к ним варианты ответов.
    """
    if request.method == "POST":
        candidate = Candidate.objects.create(
            planet_id=request.POST.get("planet"),
            email=request.POST.get("email"),
            name=request.POST.get("name"),
            age=request.POST.get("age"),
        )
        test_question = TestQuestion.objects.all()
        test_answer = TestAnswer.objects.all()
        return render(request, "test.html",
                      {"candidate_id": candidate.id, "Questions": test_question,
                       "Answers": test_answer})
    planet = Planet.objects.all()
    return render(request, "candidate.html", {"planet": planet})


def index(request):
    """
    Выводит на экран 2 кнопки: Для Джедаи, Для кандидата.
    """
    return render(request, "main.html")
