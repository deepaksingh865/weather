#*****************Hello**********************
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

places=['Aberporth', 'Armagh', 'Ballypatrick', 'Bradford', 'Braemar', 'Camborne', 'Cambridge', 'Cardiff','Chivenor',
        'Cwmystwyth', 'Dunstaffnage', 'Durham', 'Eastbourne', 'Eskdalemuir', 'Heathrow', 'Hurn', 'Lerwick','Leuchars',
        'Manston', 'Nairn', 'NewtonRigg', 'Oxford', 'Paisley', 'Ringway', 'RossonWye', 'Shawbury', 'Sheffield',
        'Southampton', 'Stornoway', 'SuttonBonington', 'Tiree', 'Valley', 'Waddington', 'WickAirport','Yeovilton']
flag=0
try:
    user_input=sys.argv[1]
    if(user_input not in places):
        flag=1
    location=user_input.lower()
    r = requests.get('https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{0}data.txt'.format(location))
    raw_data = r.text
    # ********* Removing special character and unwanted word************
    un = ["*", "#", "Provisional", "||", "---"]
    for i in un:
        if i == "---":
            data1 = raw_data.replace(i, "0")
            raw_data = data1
        else:
            data1 = raw_data.replace(i, "")
            raw_data = data1
    data2 = data1.split()

    # ***************Data Parsing********************************************
    p = (data2.index("hours") + 1)
    length = len(data2)
    datalist = []
    month = ["Jan", "Fab", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    while ((p + 7) < length):
        l = []
        for y in range(0, 7):
            if y == 0:
                l.append(int(data2[p + y]))
            elif y == 1:
                l.append(month[int((data2[p + y])) - 1])
            else:
                l.append(float(data2[p + y]))
        datalist.append(l)
        p = p + 7

    ###########DataFrame############
    df = pd.DataFrame(datalist, columns=["Year", "Month", "Max", "Min", "AF", "Rain", "Sunhour"])
    # df.to_csv("weather3.csv")
    m = df.loc[df["Year"].idxmax()]
    var_df = df[df['Year'] < m[0]]  # ********* Selection of 20 years
    required_df = var_df[var_df['Year'] > m[0] - 22]

    # ********* Average of Columns Data *******************
    Av = required_df.groupby(by="Year").mean()
    Av.reset_index(level=0, inplace=True)

    # **************Plotting*********************
    figure, axis = plt.subplots(nrows=2, ncols=1, figsize=(20, 20))

    fig1 = sns.barplot(data=Av, x="Year", y="Min", ax=axis[1])
    fig1.set(ylabel="Avg minimum temparature(in degree):", title="Average Minimum Temp for every year")
    plt.xticks(rotation=45)

    fig2 = sns.barplot(data=required_df, x='Month', y='Min', hue='Year', ax=axis[0])
    fig2.set(ylabel="Minimum temparature(in degree):", title="Minimum monthly Temp for 20 Years(City:"+user_input+")")
    fig2.legend(bbox_to_anchor=(1.03, 1))

    # sns.barplot(data= required_df, x='Month',y='Max',hue='Year', ax=axis[1,0])
    # sns.barplot(data= required_df, x='Month',y='Rain',hue='Year', ax=axis[1,1])
    # figure.tight_layout()
    plt.show()

except:
    if(flag==1):
        print("Enter a valid city name from the list of cities:", places)
    else:
        print("Something is wrong, please enter another city name from list")