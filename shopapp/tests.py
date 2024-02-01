from django.test import TestCase
from shopapp.utils import add_two_numbers
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from string import ascii_letters
from random import choices
from .models import Product, Order
from django.urls import reverse_lazy
from django.conf import settings

class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict()
        cls.user = User.objects.create_user(username="Bob", password="Jbez7NDCbhc22")
        permission = Permission.objects.get(codename="add_product")
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self)->None:
        self.client.force_login(self.user)
        self.product_name="".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    
    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:product-create"),
            {
              "name":self.product_name, 
              "price": "123.34", 
              "description": "A good table", 
              "discount": "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:product-list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict()
        cls.user = User.objects.create_user(username="Bob", password="Jbez7NDCbhc22")
        permission = Permission.objects.get(codename="add_product")
        cls.user.user_permissions.add(permission)
        cls.product = Product.objects.create(name="Best product", created_by = cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.user.delete()

    def test_get_product(self):
        responce = self.client.get(reverse("shopapp:product-detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(responce.status_code, 200)

    def test_get_product_and_check_content(self):
        responce = self.client.get(reverse("shopapp:product-detail", kwargs={"pk": self.product.pk}))
        self.assertContains(responce, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        'product-fixtures.json',
        'user-fixtures.json',
        'groups-fixtures.json',
        'group-fixtures.json',
        'permission-fixtures.json',
        ]

    # def test_products(self):
    #     response = self.client.get(reverse("shopapp:product-list"))
    #     for product in Product.objects.filter(archived=False).all():
    #         self.assertContains(response, product.name)

    # def test_products(self):
    #     response = self.client.get(reverse("shopapp:product-list"))
    #     products = Product.objects.filter(archived=False).all()
    #     products_ = response.context["products"]
    #     for p, p_ in zip(products,products_):
    #         self.assertEqual(p.pk, p_.pk)

    def test_products(self):
        response = self.client.get(reverse("shopapp:product-list"))
        self.assertQuerysetEqual(
            qs = Product.objects.filter(archived=False).all(),
            values = (p.pk for p in response.context["products"]),
            transform = lambda p: p.pk,
            )
        self.assertTemplateUsed(response, 'shopapp/product_list.html')


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="Bob", password="Jbez7NDCbhc22")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self)->None:
        self.client.force_login(self.user)
    
    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:order-list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:order-list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)

class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'product-fixtures.json',
        'user-fixtures.json',
        'groups-fixtures.json',
        'group-fixtures.json',
        'permission-fixtures.json',
        ]

    def test_get_products_view(self):
        response = self.client.get(reverse("shopapp:product-export"))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(products_data["products"], expected_data,)
