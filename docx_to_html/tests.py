import json

from django.test import TestCase
from django.core.urlresolvers import reverse


class CodeCoverageTestCase(TestCase):
    def test_smoke(self):
        from docx_to_html import wsgi
        assert wsgi


class IndexTestCase(TestCase):
    url = reverse('index')

    def post(self, params=None, status_code=302):
        if params is None:
            params = {}
        r = self.client.post(self.url, params)
        self.assertEqual(r['Content-Type'], 'application/json')
        self.assertEqual(r.status_code, status_code)
        return json.loads(r.content)

    def test_GET_returns_405(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 405)

    def test_empty_POST_returns_JSON_response_with_errors(self):
        r = self.post(status_code=200)
        self.assertEqual(r, {u'file': [u'This field is required.']})
