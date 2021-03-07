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

### **polls.views.index**

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

### **polls.views.detail**

```python
def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')
    #
    # return render(request, 'polls/detail.html', {'question': question})
    # 利用django内置的shortcut库来防止视图层和模型层的耦合
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', context={'question': question})
```

首先利用get_object_or_404方法根据question_id这一主键获取Question表中的数据并传给模板层的路径中的文件。return时将context中的字典数据作为request传输给路径页面（这一部分有待理解）

**注意使用render来重定向时，path路径默认会查询APP_NAME这个DIR中的template**

[函数执行完成后渲染模板层中的detail.html文件](#pollstemplatespollsdetailhtml)

### polls.views.vote

```python
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])    
        # 通过关键字名称获取POST数据中Choice的ID
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

接受到模型层detail.html中提交的POST表单数据后，将表单中name：choice按钮事件中的value值choice_id，并赋值给selected_choice，如果没有选择按钮，value会返回空。try语句进入except语句中并返回[原本的界面](#pollstemplatespollsdetailhtml)。else情况下数据库中votes数+1，并sava()记录到数据库中。

并进行函数运行。

## urls

### **polls.urls**

```python
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

```

对url设置namespace的时候能够让template模块下的视图文件通过命名空间来进行识别，
对多个app项目存在的情况
&lt;a href="{% url 'detail' question.id %}"&gt;
会因为多个app中的detail的存在而错误识别。
&lt;a href="{% url 'polls:detail' question.id %}"&gt;
添加对应app路径进行定位.

**note:不要忘记urlconf中path最后的'/'**

## Templates

### **polls.templates.polls.detail.html**

```html
<h1>{{ question.question_text }}</h1>	<!--获取Question表中的text数据-->
<h2>这个是{{ question.id }}号问题</h2>


{% if error_message %}	<!--如果传来的request中存在error_message则直接添加一行反馈数据，需要注意的是{%%}是django提供的Python嵌入HTML-->
    <p><strong>{{ error_message }}</strong></p>
{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}    <!--所有针对内部的表单提交数据都应该加上这一句-->
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>	<!--forloop.couter表示循环的次数-->
    {% endfor %}
<input type="submit" value="Vote">
</form>

```

HTML文件渲染完成后，若是提交表单，将会将数据传输给namespace:polls中的[vote路由](#pollsurls)。并执行路由中所设置的[vote](#pollsviewsvote)方法。

