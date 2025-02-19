from django.test import Client, TestCase
from django.urls import reverse

from data import (
    CATEGORIES,
    CATEGORY,
    PATH_CATEGORIES,
    PATH_MAIN,
    PATH_POST,
    POSTS,
    SUBCATEGORIES,
    SUBCATEGORY,
)
from knowledge_base.models import Category, Post, SubCategory, User


class MainViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("knowledge_base:main")
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.subcategory = SubCategory.objects.create(
            name="Test SubCategory", category=self.category
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            category=self.category,
            subcategory=self.subcategory,
            author=self.user,
        )

    def test_main_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_main_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, PATH_MAIN)

    def test_main_view_context(self):
        response = self.client.get(self.url)
        self.assertIn("categories", response.context)
        self.assertIn("latest_posts", response.context)
        self.assertIn("top_users", response.context)


class CategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.url = reverse("knowledge_base:category", args=[self.category.slug])

    def test_category_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_category_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, PATH_CATEGORIES)

    def test_category_view_context(self):
        response = self.client.get(self.url)
        self.assertIn(CATEGORY, response.context)
        self.assertIn(SUBCATEGORIES, response.context)
        self.assertIn(CATEGORIES, response.context)


class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.subcategory = SubCategory.objects.create(
            name="Test SubCategory", category=self.category
        )

        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            category=self.category,
            subcategory=self.subcategory,
            author=self.user,
        )
        self.url = reverse(
            "knowledge_base:post",
            args=[self.category.slug, self.subcategory.id],
        )

    def test_post_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, PATH_POST)

    def test_post_view_context(self):
        response = self.client.get(self.url)
        self.assertIn(POSTS, response.context)
        self.assertIn(SUBCATEGORIES, response.context)
        self.assertIn(CATEGORIES, response.context)
        self.assertIn(CATEGORY, response.context)
        self.assertIn(SUBCATEGORY, response.context)


class CreatePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.subcategory = SubCategory.objects.create(
            name="Test SubCategory", category=self.category
        )

        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )

        self.url = reverse(
            "knowledge_base:create_post",
            args=[self.category.slug, self.subcategory.id],
        )

    def test_create_post_view_status_code_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_post_view_status_code_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_post_view_template(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "knowledge_base/created_post.html")

    def test_create_post_view_context(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertIn(SUBCATEGORIES, response.context)
        self.assertIn(CATEGORIES, response.context)
        self.assertIn(CATEGORY, response.context)
        self.assertIn(SUBCATEGORY, response.context)


class EditPostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.subcategory = SubCategory.objects.create(
            name="Test SubCategory", category=self.category
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            category=self.category,
            subcategory=self.subcategory,
            author=self.user,
        )
        self.url = reverse(
            "knowledge_base:edit_post",
            args=[self.category.slug, self.subcategory.id, self.post.id],
        )

    def test_edit_post_view_status_code_author(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_edit_post_view_status_code_non_author(self):
        other_user = User.objects.create_user(
            username="otheruser", password="testpass"
        )
        self.client.login(username="otheruser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_edit_post_view_template(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "knowledge_base/edit_post.html")

    def test_edit_post_view_context(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertIn(SUBCATEGORIES, response.context)
        self.assertIn(CATEGORIES, response.context)
        self.assertIn(CATEGORY, response.context)
        self.assertIn(SUBCATEGORY, response.context)


class DeletePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.subcategory = SubCategory.objects.create(
            name="Test SubCategory", category=self.category
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            category=self.category,
            subcategory=self.subcategory,  # Добавлено
            author=self.user,
        )
        self.url = reverse(
            "knowledge_base:delete_post",
            args=[self.category.slug, self.subcategory.id, self.post.id],
        )

    def test_delete_post_view_status_code_author(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_post_view_status_code_non_author(self):
        other_user = User.objects.create_user(
            username="otheruser", password="testpass"
        )
        self.client.login(username="otheruser", password="testpass")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_delete_post_view_get_request(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)


class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("knowledge_base:search")

    def test_search_view_status_code(self):
        response = self.client.get(self.url, {"q": "test"})
        self.assertEqual(response.status_code, 200)

    def test_search_view_template(self):
        response = self.client.get(self.url, {"q": "test"})
        self.assertTemplateUsed(response, "knowledge_base/search_results.html")

    def test_search_view_context(self):
        response = self.client.get(self.url, {"q": "test"})
        self.assertIn("query", response.context)
        self.assertIn("results", response.context)
        self.assertIn(CATEGORIES, response.context)


class LikePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.subcategory = SubCategory.objects.create(
            name="Test SubCategory", category=self.category
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            category=self.category,
            subcategory=self.subcategory,
            author=self.user,
        )
        self.url = reverse("knowledge_base:like_post", args=[self.post.id])

    def test_like_post_view_status_code_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_like_post_view_status_code_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class CreateSubcategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpass", is_staff=True
        )
        self.url = reverse(
            "knowledge_base:create_subcategory", args=[self.category.slug]
        )

    def test_create_subcategory_view_status_code_staff(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_subcategory_view_status_code_non_staff(self):
        non_staff_user = User.objects.create_user(
            username="nonstaff", password="testpass"
        )
        self.client.login(username="nonstaff", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_subcategory_view_template(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, "knowledge_base/create_subcategory.html"
        )
