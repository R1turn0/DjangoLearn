# Django项目随记

## Django所提供的if/else等标签

```html
{% if latest_question_list %}	<!-- 判断latest_question_list-->
    <ul>
    {% for question in latest_question_list %}	<!--遍历latest_question_list-->
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}	<!--单次循环的停止标签-->
    </ul>	<!--从ul这个tag开始显示在页面上-->
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

------

## Models中类的str魔法方法

```python
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)	# 注意ForeignKey(外键)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

```


在Django terminal中对Choice类输出所有的Object时，显示的的信息。尝试Choice.objects.all()，会输出：

<QuerySet[Choice: Choice_text]

同时在Django中可以通过python terminal直接对models所对应的数据库进行新建，eg：

```python
from django.models import Choice
q = Choice(choice_text = 'Choice1', votes = 20, question_id = 1)	# 注意外键的存在，其指向Question表中的ID
q.save	
Choice.objects.all()	# 输出所有Choice中的内容
```

## .views

**polls.views**

```python
def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)	
# 返回template中的index.html模板文件，注意render优先查询与template中与app组件同名的dirctory中的文件
```

order by polls_question 表中的 pub_date(publish date) 对表中的前五个数据进行切片并排序。

传递的元组对象的正负决定对应数据排序的正序倒序。

## urls

**polls.urls**

```python
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

```

对url设置namespace的时候能够让template模块下的视图文件通过命名空间来进行识别，
对多个app项目存在的情况
<a href="{% url 'detail' question.id %}">
会因为多个app中的detail的存在而错误识别。
<a href="{% url 'polls:detail' question.id %}">
添加对应app路径进行定位。**这必须建立在应用（app）中存在了命名空间的设置（app_name = ''）。**

**polls.template.polls.detail.html**

```html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```

