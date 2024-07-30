from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import json
from .models import Question, Choice, Thought

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class ThoughtView(generic.ListView):
    template_name = 'polls/thoughts.html'
    context_object_name = 'latest_thought_list'
    
    def get_queryset(self):
        return Thought.objects.order_by()

def ThinkView(request):
    return render(request, 'polls/think.html')

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def think(request):
    t = Thought(title=request.POST.get('title'), thought_text=request.POST.get('thought_text'))
    t.save()
    return HttpResponseRedirect(reverse('polls:thoughts'))