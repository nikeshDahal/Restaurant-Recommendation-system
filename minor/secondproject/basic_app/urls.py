from django.conf.urls import url
from basic_app import views

app_name = 'basic_app'

urlpatterns= [

    url(r'^$',views.index,name='index'),
    url(r'^hawa/',views.hawa,name='hawa'),
    url(r'^about/',views.about,name='about'),
    url(r'^contact/',views.contact,name='contact'),
    url(r'^resturantList/',views.resturantList,name='resturantList'),
    url(r'^login/',views.login,name='login'),
    url(r'^Menu/',views.Menu,name='Menu'),
    url(r'^signup/',views.signup,name='signup'),
    url(r'^singleblog/',views.singleblog,name='singleblog'),
    # url(r'^nodata/',views.nodata,name='nodata'),
]