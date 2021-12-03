from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse

from .models import HelpMessage
from mainapp.models import Customer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if user:
            self['firstname'].initial = user.first_name
            self['surname'].initial = user.last_name
            self['email'].initial = user.email

    def clean(self):
        cleaned_data = super().clean()
        message = cleaned_data.get('message')
        if message and HelpMessage.objects.filter(message=message).exists():
            raise forms.ValidationError("Такое сообщение уже было отправлено в поддержку!")

    class Meta:
        model = HelpMessage
        fields = '__all__'

@login_required
def process_form(request):
    if request.method == 'GET':
        form = MessageForm(user=request.user)
        print(form)
        return render(request, 'help.html', {'form': form})
    elif request.method == 'POST':
        print(request.POST)
        user = request.user
        form = MessageForm(request.POST, user=user)
        print('=' * 100)
        if form.is_valid():
            data = form.cleaned_data
            message = data.get('message')
            firstname = data.get('firstname')
            surname = data.get('surname')
            print(data, message, surname, firstname, sep='\n')
            email = data.get('email')
            obj = HelpMessage(message=message, firstname=firstname, surname=surname, email=email)
            obj.save()
            return HttpResponse(f'''<p>Отправка прошла успешна.</p>
                            <a href="{reverse('base')}"> Вернуться на главную</a>''')
        else:
            return render(request, 'help.html', {'form': MessageForm(user=request.user), 'error': 'При отправке формы возникла ошибка. Возможно такое сообщение уже было отправлено.'})
