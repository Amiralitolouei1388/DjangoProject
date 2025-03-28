from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Topic,Entry
from .forms import TopicForm,EntryForm

# Create your views here.
def index(request):
    return render(request, "learning_logs/index.html")

def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request,'learning_logs/topics.html', context)

from django.shortcuts import render, get_object_or_404

def topic(request, slug):
    topic = Topic.objects.get(slug=slug)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id, slug):
    topic = Topic.objects.get(slug=slug)
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=(topic.id,)))
    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html',context)
