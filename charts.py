import matplotlib.pyplot as plt
import pandas as pd


def chart1(df, year):
    df = df[df['year'] == year]
    fig, ax = plt.subplots(figsize=(12, 7))
    twin = ax.twinx()

    p1, = ax.plot(
        df['day'], df['temp_max'],
        color='red',
        label='temp. max',
        alpha=0.5
    )

    p2, = ax.plot(
        df['day'], df['temp_min'],
        color='blue',
        label='temp. min',
        alpha=0.5
    )

    p3, = ax.plot(
        df['day'], df['temp_avg'],
        color='grey',
        label='temp. avg',
        alpha=0.5
    )

    p4 = twin.bar(
        x=df['day'], height=df['rainfall'],
        color='lightgrey',
        label='rainfall',
        alpha=0.5
    )

    ax.axhline(0, c='grey', ls='--')
    ax.set_xlim(0)

    ax.set_xlabel('Day', fontsize=12)
    ax.set_ylabel('Temperature', fontsize=12)
    twin.set_ylabel('Rainfall [mm]', fontsize=12)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(handles=[p1, p2, p3, p4], frameon=False)

    fig1 = plt.gcf()
    fig1.savefig('static/chart.png')
    image_url = 'static/chart.png'

    return image_url

def chart2(df, month, year):
    one_station_months = df.groupby(by='day').agg(
        {'temp_avg': ['max', 'min']})

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.fill_between(
        one_station_months.index, one_station_months['temp_avg', 'min'], one_station_months['temp_avg', 'max'],
        color='lightgrey',
        alpha=0.5,
        label='1951-2023'
    )

    ax.plot(
        df['day'], df['temp_avg'],
        color='black',
        label=f'{month}.{year}',
        alpha=0.5
    )

    ax.axhline(0, c='grey', ls='--')
    ax.set_xlim(0)
    ax.set_xlabel('Day', fontsize=10)
    ax.set_ylabel('Temperature', fontsize=10)
    ax.legend(frameon=False)

    fig2 = plt.gcf()
    fig2.savefig('static/chart2.png')
    image_url2 = 'static/chart2.png'

    return image_url2

def chart3(df, month, year, station):
    fig3 = plt.gcf()
    fig3.savefig('static/chart3.png')
    image_url3 = 'static/chart3.png'
    return image_url3
