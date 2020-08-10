import requests
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from datetime import datetime, timedelta

data = requests.get('https://pomber.github.io/covid19/timeseries.json').json()
prev = 0
cases = {}
dates = {}
countries = []
date_format = mpl_dates.DateFormatter('%b %d')
week_day = 0
total = 0
last_day = datetime.today()
week = timedelta(days=7)
plt.style.use('seaborn')
countries = input('Enter countries separated by space : ').split()

for country in countries:
    if country in data.keys():
        pass
    else:
        print(country + ' is not a valid country name. Please try again')
        exit()
for country in countries:
    total = 0
    week_day = 0
    prev = 0
    last_day = datetime.today()
    cases = []
    dates = []
    for num in data[country]:
        week_day+=1
        total += num['confirmed']-prev
        last_day = datetime.strptime(num['date'], '%Y-%m-%d')
        if week_day==7:
            cases.append(round(total/7, 2))
            total = 0
            week_day = 0
            dates.append(datetime.strptime(num['date'], '%Y-%m-%d')-week)
        prev = num['confirmed']
    if week_day!=0:
        cases.append(round(total/week_day, 2))
        dates.append(last_day-timedelta(days=week_day))
    plt.plot_date(dates, cases, label=country,linestyle='solid', marker=None)
plt.title('7 Day moving average - Daily New cases')
plt.tight_layout()
plt.gca().xaxis.set_major_formatter(date_format)
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()
