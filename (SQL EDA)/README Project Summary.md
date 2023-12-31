
# Introduction:

The purpose of this project is to use MySQL to analyze a bike store relational database. The datasets can be found [here](https://www.sqlservertutorial.net/sql-server-sample-database/). The database will be analyzed with the purpose of recommending business changes that might help to promote growth. 


# Process: 

First the relational database was viewed and some questions were developed to help determine the status of the business. Sqlservertutorial provided a image of the layout of the relational database that was critical to the SQL queries developed. 

<img width="746" alt="bike_relational_database" src="https://github.com/zaklang123/portfolio-projects/assets/79182085/64fce57c-eb82-4c79-821f-de6b4d789d77">

The questions that were developed from this image were as follows:

1: Where are customers buying products from?
2: What is the most commonly purchased product?
3: What email providers are the most popular among customers?
4: What are the most and least expensive products sold?
5: Which store has the greatest revenue and are store employees allocated efficiently?
6: What brand contributes the most to total revenue?

With these questions in hand it was time for analysis.


# Analysis: 

1: Where are customers buying products from?

Most customers buy products in New York (71%) followed by California (20%) and Texas (10%). It seems as though there are only customers in these states.

2: What is the most commonly purchased product?

The most commonly bought product is a Surly Ice Cream Trucj Frameset - 2016 (with 167 of them bought). The most commonly bought product per order is also a Surly Ice Cream Trucj Frameset - 2016 (with 110 of them bought). There are 32 products that are only sold once.

3: What email providers are the most popular among customers?

The bike store's customers use 5 email providers Yahoo, Gmail, MSN, AOL, and Hotmail. They use them in approximately the same proportion. 

4: What are the most and least expensive products sold?

The most expensive product is Trek Domane SLR 9 Disc - 2018 with a list price of $11999.99 and a total of 5 sold. The least expensive product sold is Strider Classic 12 Balance Bike - 2018 with a list price of $89.99 and a total of 11 sold.

5: Which store has the greatest revenue and are store employees allocated efficiently?

The store in Baldwin, NY earns 63% of the revenue. Whereas, Santa Cruz, CA and Rowlett, TX earn 26% and 10% of the revenue respectively. The employees are allocated in an approximately even fashion with 3 in NY, 3 in TX, and 4 in CA.

6: What brand contributes the most to total revenue?

Trek represents 59.8% of the total revenue with $5 million sold. Strider represents 0.1% of the total revenue with $5000 sold.


# Key Findings:

- Greater than 70% of customers make purchases at the New York store and it is responsible for 63% of total revenue. 
- Surly Ice Cream Trucj Frameset - 2016 is the most sold product. 
- There are 32 products only sold once.
- Trek represents 59.8% of the total revenue. Strider represents 0.1% of the total revenue.


# Conclusion:

The Findings suggest that Baldwin, New York might have the greatest market for this type of bike store. Further, it might be useful to explore opening another store near Baldwin, New York. It is important to maintain inventory of the Surly Ice Cream Trucj Frameset - 2016 since it is the most common purchase. It might be worthwhile to look into removing some of the 32 products that were only sold once and removing Strider as a brand that is sold. 

# Further Exploration:

Exploration of the 32 products that were only sold once to see if they correspond to a demographic that we don't have much alternatives for, or if they are products we might move from our stores to create more space for other inventory would be useful. Another possible future analysis could be seeing what attributes a lower number of customers at the Texas and California stores. Maybe there is something that can be done to increase purchases here. 


