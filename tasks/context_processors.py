"""Context processors for the tasks app"""
import pytz
from tasks.forms import TimezoneForm

def timezone_form(request):
    """Gives the timezone form to every view"""
    timezone = request.session.get("django_timezone")
    if timezone in pytz.common_timezones:
        form = TimezoneForm({'timezone' : timezone})
    else:
        form = TimezoneForm({'timezone' : 'UTC'})
    return {'timezone_form' : form}
