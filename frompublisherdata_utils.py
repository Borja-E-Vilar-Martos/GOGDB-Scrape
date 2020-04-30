import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt


def discountsthroughtime(publisher):
    # Open csv
    df = pd.read_csv('D:\Python\exercises\Webscraping\GOGDB\csvsgames\Results\\{}_gamesdiscounts.csv'.format(publisher), index_col='Game')

    df.columns = pd.to_datetime(df.columns)

    # Detects beginning of sales periods, and creates variables positions and labels
    positions = []
    yestarray = np.zeros(shape=(1, len(df.index)))

    for d in df.columns:
        if yestarray.shape != np.asarray(np.where(df[d].isnull())).shape:
            condition = yestarray.shape[1] - np.asarray(np.where(df[d].isnull())).shape[1]
            if (abs(condition) > 5):
                positions.append(d)
            yestarray = np.asarray(np.where(df[d].isnull()))

    labels = [l.strftime('%m-%d-%y') for l in positions]

    # Create graph based on the two previos variables
    plt.rcParams["figure.figsize"] = (20, 10)
    ax = df.T.plot(legend=None)
    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    plt.gcf().autofmt_xdate()
    plt.grid(b=True, axis='x')
    plt.show()

# for publisher in publisher_dict.keys():

def allgamesgraph(publisher):
    # Open csv
    df = pd.read_csv('D:\Python\exercises\Webscraping\GOGDB\csvsgames\Results\\{}.csv'.format(publisher), index_col='Game')

    # Create edited graphs
    df.dropna(inplace=True)
    dfDiscountTimedelta = df.sort_values(['DiscountTimedelta'])
    dfDiscountTimedelta.set_index(['DiscountTimedelta', dfDiscountTimedelta.index], inplace=True)

    # Establish median and mean reference lines
    medianline = np.median(np.array(dfDiscountTimedelta.index.get_level_values(0)))
    meanline = np.mean(np.array(dfDiscountTimedelta.index.get_level_values(0)))

    # Create graph
    plt.rcParams["figure.figsize"] = (20, 10)
    plt.bar(dfDiscountTimedelta.index.get_level_values(1), dfDiscountTimedelta.index.get_level_values(0), color='lightseagreen')
    plt.axhline(medianline, color='tomato', linestyle='--')
    plt.axhline(meanline, color='gold', linestyle='--')
    plt.title('Devolver Digital')
    plt.gcf().autofmt_xdate()


def crosspublishercsv_creator(publishersdict = {}):

    # Create CSV with all publsihers
    with open('D:\Python\exercises\Webscraping\GOGDB\csvsgames\Results\\publishers_insights.csv', 'w') as publishers_insights:
        csv_writerpubinsights = csv.writer(publishers_insights)
        csv_writerpubinsights.writerow(['Publisher', 'NumberOfGames', 'TimedeltaSumMean', 'TimedeltaSum50',
                                        'TimedeltaSumMax', 'Timdelta5050', 'BaseMax50', 'FinalMin50',
                                        'DiscountMean50', 'DiscountMeanMean', 'Discount5050', 'Discount50Mean'
                                        'DiscountTimedeltaMean', 'DiscountTimedelta50', 'DiscountTimedeltaMax', 'DiscountTimedeltaStd'])

    for publisher in publishersdict.keys():

        # Open publisher's CSV
        df = pd.read_csv('D:\Python\exercises\Webscraping\GOGDB\csvsgames\Results\\{}.csv'.format(publisher), index_col='Game')

        # Obtain destcriptive stats
        df.dropna(inplace=True)
        df[['TimedeltaSum', 'TimedeltaMin', 'TimedeltaMax', 'Timedelta25', 'Timedelta50', 'Timedelta75']] = df[['TimedeltaSum', 'TimedeltaMin', 'TimedeltaMax', 'Timedelta25', 'Timedelta50', 'Timedelta75']].applymap(pd.to_timedelta) / pd.to_timedelta(1, unit='D')
        dfdescribe = df.describe()

        # Add line on each publishers with descriptive statistics of all game's descriptive statistics
        with open('D:\Python\exercises\Webscraping\GOGDB\csvsgames\Results\\publishers_insights.csv', 'a') as publishers_insights:
            csv_writerpubinsights = csv.writer(publishers_insights)
            csv_writerpubinsights.writerow([publisher, dfdescribe.loc['count', 'TimedeltaSum'], dfdescribe.loc['mean', 'TimedeltaSum'], dfdescribe.loc['50%','TimedeltaSum'],
                                           dfdescribe.loc['max', 'TimedeltaSum'],  dfdescribe.loc['50%','Timdelta50'], dfdescribe.loc['50%', 'BaseMax'], dfdescribe.loc['50%', 'FinalMin'],
                                            dfdescribe.loc['50%', 'DiscountMean'], dfdescribe.loc['mean', 'DiscountMean'], dfdescribe.loc['50%', 'Discount50'], dfdescribe.loc['mean', 'Discount50'],
                                            dfdescribe.loc['mean', 'DiscountTimedelta'], dfdescribe.loc['50%', 'DiscountTimedelta'],  dfdescribe.loc['max', 'DiscountTimedelta'], dfdescribe.loc['std', 'DiscountTimedelta']])
