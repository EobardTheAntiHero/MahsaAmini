import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import seaborn as sns
import praw
from datetime import datetime

#Project Description
st.sidebar.header("How Reddit Reacted to the Murder of Mahsa Amini")
st.sidebar.markdown("""Dedicated to the memory Mahsa Amini, who was brutally murdered by the morality police on September 16th, and started a fire within all of us.""")
st.sidebar.markdown("""A small project by Payam Saeedi""")

st.subheader("Hover over the circles to see date and number of posts")

#Reddit Authentication
reddit = praw.Reddit(client_id='VBYqU0EAeHAP_Q', client_secret='ANbybH8lpy9kYJ8eYD_zeumUSH5KHQ', user_agent='Starbucks Analysis')

#Reading the Data from Reddit
alls = reddit.subreddit("all")

#Reading the Data on Mahsa Amini
posts = []
for submission in alls.search("Mahsa Amini" , limit = 1000):
    posts.append([submission.title, submission.score, submission.id, submission.url, submission.num_comments, submission.selftext, submission.created])
mahsa = pd.DataFrame(posts,columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created'])
#Reading the Data on Iran
posts1 = []
for submission in alls.search("Iran" , limit = 1000):
    posts1.append([submission.title, submission.score, submission.id, submission.url, submission.num_comments, submission.selftext, submission.created])
Iran = pd.DataFrame(posts1,columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created'])


#Correcting Date Format
mahsa['Date'] = pd.to_datetime(mahsa['created'], utc = True, unit = 's').dt.date
mahsa['Date'] = pd.to_datetime(mahsa['Date'])

Iran['Date'] = pd.to_datetime(Iran['created'], utc = True, unit = 's').dt.date
Iran['Date'] = pd.to_datetime(Iran['Date'])

#Prepating Dataframe for initial visualization
df = mahsa.groupby('Date').count()[['title']]
df = df.rename(columns = {'title':'Number of Posts'})
df = df.reset_index()

df1 = Iran.groupby('Date').count()[['title']]
df1 = df1.rename(columns = {'title':'Number of Posts'})
df1 = df1.reset_index()

final_date = pd.merge(df,df1, on = 'Date')
final_date = final_date.rename(columns = {'Number of Posts_x':'Mahsa Amini','Number of Posts_y':'Iran'})
final_date = final_date.melt('Date', var_name='Category', value_name='Number of Posts')

#Creating Visualization 1
circles = alt.Chart(df).mark_point(size = 100).encode(
    alt.X('monthdate(Date):O', axis = alt.Axis(title = 'Date',grid = False, labelAngle=0, labelFontSize=9, tickSize=0, labelPadding=10, labelColor = 'gray')),
    alt.Y('Number of Posts:Q', axis= None),
    # The highlight will be set on the result of a conditional statement
    color=alt.value('crimson'),
    tooltip=['Date','Number of Posts']
    
).properties(title = 'Mentions of Mahsa Amini on Reddit', width =800, height = 400)

lines = alt.Chart(df).mark_line().encode(
    alt.X('monthdate(Date):O', axis = alt.Axis(title = 'Date',labels = False, grid = False, labelAngle=0, labelFontSize=9, tickSize=0, labelPadding=10, labelColor = 'crimson')),
    alt.Y('Number of Posts:Q', axis=None),
    # The highlight will be set on the result of a conditional statement
    color=alt.value('crimson'),
    tooltip=['Date','Number of Posts']
    
).properties(title ="Mentions of Mahsa Amini on Reddit", width =800, height = 400)


callout = alt.Chart(df[df['Date'] == '2022-09-16']).mark_point(
    color='crimson', size=300, tooltip="Mahsa was killed by the morality police").encode(
    x='monthdate(Date):O',
    y='Number of Posts:Q')

#Creating Visualization 2
IR = alt.Chart(final_date).mark_line().encode(
    alt.X('monthdate(Date):O', axis = alt.Axis(title = 'Date',labels = True, grid = False, labelAngle=0, labelFontSize=9, tickSize=0, labelPadding=10, labelColor = 'gray')),
    alt.Y('Number of Posts:Q', axis= None),
    # The highlight will be set on the result of a conditional statement
    color=alt.Color('Category:N', scale=alt.Scale(domain=['Mahsa Amini','Iran'], range=['crimson','grey']), legend = alt.Legend(title = None)),
    tooltip=['Date','Number of Posts']
    
).properties(title ="One Mahsa Amini, One Iran", width =800, height = 200)

#Displating Visualizations

st.altair_chart((circles+lines+callout).configure_view(stroke = 'transparent', strokeOpacity = 0).configure_title(anchor='start', color = 'crimson'))

st.subheader("Since her murder on Sept. 16, mentions of Mahsa and Iran on Reddit have followed a similar pattern")
st.altair_chart((IR).configure_view(stroke = 'transparent',strokeWidth=0, strokeOpacity = 0).configure_title(anchor='start', color = 'grey').configure_axisX(titleAlign='left'))


