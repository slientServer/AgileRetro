from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import User
from boards.models import Board
from django.db.models import Count, Q, F


# Restful API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import UsersSerializer

# Create your views here.
def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      auth_login(request, user)
      return redirect('home')
  else:
    form = SignUpForm()
  return render(request, 'signup.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user


# Restful API
class UsersStatisticView(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
      board = get_object_or_404(Board, id=request.query_params.get('pk', None))
      users = User.objects.all().filter(entity = board.entity, is_active=1).annotate(topics_count=Count('topics', filter=Q(topics__board=board), distinct=True)).annotate(posts_count=Count('posts', filter=Q(posts__topic__board=board), distinct=True))

      return Response(UsersSerializer(users, many=True).data)

