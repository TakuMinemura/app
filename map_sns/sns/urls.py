from django.urls import path
from . import views

app_name    = "sns"
urlpatterns = [
    path('', views.index, name="index"),
    # single/1/ であればviews.singleを実行する。single/test/ などはviews.single実行しない
    path('single/<int:pk>/', views.single, name="single"),

    
    #user_editはmypageに統一する。mypageにて、ダイレクトメッセージの送受信を行う。
    #path('user_edit/', views.user_edit, name="user_edit"),
    path('mypage/', views.mypage, name="mypage"),
    path('message/', views.message, name="message"),

    path('user/<uuid:pk>/', views.user, name="user"),
]

