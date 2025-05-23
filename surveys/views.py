from django.shortcuts import render, get_object_or_404, redirect
from users.models import UserProfile
from .models import Survey, Question, Option, Answer
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import csv
from django.http import HttpResponse
from django.core.mail import send_mail

def send_survey_notification(user, survey):
    subject = f"So‘rovnoma to‘ldirildi: {survey.title}"
    message = f"{user.username} foydalanuvchi {survey.title} so‘rovnomasini to‘ldirdi."
    admin_email = 'admin@example.com'

    send_mail(subject, message, EMAIL_HOST_USER, [admin_email])



def export_survey_csv(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    questions = survey.question_set.all()
    answers = Answer.objects.filter(question__survey=survey)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{survey.title}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Foydalanuvchi', 'Savol', 'Javob'])

    for answer in answers:
        if answer.text_answer:
            result = answer.text_answer
        elif answer.rating:
            result = answer.rating
        elif answer.selected_option:
            result = answer.selected_option.text
        else:
            result = ''
        writer.writerow([answer.user.username, answer.question.text, result])

    return response


def home(request):
    if request.user.is_authenticated:
        profile = request.user.userprofile
        surveys = Survey.objects.filter(target_roles=profile.role)
    else:
        surveys = Survey.objects.none()
    return render(request, 'surveys/home.html', {'surveys': surveys})


def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    questions = survey.question_set.all()

    # ❗ Faqat 1 marta to‘ldirish cheklovi
    already_answered = Answer.objects.filter(user=request.user, question__survey=survey).exists()
    if already_answered:
        return render(request, 'surveys/already_answered.html', {'survey': survey})

    if request.method == 'POST':
        for question in questions:
            key = f"question_{question.id}"
            answer = Answer(user=request.user, question=question)

            if question.question_type == 'text':
                answer.text_answer = request.POST.get(key)
            elif question.question_type == 'rating':
                answer.rating = int(request.POST.get(key))
            else:
                answer.selected_option_id = request.POST.get(key)

            answer.save()
        return redirect('thank_you')

    return render(request, 'surveys/survey_detail.html', {'survey': survey, 'questions': questions})

def thank_you(request):
    return render(request, 'surveys/thank_you.html')


def survey_stats(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    questions = survey.question_set.all()
    data = []

    for q in questions:
        options = q.option_set.annotate(count=Count('answer'))
        data.append({
            'question': q,
            'options': options
        })

    return render(request, 'surveys/stats.html', {'survey': survey, 'data': data})