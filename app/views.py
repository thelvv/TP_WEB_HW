from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Question, Answer


def index(request):
    questions = Question.objects.new_questions()
    questions = paginate(request, questions)
    return render(request, 'index.html', {
        'questions': questions,
        'page_obj': questions
    })


"""
def index(request, pk):
    question = Question.objects.filter(identificator=pk)
    {{question.model.rate_up()}}
    questions = Question.objects.new_questions()
    questions = paginate(request, questions)

    return render(request, 'index.html', {
        'questions': questions,
        'page_obj': questions
    })
"""


def hot_questions(request):
    questions = Question.objects.hot_questions()
    questions = paginate(request, questions)
    return render(request, 'hot_questions.html', {
        'questions': questions,
        'page_obj': questions
    })


def question(request, pk):
    question = Question.objects.filter(identificator=pk).first()
    answers = Answer.objects.filter(question=question)
    answers = paginate(request, answers)
    return render(request, 'question_page.html', {
        'question': question,
        'answers': answers,
        'page_obj': answers
    })


def ask(request):
    return render(request, 'ask.html', {})


def tag(request, tag):
    questions_ = Question.objects.questions_by_tag(tag)
    questions = paginate(request, questions_)
    return render(request, 'tag.html', {
        'questions': questions_,
        'page_obj': questions
    })


def settings(request):
    return render(request, 'settings.html', {})


def login(request):
    return render(request, 'login.html', {})


def register(request):
    return render(request, 'register.html', {})


def paginate(request, objects_list, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
