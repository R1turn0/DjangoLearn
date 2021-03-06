from django.urls import path
from . import views

app_name = 'polls'  # 设置命名空间
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
'''
对url设置namespace的时候能够让template模块下的视图文件通过命名空间来进行识别，
对多个app项目存在的情况
<a href="{% url 'detail' question.id %}">
会因为多个app中的detail的存在而错误识别。
<a href="{% url 'polls:detail' question.id %}">
添加对应app路径进行定位
'''