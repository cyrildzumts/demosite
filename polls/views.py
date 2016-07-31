from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
# Create your views here.


class IndexView(generic.ListView):
    page_title = "Polls Home Page"
    template_name = "polls/index.html"
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # query the last 5 questions
        return Question.objects.order_by('pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# Polls Home Page
def index(request):
    page_title = "Polls Home Page"
    template_name = "polls/index.html"
    # query the last 5 questions
    latest_question_list = Question.objects.order_by('pub_date')
    output = ', '.join([q.question_text for q in latest_question_list])
    context = {'page_title': page_title,
               'latest_question_list': latest_question_list,
               'output': output
               }
    return render(request, template_name, context)


# polls questions
@login_required
def results(request, pk):
    question = get_object_or_404(Question, pk=pk)
    template_name = "polls/results.html"
    return render(request, template_name, {'question': question})


@login_required
def vote(request, pk):
    question = get_object_or_404(Question, pk=int(pk))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Vous n'avez pas fait de choix.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',
                                    args=(question.id,)))


def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    template_name = 'polls/detail.html'
    page_title = "Question %s" % question.id
    context = {'question': question, 'page_title': page_title}
    return render(request, template_name, context)
