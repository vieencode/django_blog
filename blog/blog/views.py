from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.views.generic import ListView
from django.db.models import Count 
from taggit.models import Tag
from blog.models import Post
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import SearchForm
from django.views.decorators.csrf import csrf_exempt


def post_list(request, tag_slug=None):

    post_list = Post.published.all()
    post_tags_ids = post_list.values_list('tags', flat=True).distinct().order_by()
    post_tags = Tag.objects.filter(id__in=post_tags_ids) 

    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            post_list = Post.published.annotate(search=search_vector,
                                                rank=SearchRank(search_vector, search_query)
                                               ).filter(search=search_query).order_by('-rank')
    

    tag = None 
    if tag_slug: 
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3) 
    page = request.GET.get('page')
    try: 
        posts = paginator.page(page)
    except PageNotAnInteger: 
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 

    context = {
        'page': page,
        'posts': posts,
        'post_tags': post_tags,
        'tag': tag, 
        'form': form,
        'query': query,
    }
    
    return render(request, 
                  'blog/post/list.html', 
                  context)

#class PostListView(ListView):
#    queryset = Post.published.all()
#    context_object_name = 'posts'
#    paginate_by = 3 
#    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year, 
                                   publish__month=month,
                                   publish__day=day) 

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    context = {
        'post': post,
        'similar_posts': similar_posts

    }

    return render(request, 
                 'blog/post/detail.html', 
                 context)

def post_detail_draft(request, post):
    post = get_object_or_404(Post, slug=post,
                                   status='draft') 

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    context = {
        'post': post,
        'similar_posts': similar_posts

    }

    return render(request, 
                 'blog/post/detail.html', 
                 context)


def blog_about(request):
    return render(request, "about.html")

def blog_tech_specs(request):
    return render(request, "tech_specs.html")
    

@csrf_exempt
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post_likes = post.likes 
                post_likes += 1
                post.likes = post_likes
                post.save()
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})


