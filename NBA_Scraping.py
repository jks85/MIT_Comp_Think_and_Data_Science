## scripts for cleaning data from basketball reference
## pulling tables from bref for advanced team offense stats
## using BeautifulSoup to scrape html tables
## Using lxml parser

import pandas
import lxml
from bs4 import BeautifulSoup
import requests
import re

# testing scraping and cleaning 2024-2025 advanced stats
# bref uses html tables
# note bref_url_25 is for 2024-2025 season

#bref link
bref_url_25 = 'https://www.basketball-reference.com/leagues/NBA_2025.html'



######## helper functions

def get_html_req(bref_url):
     '''
     Takes the given url and uses the requests library to extract
     the site as an html tree. Returns the site in html doc form.


     :param bref_url: url to basketball-reference.com
     :return: html text tree from website
     '''

     html_data = requests.get(bref_url).text
     return html_data

def get_html_tree(html_obj):
     '''

     :param html_obj: an html doc from html_req()
     :return: a BeautifulSoup object representing an html tree
     '''

     soup = BeautifulSoup(html_obj, 'lxml')
     return soup

def bref_html(bref_url):
     '''
     Takes a link to basketball-reference.com and returns a parsed
     BeautifulSoup html webpage object to be used for scraping.

     This function is a wrapper for get_html_req() and get_html_tree().

     :param bref_url:
     :return: BeautifulSoup object corresponding to an html webpage
     '''

     # make and request and parse html tree
     html_data = get_html_req(bref_url)
     html_tree = get_html_tree(html_data)

     return html_tree

def scrapeTables(bref_url):
     '''
     Converts url into a BeautifulSoup html tree and return a results set
     of html tables within the tree.

     This is a wrapper for bref_html

     :param bref_url: link to a basketball-reference.com url
     :return: a BeautifulSoup results set containing all tables within the url
     '''

     # get html tree for website
     html_tree = bref_html(bref_url)

     # get table(s) on html page and return a message if no table is found
     try:
         bref_tables = html_tree.find_all(name = "table")
     except:
          try:
               bref_tables = html_tree.find(name = "table")
          except:
               raise ValueError('No html tables found on page.')

     return bref_tables



def getTableHeaders(bref_thead):
     '''
     Takes html strings enclosed in thead tags (e.g. <thead>...</thead>) and
     finds header names for html table. Note that this code is formed using the html
     structure from certain tables on basketball-reference and will not work
     on other sites

     Note: If there are multiple header rows, the header row closest to the table
     data (e.g. highest index) is taken as the header row.

     Returns a list of strings that can be set as column names for a table

     :param bref_thead: a BeautifulSoup object created with thead tags
     :return: list of strings to serve as column headers
     '''

     # get header rows and choose last row
     header_rows = bref_thead.find_all(name = "tr")
     header_row = header_rows[-1]

     # get headers
     header_row = header_row.find_all(name = "th")
     headers = [header.text for header in header_row]

     return headers


def tbody2df(bref_tbody):
     '''
     Takes html strings enclosed in tbody tags (e.g. <tbody>...</tbody>) and
     constructs and html table. Note that this code is formed using the html
     structure from certain tables on basketball-reference and will not work
     on other sites

     Returns a data frame-- with no columns names

     :param bref_tbody: a BeautifulSoup object created with tbody tags
     :return: html table as a pandas data frame w/o column names
     '''

     # get table rows
     df_rows = []  # list of lists that will hold df rows
     table_row_list = bref_tbody.find_all(name ="tr")
     for row in table_row_list:
          cell_data = []
          row_cells = row.find_all(name = ["th","td"])   # get header or cell tags in row
          cell_data = [cell.text for cell in row_cells]  # create list of text in row
          df_rows.append(cell_data)

     temp_df = pandas.DataFrame(df_rows)
     return temp_df


def table2df(bref_table):
     '''
     Takes a BeautifulSoup html object from Basketball-Reference.com corresponding to
     a *single* html table and scrapes the object to create a pandas data frame from
     the table. Uses headers within the html tree to name columns. The table should be
     enclosed in a single set of <table>...</table> tags.

     Note that this code is formed using the html table structure from certain tables on
     basketball-reference and may not work on other sites.


     :param bref_soup: a BeautifulSoup html object
     :return: a pandas data frame
     '''

     # get thead and tbody tags. use find() not find_all since this is assumed to be a single table
     bref_thead = bref_table.find(name="thead")
     bref_tbody = bref_table.find(name="tbody")

     # get column names and data frame
     df_cols = getTableHeaders(bref_thead)
     bref_df = tbody2df(bref_tbody)
     bref_df.columns = df_cols

     return bref_df

##### END HELPERS

#################################3
####################################

##### MAIN FUNCTIONS

def getTables(bref_url):
     '''
     Takes a url to basketball-reference.com and constructs a pandas
     dataframe for each html table.

     This function is a wrapper for various functions in this library.

     :param bref_url: url to basketball-reference.com
     :return: list containing data frames made from html tables on website
     '''

     # scrape html tables from url
     bref_tables = scrapeTables(bref_url)

     # create list of data frames from html tables
     df_list = []
     for table in bref_tables:
          df_list.append(table2df(table))

     return df_list

