from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


# here is what a explaintion for the PostListView clss
def post_list(request, tag_slug=None):
    post_list = Post.objects.all()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug= tag_slug)
        post_list= post_list.filter(tag__in=[tag])


    paginator = Paginator(post_list, 1)
    page_number = request.GET.get('page')
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts, 'tag':tag}
    return render(request, 'blogapp/list.html', context)

# class PostListView(ListView):
#     model = Post
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blogapp/list.html'

def post_detail(request,year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug = post,
                             publish__year = year,
                             publish__month = month,
                             publish__day = day,)
    # List of active comments for this post
    comments = post.comments.filter(active= True)
    # Form for users to comment
    form = CommentForm()

    # list of similar posts
    posts_tags_ids = post.tag.values_list('id', flat=True)

    similar_posts = Post.objects.filter(tag__in=posts_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags')

    context = {'post': post, 'comments': comments, 'form':form,'similar_posts':similar_posts}
    return render(request, 'blogapp/detail.html',context )

def post_share(request, post_id):
    post = get_object_or_404(Post, id= post_id, status= Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        
        if form.is_valid():

            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n{cd['name']}'s comments: {cd['comments']}" 
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    context = {'post': post,'form': form,'sent': sent}
    return render(request,'blogapp/share.html',context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id = post_id, status= Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data= request.POST)
    if form.is_valid():
        # Create a comment object without saving it to the database
        comment = form.save(commit= False)
        # Assign the comment to the database
        comment.post = post
        # save to the database 
        comment.save()
    return render(request,'blogapp/comment.html',{'post': post,'form': form,'comment': comment} )




def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query, config='english')
            results = Post.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            # results = Post.objects.annotate(search=SearchVector('title', 'body'),).filter(search=query)
    
    context = {'form': form,'query': query,'results': results}
    return render(request, 'blogapp/post/search.html', context)