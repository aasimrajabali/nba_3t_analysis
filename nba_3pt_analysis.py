# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 16:26:02 2019

@author: aasim
"""


import pandas as pd
import plotly.offline as pyo
from plotly.offline import plot
import plotly.graph_objects as pygo

pyo.init_notebook_mode(connected=True)

#--Loading and Prepping the Dataset

overall_data = pd.read_csv("Seasons_stats_complete.csv")

#--Cleaning the Dataset
overall_data = overall_data.fillna(0)
overall_data = overall_data[overall_data.Tm != 'TOT']

#The 3pt was introduced in 1980, so we'll need stats for all years 1980+
overall_data_1980 = overall_data.loc[overall_data['Year'] > 1979]
    
#We only need to grab the columns that we're interested in
overall_data_1980 = overall_data_1980[['Year', '2PA', '3PA', 'FGA']]

#We will compare total 2pt shots vs 3pt shots first
data_1980_sum = overall_data_1980.groupby('Year').sum()
#sanity check
#print(data_1980_sum.head())
total_yrs = data_1980_sum.index

#--VISUALIZATIONS--#

#--SHOT ATTEMPTS--
# To get a comparison and fina a trend, the best way 
# visually would be a bar graph showing both 2pt and 2pt bars.

pt_2 = pygo.Bar(
        x = total_yrs,
        y = data_1980_sum['2PA'],
        name = '2-PT Attempts',
        marker = dict(color="#1b51f2")
)
pt_3 = pygo.Bar(
        x = total_yrs,
        y = data_1980_sum['3PA'],
        name = '3-PT Attempts',
        marker = dict(color="#0b995b")
)

data = [pt_2, pt_3]

layout = pygo.Layout(
            title = 'Total Shot Attempts 1980-2019',
            xaxis = dict(
                    title='Years',
                    titlefont=dict(size=16, color='white'),
                    tickfont=dict(size=14, color='#0080ff')
                    ),
            yaxis = dict(
                    title='Total Attempts',
                    titlefont=dict(size=16, color='white'),
                    tickfont=dict(size=14, color='#0080ff'),
                    showgrid = True, gridwidth=0.2, gridcolor='#D7DBDD'
                    ),
            legend=dict(
                    x = 1,
                    y = 1.0,
                    bgcolor = 'black',
                    bordercolor = 'black'
                    ),
            plot_bgcolor = 'black',
            barmode = 'group',
            bargap = 0.2,
            bargroupgap = 0.1
)

fig = pygo.Figure(data=data, layout=layout)
plot(fig)
fig.show()

#--SHOT PERCENTAGES--
# The same concept for shot attempts applies to percentages.
# However, since there are not % values we can grab from the csv, 
# we'll have to create a formula and make our own.

data_1980_sum['2P%'] = round(data_1980_sum['2PA'] / data_1980_sum['FGA'] * 100, 2)
data_1980_sum['3P%'] = round(data_1980_sum['3PA'] / data_1980_sum['FGA'] * 100, 2)

pt_2_pct = pygo.Bar(
        x = total_yrs,
        y = data_1980_sum['2P%'],
        name = '2-PT%',
        marker = dict(color="#1b51f2")
)
pt_3_pct = pygo.Bar(
        x = total_yrs,
        y = data_1980_sum['3P%'],
        name = '3-PT%',
        marker = dict(color="#0b995b")
)

data = [pt_2_pct, pt_3_pct]

layout = pygo.Layout(
            title = 'Percentages 1980-2019: 2PT vs 3PT',
            xaxis = dict(
                    title='Years',
                    titlefont=dict(size=16, color='white'),
                    tickfont=dict(size=14, color='#0080ff')
                    ),
            yaxis = dict(
                    title='Total Attempts (%)',
                    titlefont=dict(size=16, color='white'),
                    tickfont=dict(size=14, color='#0080ff'),
                    showgrid = True, gridwidth=0.2, gridcolor='#D7DBDD'
                    ),
            legend=dict(
                    x = 1,
                    y = 1.0,
                    bgcolor = 'black',
                    bordercolor = 'black'
                    ),
            plot_bgcolor = 'black',
            barmode = 'group',
            bargap = 0.2,
            bargroupgap = 0.1
)

fig = pygo.Figure(data=data, layout=layout)
plot(fig)
fig.show()

# NARROWING THE DATA: Getting visualizations for stats of an average game
# We can create a new dataframe to simplify/organize our visualization process
# We can also include the player position to make the data even more specific

# The dataset we are using doesn't have columns for average game data,
# so we can create a function that can create our own columns for those datapoints
# The idea behind this is a == DataFrame we're using and b == Column being used

def create_col(a, b):
    a[b + '_G'] = round(a[b] / a['G'], 2)

# Once again, we only grab the columns we're interested in
avg_game_data = overall_data[['Year', 'Pos', 'G', 'MP', '2PA', '3PA', 
                              'ORB', 'DRB', 'TRB', 'PTS', 'USG%']]

# We'll need to filter the data past 1980 once again, but also
# we'll filter out inactive players

avg_game_data = avg_game_data.loc[(avg_game_data['Year'] > 1979) & + \
                                  (avg_game_data['G'] > 24)]

# Using the function we create earlier, we can filter inactive players further 
# by minutes played (in this case, we'll choose 17 min)

create_col(avg_game_data, 'MP')
avg_game_data = avg_game_data.loc[avg_game_data['MP_G'] > 17]

# Find shot attempts per game
create_col(avg_game_data, '2PA') #2PA_G
create_col(avg_game_data, '3PA') #3PA_G

# Including player position
# Syntax follows as att == Attempts followed by the position

att_pg = round(avg_game_data.loc[avg_game_data['Pos'] == 'PG'].groupby('Year').mean(),2)
att_sg = round(avg_game_data.loc[avg_game_data['Pos'] == 'SG'].groupby('Year').mean(),2)
att_sf = round(avg_game_data.loc[avg_game_data['Pos'] == 'SF'].groupby('Year').mean(),2)
att_pf = round(avg_game_data.loc[avg_game_data['Pos'] == 'PF'].groupby('Year').mean(),2)
att_c = round(avg_game_data.loc[avg_game_data['Pos'] == 'C'].groupby('Year').mean(),2)
att_avg = round(avg_game_data.groupby('Year').mean(),2)

att_yrs = att_pg.index

# 2PA PER GAME
# Since we're comparing the attempts of so many positions, it's best to visualize 
# a line graph comparison, and we can include a bar graph of the 
# average attempts per year

p2_pg = pygo.Scatter(x=att_yrs, y=att_pg['2PA_G'], 
                     name='Point Guards', marker=dict(color='red'))
p2_sg = pygo.Scatter(x=att_yrs, y=att_sg['2PA_G'], 
                     name='Shooting Guards', marker=dict(color='orange'))
p2_sf = pygo.Scatter(x=att_yrs, y=att_sf['2PA_G'], 
                     name='Small Forwards', marker=dict(color='violet'))
p2_pf = pygo.Scatter(x=att_yrs, y=att_pf['2PA_G'], 
                     name='Power Forwards', marker=dict(color='green'))
p2_c = pygo.Scatter(x=att_yrs, y=att_c['2PA_G'], 
                     name='Centers', marker=dict(color='blue'))
p2_avg = pygo.Bar(x=att_yrs, y=att_avg['2PA_G'],
                  name='Average', marker=dict(color='lightgray'))

data = [p2_pg,p2_sg,p2_sf,p2_pf,p2_c,p2_avg]
layout = pygo.Layout(
            title='2PA Per Game',
            xaxis=dict(
                    title='Years',
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000')
                    ),
            yaxis=dict(
                    title='2PA per game',
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000'),
                    showgrid=True, gridwidth=0.2, gridcolor = '#D7DBDD'
                    ),
            legend=dict(
                    x=1, y=1.0, bgcolor='black', bordercolor='white'
                    ),
            plot_bgcolor = 'black',
            barmode = 'group',
            bargap = 0.15,
            bargroupgap = 0.1
)
fig = pygo.Figure(data=data, layout=layout)
plot(fig)
fig.show()

# 3PA PER GAME: (same concept as 2PA per game)
p3_pg = pygo.Scatter(x=att_yrs, y=att_pg['3PA_G'], 
                     name='Point Guards', marker=dict(color='red'))
p3_sg = pygo.Scatter(x=att_yrs, y=att_sg['3PA_G'], 
                     name='Shooting Guards', marker=dict(color='orange'))
p3_sf = pygo.Scatter(x=att_yrs, y=att_sf['3PA_G'], 
                     name='Small Forwards', marker=dict(color='violet'))
p3_pf = pygo.Scatter(x=att_yrs, y=att_pf['3PA_G'], 
                     name='Power Forwards', marker=dict(color='green'))
p3_c = pygo.Scatter(x=att_yrs, y=att_c['3PA_G'], 
                     name='Centers', marker=dict(color='blue'))
p3_avg = pygo.Bar(x=att_yrs, y=att_avg['3PA_G'],
                  name='Average', marker=dict(color='lightgray'))

data = [p3_pg,p3_sg,p3_sf,p3_pf,p3_c,p3_avg]
layout = pygo.Layout(
            title='3PA Per Game',
            xaxis=dict(
                    title='Years',
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000')
                    ),
            yaxis=dict(
                    title='3PA per game',
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000'),
                    showgrid=True, gridwidth=0.2, gridcolor = '#D7DBDD'
                    ),
            legend=dict(
                    x=1, y=1.0, bgcolor='black', bordercolor='white'
                    ),
            plot_bgcolor = 'black',
            barmode = 'group',
            bargap = 0.15,
            bargroupgap = 0.1
)
fig = pygo.Figure(data=data, layout=layout)
plot(fig)
fig.show()

# How the 3-Pointer can potentially impact other stats
# Create a new DataFrame to measure stats
stats_pergame = overall_data[['Year', 'Pos', 'G', 'MP', 
                              'ORB', 'DRB', 'TRB', 'PTS', 'USG%']]

#filter the new DataFrame
stats_pergame = stats_pergame.loc[(stats_pergame['Year'] > 1979) & + \
                                  (stats_pergame['G'] > 24)]
create_col(stats_pergame, 'MP')
stats_pergame = stats_pergame.loc[stats_pergame['MP_G'] > 17]

# Create the columns we need to get stats per game
create_col(stats_pergame, 'ORB') #ORB_G
create_col(stats_pergame, 'DRB') #DRB_G
create_col(stats_pergame, 'TRB') #TRB_G
create_col(stats_pergame, 'PTS') #PTS_G

# Including player position
# Syntax follows as st == Stat (since we're getting both reb's and pts)
# followed by the position
st_pg = round(stats_pergame.loc[stats_pergame['Pos'] == 'PG'].groupby('Year').mean(),2)
st_sg = round(stats_pergame.loc[stats_pergame['Pos'] == 'SG'].groupby('Year').mean(),2)
st_sf = round(stats_pergame.loc[stats_pergame['Pos'] == 'SF'].groupby('Year').mean(),2)
st_pf = round(stats_pergame.loc[stats_pergame['Pos'] == 'PF'].groupby('Year').mean(),2)
st_c = round(stats_pergame.loc[stats_pergame['Pos'] == 'C'].groupby('Year').mean(),2)
st_avg = round(stats_pergame.groupby('Year').mean(),2)

st_yrs = st_pg.index


# Correlation between 3-Pointers and Rebounds Analysis:
# RB's PER GAME
orb = pygo.Scatter(x=st_yrs, y=st_avg['ORB_G'], 
                   name='Offensive Rebounds', marker=dict(color='red'))
drb = pygo.Scatter(x=st_yrs, y=st_avg['DRB_G'], 
                   name='Defensive Rebounds', marker=dict(color='blue'))
trb = pygo.Bar(x=st_yrs, y=st_avg['TRB_G'], 
                   name='Rebounds', marker=dict(color='lightgray'))

data=[orb,drb,trb]
layout = pygo.Layout(
        title='Rebounds Per Game',
    	xaxis=dict(
    		title='Years',
    		titlefont=dict(size=16, color='#000000'),
    		tickfont=dict(size=14, color='#000000')
    	),
    	yaxis=dict(
    		title='Rebounds per game',
    		titlefont=dict(size=16, color='#000000'),
    		tickfont=dict(size=14, color='#000000'),
            showgrid=True, gridwidth=0.2, gridcolor='#D7DBDD'
    	),	
    	legend=dict(
    		x=1,
    		y=1.0,
    		bgcolor='black',
    		bordercolor='white'
    	),
        plot_bgcolor='black',
    	barmode='group',
    	bargap=0.15,
    	bargroupgap=0.1
)
 
fig = pygo.Figure(data=data, layout=layout)
plot(fig)
fig.show()

# TRB BY POS

trb_pg = pygo.Scatter(x=st_yrs, y=st_pg['TRB_G'], 
                     name='Point Guards', marker=dict(color='red'))
trb_sg = pygo.Scatter(x=st_yrs, y=st_sg['TRB_G'], 
                     name='Shooting Guards', marker=dict(color='orange'))
trb_sf = pygo.Scatter(x=st_yrs, y=st_sf['TRB_G'], 
                     name='Small Forwards', marker=dict(color='violet'))
trb_pf = pygo.Scatter(x=st_yrs, y=st_pf['TRB_G'], 
                     name='Power Forwards', marker=dict(color='green'))
trb_c = pygo.Scatter(x=st_yrs, y=st_c['TRB_G'], 
                     name='Centers', marker=dict(color='blue'))
trb_avg = pygo.Bar(x=st_yrs, y=st_avg['TRB_G'],
                  name='Average', marker=dict(color='lightgray'))
data = [trb_pg,trb_sg,trb_sf,trb_pf,trb_c,trb_avg]
layout = pygo.Layout(
            title='Total Rebounds Per Game By Position',
            xaxis=dict(
                    title='Years',
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000')
                    ),
            yaxis=dict(
                    title="REB's per game",
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000'),
                    showgrid=True, gridwidth=0.2, gridcolor = '#D7DBDD'
                    ),
            legend=dict(
                    x=1, y=1.0, bgcolor='black', bordercolor='white'
                    ),
            plot_bgcolor = 'black',
            barmode = 'group',
            bargap = 0.15,
            bargroupgap = 0.1
)

fig = pygo.Figure(data=data, layout=layout)
plot(fig)
fig.show()

# DRB BY POS

drb_pg = pygo.Scatter(x=st_yrs, y=st_pg['DRB_G'], 
                     name='Point Guards', marker=dict(color='red'))
drb_sg = pygo.Scatter(x=st_yrs, y=st_sg['DRB_G'], 
                     name='Shooting Guards', marker=dict(color='orange'))
drb_sf = pygo.Scatter(x=st_yrs, y=st_sf['DRB_G'], 
                     name='Small Forwards', marker=dict(color='violet'))
drb_pf = pygo.Scatter(x=st_yrs, y=st_pf['DRB_G'], 
                     name='Power Forwards', marker=dict(color='green'))
drb_c = pygo.Scatter(x=st_yrs, y=st_c['DRB_G'], 
                     name='Centers', marker=dict(color='blue'))
drb_avg = pygo.Bar(x=st_yrs, y=st_avg['DRB_G'],
                  name='Average', marker=dict(color='lightgray'))
data = [drb_pg,drb_sg,drb_sf,drb_pf,drb_c,drb_avg]
layout = pygo.Layout(
            title='Defensive Rebounds Per Game By Position',
            xaxis=dict(
                    title='Years',
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000')
                    ),
            yaxis=dict(
                    title="REB's per game",
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000'),
                    showgrid=True, gridwidth=0.2, gridcolor = '#D7DBDD'
                    ),
            legend=dict(
                    x=1, y=1.0, bgcolor='black', bordercolor='white'
                    ),
            plot_bgcolor = 'black',
            barmode = 'group',
            bargap = 0.15,
            bargroupgap = 0.1
)

fig = pygo.Figure(data=data, layout=layout)
plot(fig)
fig.show()

# ORB BY POS

orb_pg = pygo.Scatter(x=st_yrs, y=st_pg['ORB_G'], 
                     name='Point Guards', marker=dict(color='red'))
orb_sg = pygo.Scatter(x=st_yrs, y=st_sg['ORB_G'], 
                     name='Shooting Guards', marker=dict(color='orange'))
orb_sf = pygo.Scatter(x=st_yrs, y=st_sf['ORB_G'], 
                     name='Small Forwards', marker=dict(color='violet'))
orb_pf = pygo.Scatter(x=st_yrs, y=st_pf['ORB_G'], 
                    name='Power Forwards', marker=dict(color='green'))
orb_c = pygo.Scatter(x=st_yrs, y=st_c['ORB_G'], 
                     name='Centers', marker=dict(color='blue'))
orb_avg = pygo.Bar(x=st_yrs, y=st_avg['ORB_G'],
                  name='Average', marker=dict(color='lightgray'))
data = [orb_pg,orb_sg,orb_sf,orb_pf,orb_c,orb_avg]
layout = pygo.Layout(
            title='Offensive Rebounds Per Game By Position',
            xaxis=dict(
                    title='Years',
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000')
                    ),
            yaxis=dict(
                    title="REB's per game",
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000'),
                    showgrid=True, gridwidth=0.2, gridcolor = '#D7DBDD'
                    ),
            legend=dict(
                    x=1, y=1.0, bgcolor='black', bordercolor='white'
                    ),
            plot_bgcolor = 'black',
            barmode = 'group',
            bargap = 0.15,
            bargroupgap = 0.1
)

fig = pygo.Figure(data=data, layout=layout)
plot(fig)
fig.show()

# Correlation between 3-Pointers and Points Analysis:
# PPG BY POS

pts_pg = pygo.Scatter(x=st_yrs, y=st_pg['PTS_G'], 
                     name='Point Guards', marker=dict(color='red'))
pts_sg = pygo.Scatter(x=st_yrs, y=st_sg['PTS_G'], 
                     name='Shooting Guards', marker=dict(color='orange'))
pts_sf = pygo.Scatter(x=st_yrs, y=st_sf['PTS_G'], 
                     name='Small Forwards', marker=dict(color='violet'))
pts_pf = pygo.Scatter(x=st_yrs, y=st_pf['PTS_G'], 
                    name='Power Forwards', marker=dict(color='green'))
pts_c = pygo.Scatter(x=st_yrs, y=st_c['PTS_G'], 
                     name='Centers', marker=dict(color='blue'))
pts_avg = pygo.Bar(x=st_yrs, y=st_avg['PTS_G'],
                  name='Average', marker=dict(color='lightgray'))
data = [pts_pg,pts_sg,pts_sf,pts_pf,pts_c,pts_avg]
layout = pygo.Layout(
            title='Points Per Game By Position',
            xaxis=dict(
                    title='Years',
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000')
                    ),
            yaxis=dict(
                    title="Points per game",
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000'),
                    showgrid=True, gridwidth=0.2, gridcolor = '#D7DBDD'
                    ),
            legend=dict(
                    x=1, y=1.0, bgcolor='black', bordercolor='white'
                    ),
            plot_bgcolor = 'black',
            barmode = 'group',
            bargap = 0.15,
            bargroupgap = 0.1
)

fig = pygo.Figure(data=data, layout=layout)
plot(fig)
fig.show()

# Correlation between 3-Pointers and Usage Analysis:
# USG% BY POS

usg_pg = pygo.Scatter(x=st_yrs, y=st_pg['USG%'], 
                     name='Point Guards', marker=dict(color='red'))
usg_sg = pygo.Scatter(x=st_yrs, y=st_sg['USG%'], 
                     name='Shooting Guards', marker=dict(color='orange'))
usg_sf = pygo.Scatter(x=st_yrs, y=st_sf['USG%'], 
                     name='Small Forwards', marker=dict(color='violet'))
usg_pf = pygo.Scatter(x=st_yrs, y=st_pf['USG%'], 
                    name='Power Forwards', marker=dict(color='green'))
usg_c = pygo.Scatter(x=st_yrs, y=st_c['USG%'], 
                     name='Centers', marker=dict(color='blue'))
usg_avg = pygo.Bar(x=st_yrs, y=st_avg['USG%'],
                  name='Average', marker=dict(color='lightgray'))
data = [usg_pg,usg_sg,usg_sf,usg_pf,usg_c,usg_avg]
layout = pygo.Layout(
            title='Player Usage Per Game',
            xaxis=dict(
                    title='Years',
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000')
                    ),
            yaxis=dict(
                    title="Usage (%)",
                    titlefont=dict(size=16, color='#000000'),
                    tickfont=dict(size=14, color='#000000'),
                    showgrid=True, gridwidth=0.2, gridcolor = '#D7DBDD'
                    ),
            legend=dict(
                    x=1, y=1.0, bgcolor='black', bordercolor='white'
                    ),
            plot_bgcolor = 'black',
            barmode = 'group',
            bargap = 0.15,
            bargroupgap = 0.1
)

fig = pygo.Figure(data=data, layout=layout)
plot(fig)
fig.show()