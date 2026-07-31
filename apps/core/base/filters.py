"""
Django-filters uchun umumiy va maxsus filter klasslari.

Ushbu modul vergul bilan ajratilgan UUID, son yoki satrlar ro'yxati (in filter)
bo'yicha saralash imkonini beruvchi klasslarni o'z ichiga oladi.
"""

import django_filters


class UUIDInFilter(django_filters.BaseInFilter, django_filters.UUIDFilter):
    """Vergul bilan ajratilgan UUID ro'yxatlarini saralovchi filter."""

    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    """Vergul bilan ajratilgan sonlar ro'yxatlarini saralovchi filter."""

    pass


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """Vergul bilan ajratilgan satrlar ro'yxatlarini saralovchi filter."""

    pass

