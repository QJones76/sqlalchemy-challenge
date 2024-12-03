# sqlalchemy-challenge

## Part One: Analysis
In this section of the challenge, I used SQLAlchemy to do a basic climate analysis on an sqlite database file containing Hawaiian whether. The analysis was split into two separate parts: the **precipitation analysis** and the **station analysis**. For the first part, I found the most recent year of data, August 23, 2016 to August 23, 2017, by reflecting the dataset into python classes. Then, I was able to find both the precipitation data and the corresponding date. I used this data with matplotlib to chart the most recent year of precipitation data. The second part of the analysis was first to used the classes to find out the most active station. After doing that, I was able find the last 12 months of the temperature observation data and plot it into a histogram to highlight the common frequency of different temperatures.

---
## Part Two: Designing a Climate App
I used Flask to develop an API that returns JSON data. The API has five different endpoints. There are 3 static routes that returns: precipitation analysis for the last year with the date as a key in the dictionary, a list of all the stations in the database, and the last year of temperature data for the most active station. Furthermore, there are two dynamic routes. The first route accepts a "start date" as a parameter from the URL and returns summary statistics from the parameter to the end of the dataset. The second route does the same thing but also accepts an "end date" parameter. 

---
### Citations
- I used [this](https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_returning_list_and_scalars.htm) in association with [ChatGPT](https://chatgpt.com/) to implement and understand the `.scalar()` SQLAlchemy function 
