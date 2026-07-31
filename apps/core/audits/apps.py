"""
Audits ilovasi konfiguratsiyasi.
"""

from django.apps import AppConfig


class AuditsConfig(AppConfig):
    """Audits sub-ilovasi konfiguratsiya klassi."""

    name = "apps.core.audits"
    verbose_name = "Audit jurnali"

