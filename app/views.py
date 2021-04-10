from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Article
from .forms import ArticleForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.order_by("-id")
        return render(request, 'app/index.html', {
            'articles': articles,
        })

class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        article = Article.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/article_detail.html', {
            'article': article
        })

class CreateArticleView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        form = ArticleForm(request.POST or None)
        return render(request, 'app/article_new.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST or None)

        if form.is_valid():
            article = Article()
            article.author = request.user
            article.title = form.cleaned_data['title']
            article.content = form.cleaned_data['content']
            article.save()
            return redirect('article_detail', article.id)

        return render(request, 'app/Article_new.html', {
            'form': form
        })

class ArticleEditView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        article = Article.objects.get(id=self.kwargs['pk'])
        form = ArticleForm(
            request.POST or None,
            initial = {
                'title': article.title,
                'content': article.content
            }
        )

        return render(request, 'app/article_new.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST or None)

        if form.is_valid():
            article = Article.objects.get(id=self.kwargs['pk'])
            article.title = form.cleaned_data['title']
            article.content = form.cleaned_data['content']
            article.save()
            return redirect('article_detail', self.kwargs['pk'])

        return render(request, 'app/article_new.html', {
            'form': form
        })

class ArticleDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = Article.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/article_delete.html', {
            'article': article
        })

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(id=self.kwargs['pk'])
        article.delete()
        return redirect('index')