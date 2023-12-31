# Import required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import scipy

#First we need to scrape the attraction list (only rides)
url_attractions = "https://touringplans.com/disneyland/attractions" 
response_attractions = requests.get(url_attractions)
soup_attractions = BeautifulSoup(response_attractions.text, "html.parser")
division_attractions = soup_attractions.find_all("div", {"class": "table-attraction"})
attractions = []
for attraction in division_attractions:
    attractions.append(attraction.find('a', href=True)['href'])

#Edit attractions so names are all lowercase
attractions_lower = []
for ride in attractions:
    attractions_lower.append(ride.lower())

#Edit attractions so spaces are replaced with -
attractions_simplified =[]
for ride in attractions_lower:
    attractions_simplified.append(ride.replace(' ','-'))

#Shows are included in attraction list, but they won't be used in this analysis
#A list of shows is created
shows = ["the-bootstrappers", "dapper-dans", "disney-gallery", "disneyland-band-at-main-street,-u.s.a.",
          "the-disneyland-story-presenting-great-moments-with-mr.-lincoln", "droid-depot", "walt-disney's-enchanted-tiki-room", "fantasmic!", "flag-retreat-ceremony", "frontierland-shootin'-exposition", '"it\'s-a-small-world"-holiday-lighting', "jambalaya-jazz", "main-street-cinema", "mickey's-house-and-meet-mickey", 
          "mickey's-mix-magic", "minnie's-house", "savi's-workshop", "sleeping-beauty-castle-walkthrough", "star-wars-launch-bay", "storytelling-at-royal-theatre"]

#Shows are removed from attraction list
for show in shows:
    attractions_simplified.remove(show)
attractions_rides_only = attractions_simplified

#Capacity (wait time per 1000 people) is web scraped using a for loop
capacity = []
for ride in attractions:

    url = "https://touringplans.com" + ride
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    division = soup.find("div", {"class": "report_card touring-info"})
    try: 
        capacity.append(division.find_all("td")[3].text)
    except AttributeError: 
        capacity.append('0')

#The wait time (on a crowd level 10 day) is also extracted using a loop function
wait_time= []
ten_crowd_wait = []
for ride in attractions: 
    url = "https://touringplans.com/" + ride
    response = requests.get(url)
    try: 
        soup = BeautifulSoup(response.text, "html.parser")
        division = soup.find("div", {"style": "margin-top: 10px;"})
        wait_time = str(division.find("img")['src'])
        index_start = wait_time.find(':')
        index_end = wait_time.find('|')
        only_times = wait_time[index_start+1:index_end]
        times_deliminated = only_times.split(',')
        ten_crowd_wait.append(times_deliminated[-1])
    except AttributeError: 
        ten_crowd_wait.append('0')

#The data is collected into a Pandas DataFrame
dict = {'Attraction': attractions, 'Capacity': capacity, 'Wait': ten_crowd_wait}
frame = pd.DataFrame(data = dict)

#The dataframe is exported to Desktop as a csv file for easy access
frame.to_csv('/Users/zak/Desktop/Data Projects/full_attractionsDL.csv')

#The same process was applied for attractions in California Adventure (Disneyland's sister park)

#The csv files are read into Python as Pandas dataframes
dl = pd.read_csv('/Users/zak/Desktop/Data Projects/full_attractionsDL.csv')
dl['Attraction'] = dl['Attraction'].str[24:]
ca = pd.read_csv('/Users/zak/Desktop/Data Projects/full_attractionsCA.csv')
ca['Attraction'] = ca['Attraction'].str[41:]

#The dataframes are joined together
attractions = dl.merge(ca, how = 'outer')

#Attractions without capacity values are eliminated from analysis
attractions = attractions.loc[attractions['Capacity'] != '0']
attractions['Capacity'] = attractions['Capacity'].str[:-8].astype(float)

#The number of people in line is calculated as a new column
attractions['People_in_line'] = attractions['Wait']/attractions['Capacity']*100

#The dataframe is sorted based on the number of people waiting for each attraction
sorted = (attractions.sort_values(by = 'People_in_line', ascending = True))

#Duplicate values are dropped from a copy of the dataframe "grouped"
first_duplicate = sorted[sorted.duplicated(['Wait', 'People_in_line'], keep = 'first')]
only_one_duplicate = first_duplicate.drop_duplicates(['Wait', 'People_in_line'], keep = 'last')
grouped = only_one_duplicate.copy()

#For loops are used to append the names of duplicated wait times and people in line so that the graphs don't have multiple points at the same spots
duplicate_list = str()
copy_list = list()
dropped = sorted.copy()
ride_to_drop = list()

for index1, attract in grouped.iterrows():
    duplicate_list = attract['Attraction']
    for index2, ride in sorted.iterrows():
        if ((ride['Wait'] == attract['Wait']) & (ride['People_in_line'] == attract['People_in_line']) & (ride['Attraction'] != attract['Attraction'])):
            duplicate_list = duplicate_list + '/' + ride['Attraction']
            ride_to_drop.append(ride['Attraction'])
        if index2 == sorted.index[-1]:
            # copy_list.append(duplicate_list)
            sorted['Attraction'].loc[sorted['Attraction'] == attract['Attraction']]= duplicate_list

df_no_matching_values = sorted[~sorted['Attraction'].isin(ride_to_drop)]

