from django import forms

from .models import Category

class ArticleForm(forms.Form):
    categories = Category.objects.all()
    category_choice = {}
    for category in categories:
        category_choice[category] = category
    title = forms.CharField(label='内容', widget=forms.Textarea())
    category = forms.ChoiceField(label='カテゴリ', widget=forms.Select, choices=list(category_choice.items()), required=False)
    content = forms.CharField(label='内容', widget=forms.Textarea())
    image = forms.ImageField(label='イメージ画像', required=False)