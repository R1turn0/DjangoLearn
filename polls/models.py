import datetime

from django.db import models


# Create your models here.
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')   # datetimefield 日期时间字段

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text
    datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    '''
    在Django terminal中对Choice类输出所有的Object时，
    显示的的信息。尝试Choice.objects.all()，会输出：
    <QuerySet[Choice: Choice_text]
    '''

