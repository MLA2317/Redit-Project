from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Article, Tag, Comment, Category
from .forms import CommentForm


def index(request):
    articles = Article.objects.order_by('-id')

    ctx = {
        'object_list': articles
    }
    return render(request, 'blog/index.html', ctx)


def article_list(request):
    articles = Article.objects.order_by('-id')
    cat = request.GET.get('cat')
    tag = request.GET.get('tag')
    search = request.GET.get('search')
    if cat:
        articles = articles.filter(category__title__exact=cat)  #aynan osha bolish kere yani cat
    if tag:
        articles = articles.filter(tags__title__exact=tag)
    if search:
        articles = articles.filter(title__icontains=search) #search ichidda bolsa yani bosh harfiga farq qilmaydi

    page_number = request.GET.get('page', 1)
    paginator = Paginator(articles, 1)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(1)
    ctx = {
        'object_list': page_obj
    }
    return render(request, 'blog/blog.html', ctx)


def article_detail(request, pk):
    article = get_object_or_404(Article, id=pk)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    last_3_articles = Article.objects.order_by('-id')[:3]
    form = CommentForm()
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(reverse("project:detail", kwargs={"pk": pk}))
        form = CommentForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)  #commit=False -- Bazaga saqlamitur
            obj.author_id = request.user.profile.id  # nma uchun profile oldik chunki onetoone bolgani uchun
            obj.article_id = article.id
            obj.save()
            return redirect('.')
    ctx = {
        'object': article,
        'categories': categories,
        'last_3_articles': last_3_articles,
        'tags': tags,
        'form': form,
    }
    return render(request, 'blog/blog-single.html', ctx)

