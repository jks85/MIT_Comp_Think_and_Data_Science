## scripts for cleaning data from basketball reference
## pulling tables from bref for advanced team offense stats
## using pandas to scrape html tables

import pandas
import numpy
import lxml

#######################

# testing scraping and cleaning 2024-2025 advanced stats
# bref uses html tables
# note bref_url_25 is for 2024-2025 season

#bref link
bref_url_25 = 'https://www.basketball-reference.com/leagues/NBA_2025.html'

# grab html tables
# nba_25 = pandas.read_html(bref_url_25)
# 11th table in list is desired table "Advanced Stats"
# not sure why it is 11th in list as it is 8th on the page...
# team_adv_25 = nba_25[10]

nba_25 = pandas.read_html(bref_url_25, match = 'ORtg')
team_adv_25 = nba_25[0]
# will use match argument instead in function
# desired table has 'ORtg' as a column and is the only table with that column variable

print('print table')
print(team_adv_25)
# df headers are messy b/c bref has two headers

col_name_clean = []     # empty list to hold columns
for (x,y) in team_adv_25.columns:
    col_name_clean.append(y)

team_adv_25.columns = col_name_clean # assign new column names

# select desired columns
# analyzing 3pt rate and offensive rating
print('reprint')
print(team_adv_25)

#team_adv_25.loc[:,['Team','ORtg','3PAr']]
#####################

def create_url(year:int) -> str:
    '''
    Creates a url  to basketball reference season team stats for a particular year
    e.g. 'https://www.basketball-reference.com/leagues/NBA_2025.html'

    Note that 'year' corresponds to the year the season ends.
    For example, year = 2025 is for the 2024-2025 season.

    :param year: year for desired team stats
    :return: string url to basketball reference stats for a particular year
    '''
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '.html'
    return url



def get_team_adv_stats(year:int):
    '''
    Returns a pandas data frame of advanced team stats for 'year'.
    Data frame includes the league average. The function creates an
    additional column in the data frame containing the year.

    Note that 'year' corresponds to the year the season ends.
    For example, year = 2025 is for the 2024-2025 season.

    :param year: season (ending year)
    :return: pandas data frame
    '''
    url = create_url(year)  # create url for desired season

    # select table(s) containing ORtg (offensive rating). In this case there is only one table
    table_list = pandas.read_html(url, match = 'ORtg') # list of html tables on b-ref website
    # team_adv = table_list[10] # team advanced stats table is the 11th table
    team_adv = table_list[0] # team advanced stats table is the 11th table

    # clean column names of df
    col_name_clean = []  # empty list to hold columns
    for (x, y) in team_adv.columns:
        col_name_clean.append(y)

    team_adv.columns = col_name_clean  # assign new column names
    num_rows = team_adv.shape[0]
    year_list = [year for i in range(num_rows)] # list containing year as tag
    team_adv['Year'] = year_list       # add column containing year

    return team_adv       # return data frame of advanced stats for year

########

## testing get_team_adv_stats()

# test_25 = get_team_adv_stats(2025) # 2025 data
# #print(test_25.head)
# #print(test_25.loc[:,['Year','Team','ORtg','3PAr']])
#
# test_24 = get_team_adv_stats(2024) # 2024 data
# #print(test_24.loc[:,['Year','Team','ORtg','3PAr']])
#
# bind_dfs = pandas.concat([test_25,test_24], ignore_index = True)
# #print(bind_dfs)

#####

### get data going back to 2012

# seasons = [i for i in reversed(range(2012,2026))]
#
# advanced_stats_seasons = [get_team_adv_stats(i) for i in seasons]
#
# print(len(advanced_stats_seasons))
#
# all_seasons_df = pandas.concat(advanced_stats_seasons)
# print(all_seasons_df.shape)

####

def get_adv_stats_multi(start_year:int, end_year:int):
    '''
    Creates data frames of advanced stats from basketball reference
    Recall that the year is the year that a season ends. For example,
    year = 2025 is for the 2024-2025 season.

    :param start_year: first season
    :param end_year: last season
    :return: pandas data frame containing advanced team stats
    '''

    seasons = [year for year in reversed(range(start_year, end_year +1))] # list of seasons
    advanced_stats_seasons = [get_team_adv_stats(season) for season in seasons] # list of data frames
    multi_season_df = pandas.concat(advanced_stats_seasons) # bind dfs by row

    return multi_season_df


### DO NOT RUN THIS. BREF rate limits requests (10 per minute)

# print("testing get_adv_stats_multi")
# test_multi = get_adv_stats_multi(2012,2025)
# print(test_multi.shape)

