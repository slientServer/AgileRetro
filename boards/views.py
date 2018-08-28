# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import Board, Topic, Post, Entity, Category
from accounts.models import User
from django.http import Http404
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
from django.views.generic import UpdateView, ListView, CreateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View

# Create your views here.

class BoardListView(ListView):
  model = Board
  context_object_name = 'boards'
  template_name = 'home.html'

class TopicListView(ListView):
  model = Topic
  context_object_name = 'topics'
  template_name = 'topics.html'
  paginate_by = 10

  def get_context_data(self, **kwargs):
    kwargs['board'] = self.board
    try:
      if self.request.user.is_authenticated:
        kwargs['categorys'] = Category.objects.all().filter(entity=(User.objects.all().filter(username=self.request.user))[0].entity)
    except 'BaseException':
        kwargs['categorys'] = []
    kwargs['selected_category'] = int(self.kwargs.get('category'), 10)
    return super().get_context_data(**kwargs)

  def get_queryset(self):
    self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
    try:
      if self.request.user.is_authenticated:
        queryset = self.board.topics.annotate(comments = Count('posts', filter = Q(posts__post_type = 'post')), 
              stars = Count('posts', filter = Q(posts__post_type = 'star')), total = Count('posts'), star_len = Count('posts', filter = Q(posts__post_type = 'star', posts__created_by = self.request.user))).order_by('-total')
      else:
        queryset = self.board.topics.annotate(comments = Count('posts', filter = Q(posts__post_type = 'post')), 
          stars = Count('posts', filter = Q(posts__post_type = 'star')), star_len = Count('posts', filter = Q(posts__post_type = 'star'))).order_by('-last_updated')

    except 'BaseException':
      queryset = self.board.topics.annotate(comments = Count('posts', filter = Q(posts__post_type = 'post')), 
            stars = Count('posts', filter = Q(posts__post_type = 'star')), star_len = Count('posts', filter = Q(posts__post_type = 'star'))).order_by('-last_updated')
    if self.kwargs.get('category') != '9999':
      queryset = queryset.filter(category=self.kwargs.get('category'))
    return queryset

@login_required
def new_topic(request, pk):
  board=get_object_or_404(Board, pk=pk)
  user = request.user
  if request.method=='POST':
    form=NewTopicForm(request.POST, user=user)
    if form.is_valid():
      topic=form.save(commit=False)
      topic.board=board
      topic.starter=user
      topic.save()
      # post=Post.objects.create(
      #   message=form.cleaned_data.get('message'),
      #   topic=topic,
      #   created_by= user
      # )
      return redirect('board_topics', pk=pk, category=9999)
  else:
    form=NewTopicForm(user=user)
  return render(request, 'new_topic.html', {'board': board, 'form': form})

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at').filter(post_type = 'post')
        return queryset

@login_required
def star_topic(request, pk, topic_pk, category):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    stars = Post.objects.filter(post_type = 'star', created_by = request.user, topic = topic)
    if request.method == 'GET' and len(stars) == 0:
        Post(post_type = 'star', created_by = request.user, topic = topic).save()
    return redirect('board_topics', pk=pk, category=category)

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now()
            topic.save()
            return redirect('board_topics', pk=pk, category=9999)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

