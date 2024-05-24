import matplotlib.pyplot as plt
import matplotlib as mpl

# charts parameters settings
mpl.rc('axes.spines', right=False, top=False)
mpl.rc('axes', labelsize=12)
mpl.rc('legend', frameon=False)
mpl.rc('figure', titlesize=16)

parameters = ['temp_max', 'temp_min', 'temp_avg']
colors = ['red', 'blue', 'grey']
values = ['max', 'min', 'mean']


def chart1(df, year, month):
    df = df[df['year'] == year]

    fig, ax = plt.subplots(2, 1, figsize=(12, 12))
    for parameter, color in zip(parameters, colors):
        ax[0].plot(df['day'], df[parameter],
                   color=color,
                   label=parameter,
                   alpha=0.5
                   )

    ax[1].bar(x=df['day'], height=df['rainfall'],
              color='lightgrey',
              label='rainfall',
              alpha=0.5
              )

    ax[0].axhline(0, c='grey', ls='--', alpha=0.5)
    ax[0].set(xlim=0, xlabel='Days', ylabel='Temperature')
    ax[1].set(xlim=0, xlabel='Days', ylabel='Rainfall [mm]')

    fig.suptitle(f'Temperatures in {month}.{year}')

    fig1 = plt.gcf()
    fig1.savefig('static/chart.png')
    image_url = 'static/chart.png'

    return image_url


def chart2(df, year, month):
    one_station_months = df.groupby(by='day').agg({"temp_avg": ['max', 'min', "mean"]})

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(
        one_station_months.index, one_station_months['temp_avg', 'min'], one_station_months['temp_avg', 'max'],
        color='lightgrey',
        alpha=0.5
    )

    for color, value in zip(colors[:2], values[:2]):
        ax.plot(one_station_months.index, one_station_months['temp_avg', value],
                color=color,
                alpha=0.5
                )

    ax.plot(df[df['year'] == year]['day'], df[df['year'] == year]['temp_avg'],
            color='black',
            linewidth=3,
            alpha=0.5,
            label=f'{month}.{year}'
            )

    ax.axhline(0, c='grey', ls='--', alpha=0.5)
    ax.set(xlim=0, xlabel='Days', ylabel='Temperature')
    ax.legend(fontsize=12, bbox_to_anchor=(1, 1))

    fig.suptitle(f'Range of Average Temperature between 1951-2023 in {month}')

    fig2 = plt.gcf()
    fig2.savefig('static/chart2.png')
    image_url2 = 'static/chart2.png'

    return image_url2


def chart3(df, year, month):
    one_station_trend = df.groupby(by=['year']).agg({'temp_max': 'max'})

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(one_station_trend.index, one_station_trend['temp_max'],
            color='red',
            alpha=0.5
            )

    ax.axhline(0, c='grey', ls='--', alpha=0.5)
    ax.axvline(year, c='grey', ls='-', alpha=0.5)

    fig.suptitle(f'Max Temperature between 1951-2023 in {month}')
    ax.set(xlabel='Years', ylabel='Avg. Temperature')

    fig3 = plt.gcf()
    fig3.savefig('static/chart3.png')
    image_url3 = 'static/chart3.png'
    return image_url3
