import os
import json

from django.test import TestCase
from django.core.urlresolvers import reverse


html_template = ''.join([
    '<html><head>',
    '<style>',
    '.pydocx-caps {text-transform:uppercase}',
    '.pydocx-center {text-align:center}',
    '.pydocx-comment {color:blue}',
    '.pydocx-delete {color:red;text-decoration:line-through}',
    '.pydocx-hidden {visibility:hidden}',
    '.pydocx-insert {color:green}',
    '.pydocx-left {text-align:left}',
    '.pydocx-right {text-align:right}',
    '.pydocx-small-caps {font-variant:small-caps}',
    '.pydocx-strike {text-decoration:line-through}',
    '.pydocx-tab {display:inline-block;width:4em}',
    '.pydocx-underline {text-decoration:underline}',
    'body {margin:0px auto;width:51.00em}',
    '</style>',
    '</head><body>',
    '%s',
    '</body></html>',
])


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

    def get_file_path(self, file_name):
        return os.path.join(
            os.path.abspath('.'),
            'docx_to_html',
            'fixtures',
            file_name,
        )

    def test_GET_returns_405(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 405)

    def test_empty_POST_returns_JSON_response_with_errors(self):
        r = self.post(status_code=200)
        self.assertEqual(r, {u'file': [u'This field is required.']})

    def test_POST_with_file_returns_302(self):
        file_path = self.get_file_path('simple.docx')
        with open(file_path) as fp:
            params = {
                'file': fp,
            }
            self.post(params=params)

    def test_POST_with_file_returns_html(self):
        file_path = self.get_file_path('simple.docx')
        with open(file_path) as fp:
            params = {
                'file': fp,
            }
            r = self.post(params=params)
        self.assertEqual(r, {'html': html_template % '<p>AAA</p>'})
