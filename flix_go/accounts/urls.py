from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from flix_go.settings import MEDIA_ROOT
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate,name='activate'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('forgotPassword/',views.forgotPassword,name="forgotPassword"),
    path('resetpassword_validate/<uidb64>/<token>', views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/', views.resetPassword,name='resetPassword'),
]