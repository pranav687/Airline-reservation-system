from django.urls import path
from django.conf.urls import url,include
from . import views

urlpatterns  = [
    path('',views.index,name='index'),
    url("search",views.search,name="search"),
    # url("book", views.book_flight,name="book_flight"),

    # url(r"^travel/search/flight/(?P<travel_id>[\w-]+)$", views.book_flight,name="book_flight"),
    url(r'^book/(?P<no_seats>[\w-]+)/(?P<travel_id>[\w-]+)/$', views.book_flight,name='book_flight'),
]