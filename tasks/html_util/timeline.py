
from calendar import HTMLCalendar, monthrange

from django.db.models.functions import datetime

from tasks.models import Task


class Timeline(HTMLCalendar):

    def __init__(self, user):

        self.tasks = user.task_set.all()
        super(HTMLCalendar, self).__init__()

    def formatday(self, day, weekday):
        year = self.current_year
        month = self.current_month
        date = datetime.datetime(year, month, day)
        day_tasks = self.tasks.filter(deadline__range=[datetime.datetime.combine(date, datetime.datetime.min.time()),
                                      datetime.datetime.combine(date, datetime.datetime.max.time())])
        html = f'{day}<div class="col-6">'
        for task in day_tasks:
            html += f'<div class="row"> {task.name} </div>'
        html += '</div>'
        return html

    def formatmonth(self, year, themonth, withyear=True):
        self.current_year = year
        self.current_month = themonth
        html = '<div class="col-12"> '

        for day in range(1,monthrange(year, themonth)[1],1):

            html += self.formatday(day, datetime.datetime(year, themonth, day).weekday())
        html += '</div>'
        return html


    def formatyear(self, year, width=12):
        html = '<div class="container">'
        pagination = '<nav aria-label ="Year navigation"> <ul class "pagination">'
        for month in range(1, 12):
            html += '<div class="col-2">'
            pagination += f'<li class="page-item"><a href="/timeline/{year}/{month}">Month {month}</a> </li>'
            html += self.formatmonth(year,month)
            html += '</div>'
        html += '</div>'
        pagination += '</ul> </nav>'
        return pagination+html

    def returnHTMLPages(self):
        oldest_date = 2020
        years_displayed = 20
        pagination = '<nav aria-label ="Year navigation"> <ul class "pagination">'
        html = ""
        for year in range(1,years_displayed):
            pagination += f'<li class="page-item"><a href="/timeline/{year}/">Year {year}</a> </li>'
            html += self.formatyear(oldest_date+year)
        pagination += '</ul> </nav>'
        return pagination + html