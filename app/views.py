from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from functools import reduce
from operator import and_

from .models import Article, Category
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
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            article.category = category_data
            article.content = form.cleaned_data['content']
            if request.FILES:
                article.image = request.FILES.get('image')
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
                'category': article.category,
                'content': article.content,
                'image': article.image
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
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            article.category = category_data
            article.content = form.cleaned_data['content']
            if request.FILES:
                article.image = request.FILES.get('image')
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

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(nama=self.kwargs['category'])
        articles = Article.objects.order_by('-id').filter(category=category)
        return render(request, 'app/index.html', {
            'articles': articles
        })

class SearchView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.order_by('-id')
        keyword = request.GET.get('keyword')
        
        if keyword:
            exclusion_list = set(['', ''])
            query_list = ""
            for word in keyword:
                if not word in exclusion_list:
                    query_list += word
            query = reduce(and_, [Q(title__icontains=q) | Q(content__icontains=q) for q in query_list])
            articles = articles.filter(query)

        return render(request, 'app/index.html', {
            'keyword': keyword,
            'articles': articles
        })