from django.contrib.auth import get_user_model
from django.test import TestCase

from knowledge_base.models import Category, Post, SubCategory

User = get_user_model()


class CategoryModelTest(TestCase):
    def setUp(self):
        # Создаем тестовую категорию
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="Test Description",
        )

    def test_category_creation(self):
        """Проверка создания категории."""
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.slug, "test-category")
        self.assertEqual(self.category.description, "Test Description")

    def test_category_str(self):
        """Проверка метода __str__."""
        self.assertEqual(str(self.category), "Test Category")


class SubCategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.subcategory = SubCategory.objects.create(
            name="Test SubCategory", category=self.category
        )

    def test_subcategory_creation(self):
        """Проверка создания подкатегории."""
        self.assertEqual(self.subcategory.name, "Test SubCategory")
        self.assertEqual(self.subcategory.category, self.category)

    def test_subcategory_str(self):
        """Проверка метода __str__."""
        self.assertEqual(str(self.subcategory), "Test SubCategory")

    def test_subcategory_relation_to_category(self):
        """Проверка связи подкатегории с категорией."""
        self.assertEqual(self.subcategory.category.name, "Test Category")
        self.assertIn(self.subcategory, self.category.subcategories.all())


class PostModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        # Создаем тестовую категорию
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        # Создаем тестовую подкатегорию
        self.subcategory = SubCategory.objects.create(
            name="Test SubCategory", category=self.category
        )
        # Создаем тестовый пост
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            category=self.category,
            subcategory=self.subcategory,
            author=self.user,
        )

    def test_post_creation(self):
        """Проверка создания поста."""
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "Test Content")
        self.assertEqual(self.post.category, self.category)
        self.assertEqual(self.post.subcategory, self.subcategory)
        self.assertEqual(self.post.author, self.user)

    def test_post_str(self):
        """Проверка метода __str__."""
        self.assertEqual(str(self.post), "Test Post")

    def test_post_relation_to_category(self):
        """Проверка связи поста с категорией."""
        self.assertEqual(self.post.category.name, "Test Category")
        self.assertIn(self.post, self.category.posts.all())

    def test_post_relation_to_subcategory(self):
        """Проверка связи поста с подкатегорией."""
        self.assertEqual(self.post.subcategory.name, "Test SubCategory")
        self.assertIn(self.post, self.subcategory.posts.all())

    def test_post_relation_to_author(self):
        """Проверка связи поста с автором."""
        self.assertEqual(self.post.author.username, "testuser")
        self.assertIn(self.post, self.user.posts.all())

    def test_post_toggle_like(self):
        """Проверка метода toggle_like."""
        self.post.toggle_like(self.user)
        self.assertIn(self.user, self.post.likes.all())

        self.post.toggle_like(self.user)
        self.assertNotIn(self.user, self.post.likes.all())
