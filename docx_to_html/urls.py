from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'docx_to_html.views',
    url(r'^$', 'index', name='index'),
)
