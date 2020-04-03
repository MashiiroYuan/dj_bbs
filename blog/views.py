from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmialPostForm, CommentForm, SrarchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from django.contrib.postgres.search import TrigramSimilarity

# email验证
def post_share(request, post_id):
    # get post object
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # submit form
        form = EmialPostForm(request.POST)
        if form.is_valid():
            # confirm form
            cd = form.cleaned_data
            # send
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, '987639797@qq.com', [cd['to']])
            sent = True
            print('email success')
            print(sent)
            return render(request, 'blog/post/list.html')

    else:
        form = EmialPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def sendemail(request):
    print('send email+++++++++++++++++++++')
    email_title = '邮件标题'
    email_body = '邮件内容'
    email = '987639797@qq.com'  # 对方的邮箱
    print(email, email_body, email_title)
    send_mail(email_title, email_body, '987639797@qq.com', [email])
    return render(request, 'blog/base.html')


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'  # 设置模板变量名称
    paginate_by = 3  # 分页显示的数量
    template_name = 'blog/post/list.html'  # 指定模板


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    # posts = Post.objects.all()

    paginator = Paginator(object_list, 3)  # 每页3篇
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # page不为整数返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 超出总页数
        posts = paginator.page(paginator.num_pages)
    print(posts)

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status="published", publish__year=year, publish__month=month,
                             publish__day=day)
    print(post)
    # get comment
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # new comment not save to database
            new_comment = comment_form.save(commit=False)

            new_comment.post = post
            # save
            new_comment.save()
    else:
        comment_form = CommentForm()
    # 显示相似Tag文章列表
    post_tag_ids = post.tags.values_list('id', flat=True)
    similar_tags = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form,
                   'similar_posts': similar_posts})


# Create your views here.

def post_search(request):
    form = SrarchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SrarchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector=SearchVector('title',weight='A')+SearchVector('body',weight='B')
            search_query=SearchQuery(query)
            # results = Post.objects.annotate(search=SearchVector('title', 'slug', 'body'),).filter(search=query)
            # results=Post.objects.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).filter(rank__gte=0.3).order_by('-rank')
            results=Post.objects.annotate(similarity=TrigramSimilarity('title',query)).filter(similarity__gte=0.1).order_by('-similarity')
    return render(request, 'blog/post/search.html', {'query': query, 'form': form, 'results': results})

