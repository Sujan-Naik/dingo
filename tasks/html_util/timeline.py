
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

    def formatmonth(self, theyear, themonth, withyear=True):
        self.current_year = theyear
        self.current_month = themonth
        html = '<div class="col-12"> '
        for day in range(1,monthrange(theyear, themonth)[1],1):
            html += self.formatday(day, datetime.datetime(theyear, themonth, day).weekday())
        html += '</div>'
        return html


    def formatyear(self, theyear, width=12):
        return f"{theyear}"
