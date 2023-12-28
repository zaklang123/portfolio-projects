
# Introduction:

The purpose of this project is to use web scraping capabilites from Beautiful Soup (a Python library) to extract data from [Touring Plans](https://touringplans.com/). This data will then be used to analyze the most popular attractions at the Disneyland Resort. The data that is extracted is comprised of attraction name, wait time (min) on a crowd level of ten day, and attraction capacity (number of minutes waited per 100 people in line). 


# Process: 

The attraction name, wait time (on a 10/high crowd day), and capacity (wait per 100 people in line) are separately scraped using BeautifulSoup. The data is aggregated into a Pandas DataFrame and the data from Disneyland is joined with data from California Adventure. This DataFrame is then cleaned removing spaces in the data and dropping shows from the table. A new column is created 'People_in_line' this column is calculated by dividing wait time by capacity and multiplying by 100. This column gives a sense of how many guests are waiting in an attraction's queue. The final item to address is rows of the data that have the same values of wait time and capacity. These attractions are aggregated with a '/' in between names. Now the data is ready for visualization.

# Visualization:

Figures were created to help visualize the attraction's wait time versus their number of guests in the queue. A linear regression was run on the data and it was found to be 18.9+0.026(number of guests in line) = approximate wait time. Therefore, every 1000 guests in line has an approximate affect of 26 minutes added to the wait time. The attractions were then color coded as whether they handled crowds better or worse than this. The plot was split into 3 different graphs to assist with visualizing all the data.


![image](https://github.com/zaklang123/portfolio-projects/assets/79182085/9ddce24a-15c3-4646-b213-a5a84b62cae6)

![image](https://github.com/zaklang123/portfolio-projects/assets/79182085/13aac9ad-ff5a-455c-965f-b226924b4f35)

![image](https://github.com/zaklang123/portfolio-projects/assets/79182085/d4a8b5cb-6eef-4752-83f0-f866cf63df53)

# Analysis: 

As seen in the above figures, some attractions have very long wait times, but also handle crowds better whereas others don't handle crowds as well. The goal of this project is to determine the most popular attractions. Some might say that popularity should be determined by how long people are willing to wait in line for an attraction. And while this might be one way to determine popularity that takes into account guest's value of time, another way to look at popularity is how many guests are willing to wait in line for an attraction. This can also be thought of as the number of guests in line for a particular attraction. 

![image](https://github.com/zaklang123/portfolio-projects/assets/79182085/f87b3e5e-59c6-49ec-9a9d-6588eea654ee)


![image](https://github.com/zaklang123/portfolio-projects/assets/79182085/5999906e-9d67-43b6-9ee4-234efdd7fc7b)

#Findings: 

It seems as though looking at attraction popularity through the lens of how many guest are in a queue gives a different picture than looking at it purely based on largest wait time. 

The top 5 at the Disneyland Resort attractions based on wait time:                        The top 5 at the Disneyland Resort attractions based on guests in line: 
1: Radiator Springs Racers                                                                1: Radiator Springs Racers
2: Space Mountain                                                                         2: Indiana Jones
3: Guardians of the Galaxy                                                                3: Space Mountain
4: Indiana Jones                                                                          4: Haunted Mansion
5: Toy Story Mania                                                                        5: Guardians of the Galaxy

As seen above, Radiator Springs Racers is the most popular attraction at the Disneyland Resort. Space Mountain, Guardians of the Galaxy and Toy Story Mania might seem popular based on wait time, but Indiana Jones and Haunted Mansion have a greater popularity when guests in line is taken as the popularity measure. (note that Star War's Galaxy's Edge is not included in this analysis)

Disneyland top 5 attractions based on wait times:                                         Disneyland top 5 attractions based on guests in line:
1: Space Mountain                                                                         1: Indiana Jones
2: Indiana Jones                                                                          2: Space Mountain
3: Splash Mountain                                                                        3: Haunted Mansion
4: Matterhorn Bobsleds                                                                    4: Splash Mountain
5: Star Tours                                                                             5: It's A Small World

If only attractions at Disneyland are analyzed, Splash Mountain and It's A Small World knock out Matterhorn Bobsleds and Star Tours from the top 5. 

#Conclusion:

Finding the most popular attractions at Disneyland can be more complex than it seems. Further measuring any subjective value will be difficult and depend on the analyst's choice of indicators. Some might say that It's A Small World is their least favorite attraction at Disneyland, but taking into account the number of guests in line, it comes out in the top 5. 

#Further Exploration:

There might be many different ways to measure the popularity of an attraction. In this analysis one was chosen to focus on, but the answer to "What are the most popular attractions?" will likely change based on the measurement. In the future, one might want to explore number of times mentioned, satisfaction level or other metrics when coming to a conclusion on this question.


