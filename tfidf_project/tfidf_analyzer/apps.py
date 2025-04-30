from django.apps import AppConfig

class TfidfAnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tfidf_analyzer'

import sys
print(sys.path)