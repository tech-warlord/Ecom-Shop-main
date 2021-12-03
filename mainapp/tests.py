from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Customer, Order, Category, Product, CartProduct, Cart
from decimal import Decimal
from .utils import recalc_cart
from .views import AddToCartView, MakeOrderView
from django.contrib import messages

User = get_user_model()

class MainAppTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.category = Category.objects.create(name='Ноутбуки', slug='notebooks')
        image = SimpleUploadedFile("aab0ec3c321650295344e1854d55b157.jpeg", content=b'', content_type='image/jpeg')
        self.notebook = Product.objects.create(category=self.category,
                                               title='Asus Classy',
                                               slug='asus',
                                               image=image,
                                               description='Descriptive description',
                                               price=Decimal('450000.00')
                                               )
        self.customer = Customer.objects.create(user=self.user, phone='888-111-222', address='address')
        self.cart = Cart.objects.create(owner=self.customer)
        self.notebook_product = CartProduct.objects.create(user=self.customer, cart=self.cart, product=self.notebook)
        self.order = Order.objects.create(customer=self.customer,
                                          first_name=self.user.first_name,
                                          last_name=self.user.last_name,
                                          phone=self.customer.phone,
                                          cart=self.cart,
                                          address=self.customer.address)

    def test_add_to_cart(self):
        '''Проверка успешного добавления в корзину товаров и правильности некоторых значений (как цена, и количество товаров в корзине)'''
        self.cart.products.add(self.notebook_product)
        recalc_cart(self.cart)
        self.assertIn(self.notebook_product, self.cart.products.all())
        self.assertEqual(self.cart.total_products, 1)
        self.assertEqual(self.cart.final_price, self.notebook_product.final_price)

    def test_add_to_cart_from_view(self):
        '''Проверка добавления товара в корзину через AddToCartView'''
        factory = RequestFactory()
        request = factory.get('/')
        request._messages = messages.storage.default_storage(request)
        request.user = self.user
        response = AddToCartView.as_view()(request, slug=self.notebook.slug)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')

    def test_makeorderform_from_view(self):
        '''Проверка, что после заполнения формы появляется заказ в базе данных'''
        factory = RequestFactory()
        request = factory.post('/', {'first_name': ['test first name'], 'last_name': ['test surname'],
                                     'phone': [self.customer.phone], 'address': [self.customer.address], 'order_date': ['2021-12-02'],
                                     'comment': 'test comment', 'buying_type': ['self']})
        request.user = self.user
        request._messages = messages.storage.default_storage(request)
        response = MakeOrderView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertEqual(Order.objects.filter(first_name='test first name').exists(), True)

