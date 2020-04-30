import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
from datetime import datetime
import csv
from datetime import date
import sys



def date_range(start, end):
    r = (end+ timedelta(days=1)-start).days
    datelist = []
    for i in range(r):
        day = (start + timedelta(days=i))
        datelist.append(day.date())
    return datelist

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)



# publisher_list = {'devolver_digital': {'Absolver: Deluxe Edition': '1274264694', 'Shadow Warrior 2 Deluxe': '1728393087', 'My Friend Pedro Soundtrack': '1597428998', 'Minit': '1861202745', 'Metal Wolf Chaos XD': '2110873848', 'Reigns: Game of Thrones': '2060365190', 'Weedcraft Inc': '1960273452', 'Okhlos: Omega Olympus Edition': '2030042380', 'Shadow Warrior Classic Redux': '1618073558', 'Mother Russia Bleeds: Dealer Edition': '1183476395', 'The Swords of Ditto: Mormo�s Curse': '1673521992', 'Pikuniku': '1246381210', 'OlliOlli': '1207665033', 'Hotline Miami': '1207659118', 'EITR': '2067089149', 'Crossing Souls': '1271058609', 'Titan Souls': '1427985242', 'The Red Strings Club': '1939727646', 'Stories Untold': '1836830469', 'Broforce': '1470490225', 'Serious Sam: The Second Encounter': '1207658877', 'Crossing Souls Demo': '1398952847', "Block'hood": '1457531523', 'Hatoful Boyfriend: Holiday Star': '1450092067', 'Downwell': '1440214117', 'Reigns': '1677885333', 'Mother Russia Bleeds': '1230154140', 'A Fistful of Gun': '1442910587', 'Hatoful Boyfriend': '1207665623', 'Shadow Warrior Classic Complete': '1207659142', 'Dropsy': '1441869560', 'Ruiner': '1637928515', 'Absolver': '1816205133', 'Katana ZERO': '1557080015', 'OlliOlli2: Welcome to Olliwood': '1438603531', 'Gato Roboto': '1727534143', 'Always Sometimes Monsters': '1207664583', 'Stories Untold Demo': '1496064967', 'Shadow Warrior (2013)': '1207659573', 'Hotline Miami 2: Wrong Number': '1424773427', 'Gods Will Be Watching': '1207664883', 'Gods Will Be Watching: Special Edition': '1207665103', 'Enter the Gungeon': '1456912569', 'My Friend Pedro': '1102856701', 'GRIS': '2078272297', 'Hotline Miami 2: Wrong Number Digital Special Edition': '1424773562', 'OmniBus: Game of the Year Edition': '1119659879', 'Hotline Miami 2: Wrong Number - Digital Comics': '1424856371', 'Heave Ho': '1923235038', 'Serious Sam: The First Encounter': '1207658876', 'Reigns: Her Majesty': '1183536009', 'Not a Hero': '1429698467', 'Okhlos: Omega': '1318673719', "Serious Sam's Bogus Detour": '2104387650', 'Luftrausers': '1207661993', 'Shadow Warrior 2': '1434021265', 'Ronin': '1435570424', 'The Messenger': '1433116924', 'Ronin: Digital Special Edition': '1435570512', 'Ape Out': '1517967052', 'Not A Hero: Global MegaLord Edition': '1429699401', 'STRAFE: Millennium Edition': '1493047913'}}

