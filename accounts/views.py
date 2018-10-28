from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views import View


class SignupView(View):
    def get(self, request):
        return render(request, 'accounts/signup.html')

    def post(self, request):
        #Check matches password and confirm_password
        if request.POST['password'] == request.POST['confirm_password']:
            #Check if exists user with this username
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':'This username has already been taken'})
            except User.DoesNotExist:
                # if user not exists greate new user and save in db
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                profile = Profile(user=user)
                profile.save()
                auth.login(request, user)
                return redirect('home')
        else:
            #Both passwords did not matches
            return render(request, 'accounts/signup.html', {'error':'Passwords must match. Try again'})

class LoginView(View):
    def get(self, request):
        next = request.GET.get('next', '')
        return render(request, 'accounts/login.html', {'next':next})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if request.POST['next_page'] is not '':
                return redirect(request.POST['next_page'])
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'accounts/login.html', {'error':'Incorrect username or password'})

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        return redirect('home')

    def get(self, request):
        return redirect('home')

@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class UserListView(ListView):

    model = User
    paginate_by = 3  # if pagination is desired
    template_name = 'user_list.html'
    ordering = ['-date_joined']

    def get_queryset(self):
        #original query set
        qs = super().get_queryset()
        return qs.exclude(username=self.request.user)


@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class UserProfile(DetailView):
    model = User
    context_object_name = 'hunter'
    template_name = "accounts/profile.html"

@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class UserVotesDetail(ListView):
    paginate_by = 10
    template_name = "accounts/user_votes.html"

    def get_queryset(self):
        self.hunter = get_object_or_404(User, pk=self.kwargs['user_id'])
        return self.hunter.product_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hunter'] = self.hunter
        return context
