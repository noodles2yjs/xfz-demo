from django.http import Http404
from django.shortcuts import render

from apps.news.forms import PublicCommentForm
from apps.news.models import News, NewsCategory, Comment, Banner
from django.conf import settings

from apps.news.serializers import NewsSerializer, CommentSerializer
from apps.xfzauth.decorators import xfz_login_required
from utils import restful

count=settings.ONE_PAGE_NEWS_COUNT

def index(request):

    newses=News.objects.select_related('category','author').order_by('-pub_time')[0:count]
    categories=NewsCategory.objects.all()
    context={
        'newses':newses,
        'categories':categories,
        'banners':Banner.objects.all()
    }
    return render(request, 'news/index.html',context=context)
def news_list(request):
    # 通过p参数，来指定要获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式传过来的/news/list/?p=2
    #request.GET.get('p', 1) 默认给p传了个1
    page=int(request.GET.get('p', 1))
    # 分类为0：代表不进行任何分类，直接按照时间倒序排序
    category_id=int(request.GET.get('category_id',0))
    start=(page-1)*count
    end=start + count
    if category_id == 0:
        newses=News.objects.select_related('category','author').all()[start:end]
    else :
        newses=News.objects.select_related('category','author').filter(category__id=category_id)[start:end]

    # many=True--newses有多条数据,都需要序列化
    serializer=NewsSerializer(newses,many=True)
    data=serializer.data
    return restful.result(data=data)



def news_detail(request,news_id):
    #使用get()如果没找到,或者有多个则会抛出异常
    try:
        news = News.objects.select_related('category','author').get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)

    except:
        raise Http404


def search(request):
    return render(request,'search/search.html')

'''def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        try:
            news_id = form.cleaned_data.get('news_id')
            content = form.cleaned_data.get('content')
            news = News.objects.get(pk=news_id)
            comment = Comment.objects.create(content=content, news=news, author=request.user)
            serializer = CommentSerializer(comment)
            return restful.result(data=serializer.data)
        except News.DoesNotExist:
            raise Http404
    else:
        return restful.params_error(message=form.errors())'''
@xfz_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serizlize = CommentSerializer(comment)
        return restful.result(data=serizlize.data)
    else:
        return restful.params_error(message=form.get_errors())

