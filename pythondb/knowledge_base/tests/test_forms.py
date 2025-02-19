from django.contrib.auth import get_user_model
from django.test import TestCase

from knowledge_base.forms import PostForm, SubcategoryForm
from knowledge_base.models import Category, SubCategory

User = get_user_model()


class PostFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.subcategory = SubCategory.objects.create(
            name="Test SubCategory", category=self.category
        )

    def test_post_form_valid_data(self):
        form_data = {"title": "Test Post", "content": "This is a test content."}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_form_empty_title(self):
        form_data = {"title": "", "content": "This is a test content."}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], ["Обязательное поле."])

    def test_post_form_empty_content(self):
        form_data = {"title": "Test Post", "content": ""}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["content"], ["Обязательное поле."])

    def test_post_form_widget_attrs(self):
        form = PostForm()
        self.assertEqual(
            form.fields["content"].widget.attrs["placeholder"],
            'Для форматирования кода используйте тройные кавычки (```), например:\n\n```python\ndef example():\n    print("Это пример кода")\n```',
        )


class SubcategoryFormTest(TestCase):
    def test_subcategory_form_valid_data(self):
        form_data = {"name": "Test SubCategory"}
        form = SubcategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_subcategory_form_empty_name(self):
        form_data = {"name": ""}
        form = SubcategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["Обязательное поле."])
