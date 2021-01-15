from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.render_search, name="render_search"),
    path("search/search", views.search, name="search"),
    path("result/", views.render_result, name="render_result"),

]
