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

print('attractions done')
print(attractions)

attractions_lower = []
for ride in attractions:
    attractions_lower.append(ride.lower())

attractions_simplified =[]
for ride in attractions_lower:
    attractions_simplified.append(ride.replace(' ','-'))


shows = ["the-bootstrappers", "dapper-dans", "disney-gallery", "disneyland-band-at-main-street,-u.s.a.",
          "the-disneyland-story-presenting-great-moments-with-mr.-lincoln", "droid-depot", "walt-disney's-enchanted-tiki-room", "fantasmic!", "flag-retreat-ceremony", "frontierland-shootin'-exposition", '"it\'s-a-small-world"-holiday-lighting', "jambalaya-jazz", "main-street-cinema", "mickey's-house-and-meet-mickey", 
          "mickey's-mix-magic", "minnie's-house", "savi's-workshop", "sleeping-beauty-castle-walkthrough", "star-wars-launch-bay", "storytelling-at-royal-theatre"]


for show in shows:
    attractions_simplified.remove(show)
attractions_rides_only = attractions_simplified
print(attractions_rides_only)


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
print('capacity done')



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
print('wait_done')

dict = {'Attraction': attractions, 'Capacity': capacity, 'Wait': ten_crowd_wait}
frame = pd.DataFrame(data = dict)
# frame.to_csv('/Users/zak/Desktop/full_attractions.csv')


dl = pd.read_csv('/Users/zak/Desktop/Data Projects/full_attractions.csv')
dl['Attraction'] = dl['Attraction'].str[24:]
ca = pd.read_csv('/Users/zak/Desktop/Data Projects/full_attractionsCA.csv')
ca['Attraction'] = ca['Attraction'].str[41:]
attractions = dl.merge(ca, how = 'outer')
attractions = attractions.loc[attractions['Capacity'] != '0']
attractions['Capacity'] = attractions['Capacity'].str[:-8].astype(float)
attractions['People_in_line'] = attractions['Wait']/attractions['Capacity']*100
sorted = (attractions.sort_values(by = 'People_in_line', ascending = True))
# plt.scatter(sorted['People_in_line'], sorted['Wait'])
# plt.xlabel('Number of People in Line')
# plt.ylabel('Wait Time')
# plt.show()

people = sorted['People_in_line']
wait = sorted['Wait']
rides = sorted['Attraction']

first_duplicate = sorted[sorted.duplicated(['Wait', 'People_in_line'], keep = 'first')]

only_one_duplicate = first_duplicate.drop_duplicates(['Wait', 'People_in_line'], keep = 'last')

grouped = only_one_duplicate.copy()

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

sorted = df_no_matching_values

people = sorted['People_in_line']
wait = sorted['Wait']
rides = sorted['Attraction']

p = sns.regplot(data = sorted, x = people, y = wait)
slope, intercept, r, p, sterr = scipy.stats.linregress(x=p.get_lines()[0].get_xdata(),
                                                       y=p.get_lines()[0].get_ydata())

print(intercept, slope)

for index, ride in sorted.iterrows(): 
    if (ride['Wait'] < intercept + slope*ride['People_in_line']):
        sorted.loc[index, 'Cap']= 'high'
    else: sorted.loc[index, 'Cap'] = 'low'



# plt.figure(1)
# sns.regplot(data = sorted, x = people, y = wait)
# for ride in rides:
#     plt.text(sorted[rides == ride]['People_in_line']+10, sorted[rides == ride]['Wait'], ride, horizontalalignment='left', rotation = 0, fontsize='6', color='black', weight='semibold')
# plt.xlabel('Guests in Line')
# plt.ylabel('Wait Time (min)')

## plt.show()

graph0 = sns.lmplot(data = sorted, x = 'People_in_line', y = 'Wait', hue = 'Cap', fit_reg=False, legend = False)
sns.regplot(data = sorted, x = people, y = wait, ax=graph0.axes[0, 0], scatter=False)
for ride in rides.iloc[0:16]:
    plt.text(sorted[rides == ride]['People_in_line']+5, sorted[rides == ride]['Wait'], ride, horizontalalignment='left', rotation = 0, fontsize='6', color='black', weight='semibold')
sns.despine(right = True)
plt.xlabel('Guests in Line')
plt.ylabel('Wait Time (min)')
plt.title('Attractions with Lowest Demand')
plt.xlim(100, 325)
plt.ylim(5, 45)
plt.show()


plt.figure(3)
graph1 = sns.lmplot(data = sorted, x = 'People_in_line', y = 'Wait', hue = 'Cap', fit_reg=False, legend = False)
sns.regplot(data = sorted, x = people, y = wait, ax=graph1.axes[0, 0], scatter=False)
for ride in rides.iloc[16:28]:
    plt.text(sorted[rides == ride]['People_in_line']+10, sorted[rides == ride]['Wait'], ride, horizontalalignment='left', rotation = 0, fontsize='6', color='black', weight='semibold')
sns.despine(right = True)
plt.xlabel('Guests in Line')
plt.ylabel('Wait Time (min)')
plt.title('Attractions with Medium Demand')
plt.xlim(325,1000)
plt.ylim(15, 70)
plt.show()


plt.figure(4)
graph2 = sns.lmplot(data = sorted, x = 'People_in_line', y = 'Wait', hue = 'Cap', fit_reg=False, legend = False)
sns.regplot(data = sorted, x = people, y = wait, ax=graph2.axes[0, 0], scatter=False)
for ride in rides.iloc[28:]:
    plt.text(sorted[rides == ride]['People_in_line']+10, sorted[rides == ride]['Wait'], ride, horizontalalignment='left', rotation = 0, fontsize='6', color='black', weight='semibold')
sns.despine(right = True)
plt.xlabel('Guests in Line')
plt.ylabel('Wait Time (min)')
plt.title('Attractions with Highest Demand')
plt.xlim(left = 1000)
plt.ylim(bottom = 30)
plt.show()


sorted = sorted.sort_values(by = 'People_in_line', ascending = False)
plt.figure(5, figsize = (12,7))
sns.barplot(y = sorted[:10]['Attraction'], x = sorted[:10]['People_in_line'], hue = sorted[:10]['Wait'], dodge = False, color = 'darkblue')
plt.title('Top 10 Disneyland Resort Attractions Ranked by Guests in Queue')
plt.xlabel('Guests in Line')
plt.legend(title = 'Wait Time (min)')
plt.show()


by_wait = (sorted.sort_values(by = 'Wait', ascending= False))

plt.figure(6, figsize = (12,7))
sns.barplot(y = by_wait[:10]['Attraction'], x = by_wait[:10]['People_in_line'], hue = by_wait[:10]['Wait'], dodge = False, color = 'darkblue')
plt.title('Top 10 Disneyland Resort Attractions Ranked by Wait Time')
plt.xlabel('Guests in Line')
plt.legend(title = 'Wait Time (min)')
plt.show()



# by_capacity = (sorted.sort_values(by = 'Capacity', ascending=False))

# plt.figure(7, figsize = (12,7))
# sns.barplot(y = by_capacity[-10:]['Attraction'], x = by_capacity[-10:]['People_in_line'], color= 'cornflowerblue')
# plt.show()
