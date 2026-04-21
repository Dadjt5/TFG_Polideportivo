from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime

from ...models import Feedback


class FeedbackUnitTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="test",
            password="123456"
        )

    def test_str(self):
        feedback = Feedback.objects.create(
            usuario=self.user,
            tipo=Feedback.TipoFeedback.GENERAL,
            mensaje="Prueba feedback"
        )

        texto = str(feedback)

        self.assertIn("General", texto)
        self.assertIn(str(datetime.now().year), texto)