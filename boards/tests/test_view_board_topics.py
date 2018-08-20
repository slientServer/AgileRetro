from django.test import TestCase, Client
from django.urls import reverse, resolve
from ..views import BoardListView, TopicListView, PostListView
from ..models import Board, User, Topic, Post
# Create your tests here.

class BoardTopicsTests(TestCase):
  """docstring for BoardTopicsTests"""
  def setUp(self):
    Board.objects.create(name='Djiango', description='Djiango board')
    # User.objects.create_user(username='john', email='john@doe.com', password='old_password')  
    # self.client.login(username='john', password='old_password')

  def test_board_topics_view_success_status_code(self):
    url=reverse('board_topics', kwargs={'pk': Board.objects.first().id})
    response=Client().get(url)
    self.assertEquals(response.status_code, 200)

  def test_board_topic_view_not_found_status_code(self):
    url=reverse('board_topics', kwargs={'pk': 99})
    response=Client().get(url)
    self.assertEquals(response.status_code, 404)

  def test_board_topics_url_resolves_board_topics_view(self):
    view=resolve('/boards/1/')
    self.assertEquals(view.func.view_class, TopicListView)

  def test_board_topics_view_contains_link_back_to_homepage(self):
    board_topics_url = reverse('board_topics', kwargs={'pk': Board.objects.first().id})
    response = self.client.get(board_topics_url)
    homepage_url = reverse('home')
    self.assertContains(response, 'href="{0}"'.format(homepage_url))

  def test_board_topics_view_contains_navigation_links(self):
    board_topics_url = reverse('board_topics', kwargs={'pk': Board.objects.first().id})
    homepage_url = reverse('home')
    new_topic_url = reverse('new_topic', kwargs={'pk': Board.objects.first().id})
    response = Client().get(board_topics_url)
    self.assertContains(response, 'href="{0}"'.format(homepage_url))
    self.assertContains(response, 'href="{0}"'.format(new_topic_url))

class TopicPostsTests(TestCase):
  def setUp(self):
      board = Board.objects.create(name='Django', description='Django board.')
      user = User.objects.create_user(username='john', email='john@doe.com', password='123')
      topic = Topic.objects.create(subject='Hello, world', board=board, starter=user)
      Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user)
      url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
      self.response = self.client.get(url)

  def test_status_code(self):
      self.assertEquals(self.response.status_code, 200)

  def test_view_function(self):
      view = resolve('/boards/1/topics/1/')
      self.assertEquals(view.func.view_class, PostListView)