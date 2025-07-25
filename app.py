import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
from helper import medal_tally
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df,region_df)
st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Telly','Overall Analysis')
)


if user_menu == 'Medal Telly':
    st.sidebar.header('Medal Tally')
    Years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year',Years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title('Overall Tally')
    if selected_country != 'Overall' and selected_year == 'Overall':
        st.title(selected_country + ' Overall Performance' )
    if selected_country == 'Overall' and selected_year != 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_country != 'Overall' and selected_year != 'Overall':
        st.title(selected_country +' performance in ' +str(selected_year) + ' Olympics')
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events ')
        st.title(events )
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Year", y="count")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Year", y="count")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Year", y="count")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title('No. of Events over time(Every Sport)')
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title('Most successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport )
    st.table(x)
