from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(label='内容', widget=forms.Textarea())
    content = forms.CharField(label='内容', widget=forms.Textarea())