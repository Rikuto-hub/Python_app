from django.urls import path

from app import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("article/<int:pk>", views.ArticleDetailView.as_view(), name="article_detail"),
    path("article/new", views.CreateArticleView.as_view(), name="article_new"),
    path("article/<int:pk>/edit", views.ArticleEditView.as_view(), name="article_edit"),
    path("article/<int:pk>/delete", views.ArticleDeleteView.as_view(), name="article_delete")
]