#The new grouped and sorted dataframe is renamed "cleaned_data"
cleaned_data = df_no_matching_values

people = cleaned_data['People_in_line']
wait = cleaned_data['Wait']
rides = cleaned_data['Attraction']

#A regression plot is created and the slope and intercept are extracted
p = sns.regplot(data = cleaned_data, x = people, y = wait)
slope, intercept, r, p, sterr = scipy.stats.linregress(x=p.get_lines()[0].get_xdata(), y=p.get_lines()[0].get_ydata())
print(intercept, slope)

#A new column is created where if the data point lies above the regression line it is labeled as 'high' (below the regression line is labeled as 'low')
for index, ride in cleaned_data.iterrows(): 
    if (ride['Wait'] < intercept + slope*ride['People_in_line']):
        cleaned_data.loc[index, 'Cap']= 'high'
    else: cleaned_data.loc[index, 'Cap'] = 'low'

#A practice figure is created to help visualize the relationship between number of people in line and wait time
plt.figure(1)
sns.regplot(data = cleaned_data, x = people, y = wait)
for ride in rides:
    plt.text(cleaned_data[rides == ride]['People_in_line']+10, cleaned_data[rides == ride]['Wait'], ride, horizontalalignment='left', rotation = 0, fontsize='6', color='black', weight='semibold')
plt.xlabel('Guests in Line')
plt.ylabel('Wait Time (min)')
plt.show()

#This graph will have to be adjusted as it is hard to read

#The orginal graph will be separated into three graphs to make visualization easier
plt.figure(2)
graph0 = sns.lmplot(data = cleaned_data, x = 'People_in_line', y = 'Wait', hue = 'Cap', fit_reg=False, legend = False)
sns.regplot(data = cleaned_data, x = people, y = wait, ax=graph0.axes[0, 0], scatter=False)
for ride in rides.iloc[0:16]:
    plt.text(cleaned_data[rides == ride]['People_in_line']+5, cleaned_data[rides == ride]['Wait'], ride, horizontalalignment='left', rotation = 0, fontsize='6', color='black', weight='semibold')
sns.despine(right = True)
plt.xlabel('Guests in Line')
plt.ylabel('Wait Time (min)')
plt.title('Attractions with Lowest Demand')
plt.xlim(100, 325)
plt.ylim(5, 45)
plt.show()


plt.figure(3)
graph1 = sns.lmplot(data = cleaned_data, x = 'People_in_line', y = 'Wait', hue = 'Cap', fit_reg=False, legend = False)
sns.regplot(data = cleaned_data, x = people, y = wait, ax=graph1.axes[0, 0], scatter=False)
for ride in rides.iloc[16:28]:
    plt.text(cleaned_data[rides == ride]['People_in_line']+10, cleaned_data[rides == ride]['Wait'], ride, horizontalalignment='left', rotation = 0, fontsize='6', color='black', weight='semibold')
sns.despine(right = True)
plt.xlabel('Guests in Line')
plt.ylabel('Wait Time (min)')
plt.title('Attractions with Medium Demand')
plt.xlim(325,1000)
plt.ylim(15, 70)
plt.show()


plt.figure(4)
graph2 = sns.lmplot(data = cleaned_data, x = 'People_in_line', y = 'Wait', hue = 'Cap', fit_reg=False, legend = False)
sns.regplot(data = cleaned_data, x = people, y = wait, ax=graph2.axes[0, 0], scatter=False)
for ride in rides.iloc[28:32]:
    plt.text(cleaned_data[rides == ride]['People_in_line']+10, cleaned_data[rides == ride]['Wait'], ride, horizontalalignment='left', rotation = 0, fontsize='6', color='black', weight='semibold')
for ride in rides.iloc[32:]:
    plt.text(cleaned_data[rides == ride]['People_in_line']+10, cleaned_data[rides == ride]['Wait']-2, ride, horizontalalignment='left', rotation = 0, fontsize='6', color='black', weight='semibold')sns.despine(right = True)
plt.xlabel('Guests in Line')
plt.ylabel('Wait Time (min)')
plt.title('Attractions with Highest Demand')
plt.xlim(left = 1000)
plt.ylim(bottom = 30)
plt.show()

#The attractions are then plotted in a bar graph of how they might be ranked in the case of people in line
cleaned_data = cleaned_data.sort_values(by = 'People_in_line', ascending = False)
plt.figure(5, figsize = (12,7))
sns.barplot(y = cleaned_data[:10]['Attraction'], x = cleaned_data[:10]['People_in_line'], hue = cleaned_data[:10]['Wait'], dodge = False, color = 'darkblue')
plt.title('Top 10 Disneyland Resort Attractions Ranked by Guests in Queue')
plt.xlabel('Guests in Line')
plt.legend(title = 'Wait Time (min)')
plt.show()

#A barplot is used to rank the top 10 attractions based on wait time
by_wait = (sorted.sort_values(by = 'Wait', ascending= False))

plt.figure(6, figsize = (12,7))
sns.barplot(y = by_wait[:10]['Attraction'], x = by_wait[:10]['People_in_line'], hue = by_wait[:10]['Wait'], dodge = False, color = 'darkblue')
plt.title('Top 10 Disneyland Resort Attractions Ranked by Wait Time')
plt.xlabel('Guests in Line')
plt.legend(title = 'Wait Time (min)')
plt.show()

