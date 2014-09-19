#!/bin/sh
coverage run --source='docx_to_html/' manage.py test --verbosity=2 && coverage report --show-missing --fail-under=100 --omit="*test*.py" && find docx_to_html -name '*.py' | xargs flake8
