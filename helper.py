def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally= medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Bronze'] + medal_tally['Silver']
    return medal_tally
import numpy as np
def country_year_list(df):
    Years = df['Year'].unique().tolist()
    Years.sort()
    Years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return Years, country

def fetch_medal_tally(df,Year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if Year == 'Overall' and country == 'Overall':
         temp_df = medal_df
    if Year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if Year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(Year)]
    if Year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(Year))& (medal_df['region'] == country)]

    if flag == 1 :
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending = True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()
        x['total'] = x['Gold']+x['Bronze']+x['Silver']
    return x
def data_over_time(df,col):
     nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
     return nations_over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport!='Overall':
        temp_df = temp_df[temp_df['Sport']==sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'},inplace=True)
    return x