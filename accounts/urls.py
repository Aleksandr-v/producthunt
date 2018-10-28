from django.urls import path
from . import views


urlpatterns = [
    path('<int:user_id>/votes', views.UserVotesDetail.as_view(), name='user_votes'),
    path('', views.UserListView.as_view(), name='user-list'),
    path('profile/<int:pk>', views.UserProfile.as_view(), name='profile'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]
