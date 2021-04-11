from .models import Category

def common(request):
    category = Category.objects.all()
    context = {
        'categories': category
    }
    return context