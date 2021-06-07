from django.urls import path

from . import views

# create a namespace for this app
app_name = 'viz'

urlpatterns = [
    # path '' = root
    path('', views.index, name='index'),
]