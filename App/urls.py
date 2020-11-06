from django.conf.urls import url
from django.views.generic import RedirectView

from App import views

urlpatterns = [
    url(r'^index/', views.index, name='home'),
    url(r'^formsearch/', views.formsearch, name='search'),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^testbs/', views.testbs, name='testbs'),
    url(r'^addform/', views.addform, name='addform'),
    url(r'^getdealform/', views.getdealform, name='getdealform'),
    url(r'^getmyform/', views.getmyform, name='getmyform'),
    url(r'^formdetail/(\d+)/', views.formdetail, name='formdetail'),
    url(r'^formvalid/', views.formvalid, name='formvalid'),
    url(r'^adddealrec/(\d+)/', views.adddealrec),
    url(r'^uploadfile/', views.uploadfile, name='uploadfile'),
    url(r'^formnew/', views.formnew, name='formnew')
]
