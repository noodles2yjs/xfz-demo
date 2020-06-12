from django.shortcuts import render

from apps.news.models import News,NewsCategory
from django.conf import settings

from apps.news.serializers import NewsSerializer
from utils import restful

count=settings.ONE_PAGE_NEWS_COUNT

def index(request):

    newses=News.objects.order_by('-pub_time')[0:count]
    categories=NewsCategory.objects.all()
    context={
        'newses':newses,
        'categories':categories,
    }
    return render(request, 'news/index.html',context=context)
def news_list(request):
    # 通过p参数，来指定要获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式传过来的/news/list/?p=2
    #request.GET.get('p', 1) 默认给p传了个1
    page = int(request.GET.get('p', 1))
    # 分类为0：代表不进行任何分类，直接按照时间倒序排序
    category_id = int(request.GET.get('category_id', 0))

    start=(page-1)*count
    end=start + count
    if category_id == 0:
        newses=News.objects.all()[start:end]
    else :
        newses=News.objects.filter(category__id=category_id)[start:end]

    # many=True--newses有多条数据,都需要序列化
    serializer=NewsSerializer(newses,many=True)
    data=serializer.data
    return restful.result(data=data)



def news_detail(request,news_id):
    return render(request,'news/news_detail.html')
def search(request):
    return render(request,'search/search.html')