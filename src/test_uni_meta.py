# coding:utf-8
__author__ = 'yoni'

import unittest
import markdown
from uni_meta import uni_meta

TEST_TEXT = u"""
שלום: עולם
hello: world
ערב: חדש

regular text
""".strip()


class MyTestUniMeta(unittest.TestCase):
    def test_uni_meta(self):
        md = markdown.Markdown(extensions=[uni_meta])
        html = md.convert(TEST_TEXT)
        self.assertTrue(md.Meta, "Metadata is empty")
        self.assertEqual(html, "<p>regular text</p>", "html was not extracted well")


if __name__ == '__main__':
    unittest.main()