def findHeader(string, df_list):
     '''
     Checks list of data frames to determine whether  the table
     headers contain a particular string. Returns a list of data
     frames whose column headers. If a header is contained as a
     substring then the data frame is returned. Note, the
     string is *NOT* case-sensitive.

     :param string:
     :return: integer index of table in list of data frames
     '''

     # convert string to lower case
     string_lower = string.lower()

     # list to hold target data frames
     target_df_list = []

     # iterate over list of dfs and check headers
     for index,df in enumerate(df_list):

          # make column headers lowercase and check for string
          temp_col = df.columns[:]

          # add df to list if string is in any column header
          col_hd_low = [header.lower() for header in temp_col]
          if string_lower in col_hd_low:
               target_df_list.append(df_list[index])

     if len(target_df_list) == 0:
          raise ValueError('No data frame found')
     else:
          return target_df_list

test_tables = getTables(bref_url_25)

test_dubs_table = getTables("https://www.basketball-reference.com/teams/GSW/2025.html")
print(len(test_dubs_table))

# for i in range(len(test_dubs_table)):
#      print(test_dubs_table[i])


# print('testing getTables. num tables:',len(test_tables))
# print(test_tables[4])

# check for tables containing ortg
# ortg_dfs = findHeader('Ortg', test_tables)
# print('num tables with "ortg": ',len(ortg_dfs))
# print('first ortg df:',ortg_dfs[0])

# test_tables = scrapeTables(bref_url_25)
# print('testing getTables. num tables:',len(test_tables))
# df_list = []
# for table in test_tables:
#      df_list.append(table2df(table))
#
# print(df_list[10])

## other functions?

# 3) function that checks if a table contains a certain header?

# maybe make a wrapper combining functions 1 and 2?


## testing tbody2df
# print('testing tbody2df....')
# print(tbody2df(bref_tbody[10]))

# testing getTable()
# print('testing getTable....')
# print(table2df(bref_table[10]))
# print(table2df(bref_table[0]))
#
# has_ortg = "ORtg" in table2df(bref_table[10]).columns

# print('table header contains "ORtg"?', has_ortg)

##################
# not using the header function below as we can scrape tags directly using <thead> and <th>
# however writing this function was useful for helping me learn to scrape tag attributes
# specifically the 'data-stat' tag contains information equivalent to some header names

# Note: must use regular expressions to search for these kinds of attributes. they cannot be
# searched using strings

def get_tbody_headers(bref_tbody):
     '''
     Pulls header names for columns from the attribute 'data-stat' in
     bref tables. Function will not work if attribute does not exist

     :param bref_tbody: a BeautifulSoup object created with tbody tags
     :return: list containing headers names
     '''

     # Get data-stat attribute in all tbody tags to find headers
     table_header_list = bref_tbody.find_all(attrs={"data-stat": re.compile('^[a-zA-Z]')})

     # get unique headers
     headers = []
     # note these are not the exact table headers. the tag attribute is slightly different from the column name
     # dummy headers exist for blank columns. these can repeat but other headers should be unique
     for tag in table_header_list:
          header = tag['data-stat']
          if header not in headers or header == 'DUMMY':
               headers.append(header)
          elif header in headers:
               break

     return headers

# test_headers10 = get_tbody_headers(bref_tbody[10])
# print('testing headers table 10:',test_headers10)


# checking if a table has the offensive rating tag attribute "off_rtg"


######################### testing code

# get html data from url
# bref_data = requests.get(bref_url_25).text





# create parsing object
# bref_soup = BeautifulSoup(bref_data,'lxml')

# parsing using beautiful soup
# bref_table = bref_soup.find_all(name = "table")
# bref_thead = bref_soup.find_all(name = "thead")
# bref_tbody = bref_soup.find_all(name = "tbody")
# print('num tables:',len(bref_tbody))
# print('num thead:',len(bref_tbody))
# print('num tbody:',len(bref_tbody))

# parsing table 11

# print(bref_tbody[10])
#print(bref_tables[0])

# make tags with header names
# data-stat attribute contains a string corresponding to column header
# extract using a regular expression
# print(bref_tbody[10].find_all(attrs={"data-stat":re.compile('^[a-zA-Z]')})[0]['data-stat'])
# table_10_header_list = bref_tbody[10].find_all(attrs={"data-stat":re.compile('^[a-zA-Z]')})


# testing2 = pandas.read_html("https://www.basketball-reference.com/teams/GSW/2025.html")
# print(len(testing2))

response = requests.get('https://www.basketball-reference.com/teams/GSW/2025.html')

soup = BeautifulSoup(response.text, 'html.parser')
comments = soup.find_all(string=lambda text: isinstance(text, Comment))

tables = []
for each in comments:
    if 'table' in each:
        try:
            tables.append(pd.read_html(each)[0])
        except:
            continue

print(tables[-1].loc[1:])