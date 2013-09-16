from django.test import TestCase
from website.views import get_blocks, extract_questions, FAQ


class WebsiteTest(TestCase):

    def test_get_blocks(self):
        self.assertEqual(["x", "y"], get_blocks("x\n\ny"))
        self.assertEqual(["x", "y"], get_blocks("\n\n\n\nx\n\n   \n\ny\n\n\n\n"))
        self.assertEqual(["x", "y", "a", "b"], get_blocks(
                  "x\n\ny\n\na\n\nb\n\n\n\n"))

    def test_extract_questions(self):
        self.assertEqual([("x", "y")], extract_questions("x\n\ny"))
        self.assertEqual([("x", "y"), ("a", "b")], extract_questions(
                  "x\n\ny\n\na\n\nb\n\n\n\n"))

    def test_faq(self):
        """
        Checks FAQ parsing
        """
        self.assertEqual(2, len(FAQ))

        for p in FAQ:
            self.assertGreater(len(p), 0)
            for q, a in p:
                self.assertIsInstance(q, str)
                self.assertIsInstance(a, str)
