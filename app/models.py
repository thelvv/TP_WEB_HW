from django.db import models
from django.utils import timezone


class Author(models.Model):
    avatar = models.ImageField(default='/static/img/alien.png')

    class Meta:
        verbose_name = 'Доп. информация о пользователе'
        verbose_name_plural = 'Доп. информация о пользователях'


class User(models.Model):
    identificator = models.IntegerField(verbose_name='id пользователя', default=0)
    name = models.CharField(max_length=50, default='', verbose_name='Имя')
    password = models.CharField(max_length=32, default='', verbose_name='Пароль')
    email = models.EmailField(max_length=50, default='', verbose_name='E-mail')
    author = models.OneToOneField(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Tag(models.Model):
    title = models.TextField(null=True, verbose_name='Тег')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class QuestionManager(models.Manager):
    def hot_questions(self):
        return self.order_by('-rating')

    def new_questions(self):
        return self.order_by('-date_create')

    def questions_by_tag(self, tag):
        return self.filter(tags__title=tag)

    class Meta:
        verbose_name = 'User'


class Question(models.Model):
    identificator = models.IntegerField(verbose_name='id вопроса', default=0)
    rating = models.IntegerField(default=0, verbose_name='рейтинг вопроса')
    answers_count = models.IntegerField(default=0, verbose_name='количество ответов')
    title = models.CharField(max_length=256, verbose_name='Заголовок', null=True)
    text = models.CharField(null=True, max_length=1024, verbose_name='Текст')
    date_create = models.DateField(verbose_name='Дата создания', null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    objects = QuestionManager()

    def __str__(self):
        return self.title

    def rate_up(self):
        self.rating = self.rating + 1

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    rating = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    is_right = models.BooleanField(default=False, verbose_name='Правильность')
    text = models.TextField(null=True, verbose_name='Текст')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class QuestionLikes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, verbose_name='Вопрос')
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Лайк на вопрос'
        verbose_name_plural = 'Лайки на вопросы'


class AnswerLikes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Лайк на ответ'
        verbose_name_plural = 'Лайки на ответы'
