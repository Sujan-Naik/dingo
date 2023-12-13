"""Middleware for the tasks app"""
import zoneinfo
import pytz
from django.utils import timezone

class TimezoneMiddleware:
    """Activates the timezone saved in the user's session"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get("django_timezone")
        if tzname in pytz.common_timezones:
            timezone.activate(zoneinfo.ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