def publishergames_insights(publishers_dict = {}):

    # Range of dates in which discount info is available
    start = datetime.fromtimestamp(1496361600.0)
    end = datetime.fromtimestamp(1538352000.0)
    dateslist = date_range(start,end)

    for publisher in publishers_dict.keys():
        with open('D:\Python\exercises\Webscraping\GOGDB\csvsgames\Results\\{}.csv'.format(publisher), 'w', newline='') as insightscsv:
            csv_writerinsights = csv.writer(insightscsv)
            csv_writerinsights.writerow(['Game', 'TimedeltaSum','TimedeltaMin', 'TimedeltaMax', 'Timedelta25', 'Timedelta50', 'Timedelta75',
                                 'BaseMin', 'BaseMax', 'FinalMin', 'FinalMax', 'DiscountMean', 'DiscountMin', 'DiscountMax',
                                 'Discount50', 'DiscountTimedelta'])

        with open('D:\Python\exercises\Webscraping\GOGDB\csvsgames\Results\\{}_gamesdiscounts.csv'.format(publisher), 'w', newline='') as timediscountscsv:
            csv_writerdiscounts = csv.writer(timediscountscsv)
            csv_writerdiscounts.writerow((['Game'] + dateslist))

        for gamename in publishers_dict[publisher]:
            if "The Swords of Ditto" in gamename:
                gamename = 'The Swords of Ditto'
            else:
                gamename = gamename.replace(':', '')
            # uprint(gamename)
            try:
                df = pd.read_csv('D:\Python\exercises\Webscraping\GOGDB\csvsgames\\{}_{}prices.csv'.format(publisher, gamename), header=1)
            except:
                continue

            #Adjust NaN
            df.replace('-', np.nan, inplace=True)

            if df['Base'].isnull().all() :
                continue

            #Adjust datetime format
            df[['End', 'Start']] = df[['End', 'Start']].apply(pd.to_datetime ,format='%B %d, %Y')

            #Add Timedelta column
            df.insert(2, 'Timedelta', ((df['End'] - df['Start'])))

            #Adjust Price format
            df[['Base', 'Final']] = df[['Base', 'Final']].replace('[\$,]', '', regex=True).astype(float)

            df['Discount'] = df['Discount'].replace('%', '', regex=True).astype(float)

            # Create table with discounted prices only
            dfdiscounted = df.dropna()

            #Adjust discount format
            dfdiscounted['Discount'] = (dfdiscounted['Discount'])/100

            #Create TimedeltaSum variable and DiscountTimedeltaSum column and variable
            TimedeltaSum = dfdiscounted['Timedelta'].sum()
            dfdiscounted.insert(6, 'DiscountTimedelta', ((df['Discount']/100) * (df['Timedelta'].apply(lambda x: (x/np.timedelta64(1, 'D'))))))
            DiscountTimedeltaSum = dfdiscounted['DiscountTimedelta'].sum()

            #Create a table with descriptive stats of the discounted prices table
            dfdiscountedstats = dfdiscounted.describe()

            # Add relevant descriptive statistics to the publisher's insights csv
            with open('D:\Python\exercises\Webscraping\GOGDB\csvsgames\Results\\{}.csv'.format(publisher), 'a', newline='') as insightscsv:
                csv_writerinsights = csv.writer(insightscsv)
                csv_writerinsights.writerow([gamename, TimedeltaSum, dfdiscountedstats.loc['min', 'Timedelta'], dfdiscountedstats.loc['max', 'Timedelta'],
                                            dfdiscountedstats.loc['25%','Timedelta'], dfdiscountedstats.loc['50%', 'Timedelta'], dfdiscountedstats.loc['75%', 'Timedelta'],
                                            dfdiscountedstats.loc['min', 'Base'], dfdiscountedstats.loc['max', 'Base'], dfdiscountedstats.loc['min', 'Final'],
                                            dfdiscountedstats.loc['max', 'Final'], dfdiscountedstats.loc['mean', 'Discount'], dfdiscountedstats.loc['min', 'Discount'],
                                            dfdiscountedstats.loc['max', 'Discount'], dfdiscountedstats.loc['50%', 'Discount'], DiscountTimedeltaSum])




            # Assign discount to each day in the list above
            discounteddatedict = {}
            for start, end, discount in zip(dfdiscounted['Start'].iteritems(), dfdiscounted['End'].iteritems(), dfdiscounted['Discount'].iteritems()):
                try:
                    start = datetime.fromtimestamp(pd.Timestamp.timestamp(start[1]))
                    end = datetime.fromtimestamp(pd.Timestamp.timestamp(end[1]))
                    dateslist_sub = date_range(start,end)
                except:
                    dateslist_sub = []
                for item in dateslist_sub:
                    discounteddatedict.update({item : discount})

            #Add the respective discounts to the csv as per the dictionary above
            url = 'D:\Python\exercises\Webscraping\GOGDB\csvsgames\Results\\{}_gamesdiscounts.csv'.format(publisher)
            with open(url, 'a', newline='') as timediscountscsv:
                csv_writerdiscounts = csv.writer(timediscountscsv)
                csv_writerdiscounts.writerow([gamename])

            dftimediscounts = pd.read_csv(url, header=0, index_col='Game', )

            for item in dftimediscounts.loc[gamename].iteritems():
                itemdate = datetime.strptime(item[0], '%Y-%m-%d').date()
                if itemdate in discounteddatedict:
                    dftimediscounts.at[gamename, item[0]] = discounteddatedict[itemdate][1]
                else:
                    dftimediscounts.at[gamename, item[0]] = 'NaN'

            dftimediscounts.to_csv(url)

# publisher_insights(publisher_list)
