from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from knowledge_base.models import Category, SubCategory, Post



class KnowledgeBaseURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user_client = Client()
        self.user_client.login(username="testuser", password="testpass")

        # Создаем тестовые данные
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.subcategory = SubCategory.objects.create(name="Test SubCategory", category=self.category)
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            category=self.category,
            subcategory=self.subcategory,
            author=self.user,
        )

    def test_main_page(self):
        """Главная страница доступна всем."""
        response = self.guest_client.get(reverse("knowledge_base:main"))
        self.assertEqual(response.status_code, 200)

    def test_like_post(self):
        """Страница лайка поста доступна авторизованным пользователям."""
        url = reverse("knowledge_base:like_post", args=[self.post.id])
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_search_page(self):
        """Страница поиска доступна всем."""
        url = reverse("knowledge_base:search")
        response = self.guest_client.get(url, {
            "q": "test"})
        self.assertEqual(response.status_code, 200)

    def test_category_page(self):
        """Страница категории доступна всем."""
        url = reverse("knowledge_base:category", args=[self.category.slug])
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_page(self):
        """Страница поста доступна всем."""
        url = reverse("knowledge_base:post", args=[self.category.slug, self.subcategory.id])
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_post_page(self):
        """Страница создания поста доступна авторизованным пользователям."""
        url = reverse("knowledge_base:create_post", args=[self.category.slug, self.subcategory.id])
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_post_page(self):
        """Страница редактирования поста доступна авторизованным пользователям."""
        url = reverse("knowledge_base:edit_post", args=[self.category.slug, self.subcategory.id, self.post.id])
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_post_page(self):
        """Страница удаления поста доступна авторизованным пользователям."""
        url = reverse("knowledge_base:delete_post",
                      args=[self.category.slug, self.subcategory.id,
                            self.post.id])
        response = self.user_client.post(url)
        self.assertEqual(response.status_code, 302)