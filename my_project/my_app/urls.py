from django.urls import path
from my_app import views 

urlpatterns = [
    path('all_quiz/', views.all_quiz_view, name='all_quiz'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('quiz/<int:quiz_id>/', views.quiz_view, name='quiz_view'),
    # path('submit/<int:quiz_id>/', views.submit_quiz, name='submit'),

]