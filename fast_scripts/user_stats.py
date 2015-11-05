"""
Plots info about user and writes it down to csv file for format:
    users = {
        'app_id_1': {'2015-01-01 00:00:00': 2, 2015-01-03 00:00:00': 4},
        'app_id_2': {'2015-01-01 00:00:00': 2, 2015-01-04 00:00:00': 6},
        ...
    }

"""
import csv
import json
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, DateFormatter


# basic conf
PATH_TO_FILE = '/home/greg/Pulpit/info'
PATH_TO_OUTPUT = '/home/greg/Pulpit/stats/'
MIN_DAYS_OF_USE = 4
PLOT_NO = -1


def read_data():
    """
    read info from file.
    """
    all_users_str = ""
    with open(PATH_TO_FILE, 'r') as f:
        all_users_str = f.read()
    all_users = json.loads(all_users_str)
    users = {}

    # extract useful users
    for app_id, user_info in all_users.iteritems():

        conditions = [
            app_id.startswith('ios_launch') or app_id.startswith('alv10'),
            len(user_info) >= MIN_DAYS_OF_USE,
        ]
        if all(conditions):
            users[app_id] = user_info
    return users


def get_user_data(no, users):
    user = users[users.keys()[no]]
    return user


def user_stat(user_data):
    """
    parses info for usr.
    """
    user = [
        (datetime.strptime(point[0].split(" ")[0], "%Y-%m-%d"), point[1])
        for point in user_data.iteritems()
    ]
    user = sorted(user)
    x = np.array(zip(*user)[0])
    y = np.array(zip(*user)[1])


    delta = timedelta(days=1)
    current_date = x[0]
    all_dates = []
    while current_date <= x[-1]:
        all_dates.append(current_date)
        current_date = current_date + delta

    all_y = []
    for i, dt in enumerate(all_dates):
        if dt not in x:
            all_y.append(0)
        else:
            all_y.append(user_data[str(dt).split(".")[0]])
    return all_dates, all_y


def write_csv(no, all_dates, all_y):
    with open(PATH_TO_OUTPUT + 'user%s.csv' % no, 'wt') as f:
        writer = csv.writer(f)
        writer.writerow( ('No', 'Day', 'Count') )
        for i in xrange(len(all_dates)):
            writer.writerow((i+1, all_dates[i], all_y[i]))


def plot(all_dates, all_y):
    fig, ax = plt.subplots()
    ax.plot_date(all_dates, all_y)
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
    fig.autofmt_xdate()
    plt.show()


def main():
    users = read_data()
    HOW_MANY = len(users)
    print HOW_MANY
    for i in xrange(HOW_MANY):
        all_dates, all_y = user_stat(get_user_data(i, users))
        write_csv(i, all_dates, all_y)
        if PLOT_NO > -1 and i == PLOT_NO:
            plot(all_dates, all_y)

main()
