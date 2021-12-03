from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import HelpMessage
from mainapp.models import Customer
from .views import MessageForm

User = get_user_model()

class HelpChatTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()

        self.help_message = HelpMessage.objects.create(message='У меня есть проблема...', firstname=self.user.first_name,
                                                       surname=self.user.last_name, email=self.user.email)
        self.help_messageform = MessageForm(instance=self.help_message)

    def test_test_help_page_for_unregistered(self):
        '''Проверка может ли зайти на страницу незарегистрированный пользователь'''
        response = self.client.get('/help/')
        self.assertNotEqual(response.status_code, 200) #код 200 означает что переход на страницу прошло успешно

    def test_test_help_page_for_registered(self):
        '''Проверка может ли зайти на страницу зарегистрированный пользователь'''
        self.client.login(username='testuser', password='password')
        response = self.client.get('/help/')
        self.assertEqual(response.status_code, 200)

    def test_saving_same_help_forms(self):
        '''Проверка, что нельзя сохранять одинаковые сообщения в поддержку'''
        self.assertEqual(self.help_messageform.is_valid(), False)

    def test_saving_unique_help_forms(self):
        '''Проверка того, что после успешного заполнения формы, в базе данных появляется модель класса HelpMessage
        (т.е. сообщение отправляется в админку)'''
        message = 'уникальнейшее сообщение, которого нету в бд'
        self.client.login(username='testuser', password='password')
        response = self.client.post('/help/', {'message': message, 'firstname': 'Даня', 'surname': 'Воронов',
                                               'email': 'test@mail.ru'})
        self.assertEqual(HelpMessage.objects.filter(message=message).exists(), True)
