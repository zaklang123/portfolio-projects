
# Introduction:

The purpose of this project is to use Python's scipy library to analyze healthcare data. The dataset can be found [here](https://www.kaggle.com/zak852/python-a-b-testing-healthcare-data/edit). The dataset will be used to see if there is a statistically significant difference in patient's BMI among those who have been married and those who have never been married. Please note that the data source cannot be verified; therefore, no concrete conclusions can be extracted from this analysis.

# Narrative: 

There seems to a narrative that people who are married tend to be less healthy or gain more weight. This is thought to come from the idea that once you picked someone to spend the rest of your life with, you won't have to worry about attracting a partner. There also seems to be less of an incentive to maintain a "healthy" BMI, as married people are considered "locked in" to their partners no matter their BMI. Please note that BMI is not a cummulative measurement of health and it only takes into account someone's height and weight. 


# Method: 

It was desired to run an A/B test (two-tailed t-test) on the dataset. However, an A/B test has a few key assumptions which must be noted. 

A/B Test Assumptions:  
1: The data must be collected through random sampling (assumed/there is no data source provided).   
2: There must be two categorical groups in the independent variable (married and not married were the groups used).  
3: The dependent variable in the analysis must be continuous (BMI is a continuous measurement).   
4: The observations should be independent (assumed from different patients with no relation).    
5: The two groups should have equal variance (to be tested below).  
6: The two groups should have a normal distribution (to be tested below).




# Analysis: 

Before running any type of t-test, the assumptions above must be verified. Assumption 5 and 6 have yet to be verified so they will be included in this analysis. 

5: The two groups should have equal variance (to be tested below).  
6: The two groups should have a normal distribution (to be tested below).

To test for equal variance of the two groups, a Levene’s test was used. The null hypothesis for this test was that the two groups have equal variances. Below are the results. 

LeveneResult(statistic=9.325138211532005, pvalue=0.00227243243293373)

The p-value of this result is less than the significance value of 0.05. This indicates that the null hypothesis should be rejected and the two groups do not have equal variances. Therefore, assumption 5 is not true, and a Welch's t-Test must be used.   



To test for a normal distribution of the two groups, a variety of methods was used: 

Method 1: Plotting the distributions in histograms

![Screenshot 2023-12-31 at 3 26 13 PM](https://github.com/zaklang123/portfolio-projects/assets/79182085/c8a70e64-1cc5-48f6-9d53-1e9ad27dc102)

![Screenshot 2023-12-31 at 3 26 21 PM](https://github.com/zaklang123/portfolio-projects/assets/79182085/87b8a32c-cd5d-4a8e-88c0-d1852f28a36d)

As can be seen in the plots above, the data do seem to follow normal distributions.

Method 2: Plotting Q-Q Plots

![Screenshot 2023-12-31 at 3 26 43 PM](https://github.com/zaklang123/portfolio-projects/assets/79182085/d8e283de-cdf8-4d21-9b1c-d197b129364c)

![Screenshot 2023-12-31 at 3 26 51 PM](https://github.com/zaklang123/portfolio-projects/assets/79182085/5a431dd8-2f33-4512-bd4c-9556a9659b51)

As seen from these Q-Q plots the data do seem to follow normal distributions other than the far right side.

Method 3: Shapiro-Wilk Test

As a finally check on normality, a Shapiro-Wilk Test was run with the null hypothesis being that the data was normally distributed. The findings were as follows. 

Married: ShapiroResult(statistic=0.9036297798156738, pvalue=1.7109067544932968e-31)
Never Married: ShapiroResult(statistic=0.9349775314331055, pvalue=2.6617560028402604e-35)

These p-value are smaller than the significance value of 0.05, we will reject the null hypothesis of the data being normally distributed. However, the assumption of normality is less significant the larger the sample size and there are 1705 married observations and 3204 not married observations. These are greater than the 30 and 50 observations required, so the assumption of normality can be removed. 


A Welch's t-Test was performed on the two groups of data. The null hypothesis of this test is that the two populations have equal means. Below is the result.

TtestResult(statistic=-24.828791740516657, pvalue=1.0337793601110332e-124, df=3235.2107217019943)

The p-value is less than the significance value of 0.05. This indicates that the null hypothesis should be refuted and there is a difference in means of the two populations. The negative in the statistic value indicates that the married patients have lower average BMI than the never married patients.

# Conclusion:

Contrary to what was discussed in the narrative portion of this analysis, the population of married patients was found to have a lower BMI than the population of never married patients. This could be due to a variety of factors. One influence might be that people with a lower BMI are more likely to find a partner, and that after becoming married, their BMI doesn't change. Although this analysis doesn't come from a valid dataset, it is an interesting finding.

# Further Exploration:

A further exploration of this topic is necessary in order to claim any sort of findings. The dataset would have to come from a verified source and take random sampling into account. It would be interesting to see if these findings would be repeated or if something else would be deterimined. Additionally, BMI is only one influencing factor of health, so it would be useful to explore other variables that might be influenced by marriage. 

