from calendar import HTMLCalendar


class Timeline(HTMLCalendar):

    def __init__(self):
        super().__init__(self)

    def formatday(self, day, weekday):
        return f"{day}"

    def formatmonth(self, theyear, themonth, withyear=True):
        return f"{themonth}"

    def formatyear(self, theyear, width=12):
        return f"{theyear}"
