
from django.contrib import admin
from django.urls import path , include
# from my_app.views import StudentApi
from my_app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path('Profile/', StudentApi.as_view()),
    path('admin/', admin.site.urls),
    path('', views.welcome, name='welcome'),
    path('user/', include('my_app.urls')),

    
    
    path('dashboard', views.dashboard ,name = 'dashboard' ),
    path('leaderboard' , views.leaderboard ,name = 'leaderboard' ),
    path('adminpanel', views.adminpanel, name ='adminpanel'),
    path('result', views.result, name= 'result')

    
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) 
