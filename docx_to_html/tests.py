from django.test import TestCase
from django.core.urlresolvers import reverse


class CodeCoverageTestCase(TestCase):
    def test_smoke(self):
        from docx_to_html import wsgi
        assert wsgi


class IndexTestCase(TestCase):
    url = reverse('index')

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
