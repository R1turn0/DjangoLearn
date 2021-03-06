from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpRequest, HttpResponse, Http404
from polls.models import Question   # 其实就是从数据库中载入表


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    '''
    order by polls_question 表中的 pub_date(publish date) 对表中的前
    五个数据进行切片并排序
    
    传递的元组对象的正负决定数据排序的正序倒序
    '''
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')
    #
    # return render(request, 'polls/detail.html', {'question': question})
    # 利用django内置的shortcut库来防止视图层和模型层的耦合
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', context={'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
