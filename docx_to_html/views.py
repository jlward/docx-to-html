import json
from tempfile import NamedTemporaryFile

from django.http import HttpResponse
from django.views.decorators.http import require_POST

from pydocx.parsers import Docx2Html

from docx_to_html.forms import UploadFileForm


class JSONResponse(HttpResponse):
    def __init__(self, context, status=302, **kwargs):
        kwargs.update({
            'content_type': 'application/json',
            'status': status,
        })
        return super(JSONResponse, self).__init__(
            json.dumps(context),
            **kwargs
        )


@require_POST
def index(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        with NamedTemporaryFile(mode='wrb+', suffix='.docx') as f:
            f.write(form.cleaned_data['file'].read())
            f.flush()
            f.seek(0)
            parser = Docx2Html(f.name)
            html = parser.parsed
        return JSONResponse({'html': html})
    return JSONResponse(form.errors, status=200)
