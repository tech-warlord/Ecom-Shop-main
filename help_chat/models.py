from django.db import models

class HelpMessage(models.Model):

    firstname = models.CharField(max_length=50, verbose_name='Имя', default='Not provided')
    surname = models.CharField(max_length=50, blank=True, verbose_name='Фамилия', default='Not provided')
    email = models.EmailField(max_length=100, verbose_name='Элетронная почта', default='test@mail.ru')
    message = models.TextField(verbose_name='Описание проблемы', unique=True)

    def __str__(self):
        return self.email
