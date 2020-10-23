from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index, name='home'),
    url(r'^formsearch/', views.formsearch, name='search'),
    url(r'^login/', views.login, name='login'),
    url(r'^testbs/', views.testbs, name='testbs'),
    url(r'^addform/', views.addform, name='addform')
]