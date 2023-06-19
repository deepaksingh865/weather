import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import sys

places=['Aberporth', 'Armagh', 'Ballypatrick', 'Bradford', 'Braemar', 'Camborne', 'Cambridge', 'Cardiff','Chivenor',
        'Cwmystwyth', 'Dunstaffnage', 'Durham', 'Eastbourne', 'Eskdalemuir', 'Heathrow', 'Hurn', 'Lerwick','Leuchars',
        'Manston', 'Nairn', 'NewtonRigg', 'Oxford', 'Paisley', 'Ringway', 'RossonWye', 'Shawbury', 'Sheffield',
        'Southampton', 'Stornoway', 'SuttonBonington', 'Tiree', 'Valley', 'Waddington', 'WickAirport','Yeovilton']
flag=0
try:
    user_input= sys.argv[1]
    if(user_input not in places):
        flag=1
    location=user_input.lower()
    r = requests.get('https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{0}data.txt'.format(location))
    raw_data = r.text
    file_data=StringIO(raw_data)

    df=pd.read_fwf(file_data,skiprows=6)
    df.columns=["Year","Month","Max","Min","AF","Rain","Sunhour"]
    df.replace(to_replace='---',value=0,inplace=True)

    last_year=df['Year'].max()
    required_df=df[df['Year'].between(last_year-21, last_year-1)]
    required_df.reset_index(drop=True,inplace=True)
    required_df=required_df.astype(float)
    required_df['Year']=required_df['Year'].astype(int)
    required_df['Month']=required_df['Month'].astype(int)

    av=required_df.groupby('Year').mean()
    av.reset_index(level=0,inplace=True)

    # **************Plotting*********************
    figure, axis = plt.subplots(nrows=2, ncols=2, figsize=(20, 20))

    fig1 = sns.barplot(data=av, x="Year", y="Min", ax=axis[0,1])
    fig1.set(ylabel="Avg minimum temperature(in degree):", title="Average Minimum Temp for every year")
    plt.xticks(rotation=45)

    fig2 = sns.barplot(data=required_df, x='Month', y='Min', hue='Year', ax=axis[0,0])
    fig2.set(ylabel="Minimum temperature(in degree):", title="Minimum monthly Temp for 20 Years(City:"+user_input+")")
    fig2.legend(bbox_to_anchor=(-1, 0.1, 0.1, 0.1))

    fig3=sns.barplot(data= required_df, x='Month',y='Max',hue='Year', ax=axis[1,0])
    fig3.set(ylabel="Max temperature(in degree):",title="Maximum Temp for 20 Years")
    fig3.legend(bbox_to_anchor=(-1, 0.1, 0.1, 0.1))

    fig4=sns.barplot(data= required_df, x='Month',y='Rain',hue='Year', ax=axis[1,1])
    fig4.set(ylabel="Rain(in mm):", title="Rain for 20 Years")
    fig4.legend(bbox_to_anchor=(1.1, 2, 0.1, 0.1))
    #figure.tight_layout()
    plt.show()

except:
    if(flag==1):
        print("Enter a valid city name from the list of cities:", places)
    else:
        print("Something is wrong, please enter another city name from list")