import calendar
from calendar import HTMLCalendar, monthrange

from django.db.models.functions import datetime
from django.utils.timezone import get_current_timezone

from tasks.models import Task


class Timeline(HTMLCalendar):
    """Constructs a calendar-style task display HTML element"""

    def __init__(self, user):

        self.tasks = user.task_set.all()
        super(HTMLCalendar, self).__init__()

    def formatday(self, day, weekday):
        """Displays tasks for a given day"""
        year = self.current_year
        month = self.current_month
        date = datetime.datetime(year, month, day)
        tz = get_current_timezone()
        day_tasks = self.tasks.filter(deadline__range=[datetime.datetime.combine(date, datetime.datetime.min.time(), tz),
                                                       datetime.datetime.combine(date, datetime.datetime.max.time(), tz)])
        html = f'<div class="col-3"><span class="border">{day}'
        if len(day_tasks) != 0:
            for task in day_tasks:
                html += f'<div class="card"> <div class="card-body"> <h5 class="card-title">{task.name}</h5> <h6 class="card-subtitle mb-2 text-muted">{task.description}</h6> </div></div>'
        html += '</span> </div>'
        return html

    def formatmonth(self, year, month, withyear=True):
        """Displays tasks for a given Month"""
        self.current_year = year
        self.current_month = month

        html = '<div class="row">'
        html += f'<h2> {calendar.month_name[month]} </h2>'
        for day in range(1, monthrange(year, month)[1], 1):
            html += self.formatday(day, datetime.datetime(year, month, day).weekday())
        html += '</div>'
        return html

    def formatyear(self, year, width=12):
        """Displays tasks for a given year"""
        pagination = f'<h1> {year} </h1> <nav aria-label="Year navigation"> <ul class="pagination justify-content-center">'
        html = ''
        for month in range(1, 13):
            pagination += f'<li class="page-item"><a class="page-link" href="/timeline/{year}/{month}">{calendar.month_name[month]}</a> </li>'
            html += self.formatmonth(year, month)
        pagination += '</ul> </nav>'
        return pagination + html

    def returnHTMLPages(self):
        """Displays tasks for from 2023 to the current year + 5"""
        oldest_date = 2023
        current_date = datetime.timezone.localdate(datetime.timezone.now()).year + 5
        pagination = '<nav aria-label="navigation"> <ul class="pagination justify-content-center">'
        html = ''
        for year in range(oldest_date, current_date):
            pagination += f'<li class="page-item"><a class="page-link" href="/timeline/{year}/">Year {year}</a> </li>'
            html += self.formatyear(year)

        pagination += '</ul> </nav>'
        return pagination + html
