from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from .models import Post

User = get_user_model()


class PostModelTestCase(TestCase):
    def setUp(self):
        random_user = User.objects.create(
            username = 'dindindin'
        )

    def test_post_item(self):
        obj = Post.objects.create(
            user=User.objects.first(),
            title="test case"
        )
        self.assertTrue(obj.title == "test case")
        self.assertTrue(obj.id==1)
        absolute_url = reverse("posts:detail", kwargs={"pk": 1})
        self.assertEqual(obj.get_absolute_url(), absolute_url)
