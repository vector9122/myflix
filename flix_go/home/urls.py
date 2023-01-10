from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from flix_go.settings import MEDIA_ROOT
from. import views
urlpatterns = [
    path("", views.home,name='home'),
    path("details/<int:id>/", views.details, name='details'),
    path('import_data_to_db/', views.import_data_to_db,name='import_dtat_to_db'),
    path('export_data_to_db/', views.export_data_to_db,name='export_dtat_to_db'),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)