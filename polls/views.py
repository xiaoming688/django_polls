from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponseRedirect
from django.views import generic

from .models import Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
        # latest_question_list = Question.objects.order_by('-pub_date')[:5]
        # context = {'latest_question_list': latest_question_list}
        # return render(request, 'polls/index.html', context)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        print 'vote', request.POST
        selected_choice = p.choice_set.get(pk=request.POST["choice"])
    except:
        return render(request, 'polls/detail.html', {'question': p, 'error_message': 'You did not select a choice'})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
