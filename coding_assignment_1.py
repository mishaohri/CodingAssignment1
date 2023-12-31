# -*- coding: utf-8 -*-
"""Coding Assignment 1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13FKpcWboMsjTywkEq-p5IYHEy422v0tv

Importing Libraries and Parsing with BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import scipy
from matplotlib import pyplot as plt

opened_webpage = requests.get("https://en.wikipedia.org/wiki/COVID-19_pandemic_cases")
soup = BeautifulSoup(opened_webpage.content, "html.parser")

"""Extracting the Data"""

covid_data = []

table = soup.find("table", {"class": "wikitable"})
rows = table.find_all("tr")

"""Transforming the data and converting it to a dataframe"""

columns = ["Countries and Territories", "First Case", "Last Case", "Jan 4", "Feb 1", "Mar 1", "Apr 1", "May 1", "Jun 1", "Jul 1", "Aug 1", "Sep 1", "Oct 1", "Nov 1", "Dec 1"]

for row in rows:
    cells = row.find_all("td")
    row_data = {}
    cell_texts = [cell.text.strip() for cell in cells]
    for i in range(min(len(columns), len(cell_texts))):
        row_data[columns[i]] = cell_texts[i]
    covid_data.append(row_data)

final_covid_data = pd.DataFrame(covid_data)

"""Checking for duplicates and NA values"""

# checking for duplicate rows

number_of_duplicates = final_covid_data.duplicated().sum()
print (f" Number of duplicates: {number_of_duplicates}")
final_covid_data = final_covid_data.drop_duplicates()
number_of_duplicates = final_covid_data.duplicated().sum()
print (f" Number of duplicates after removing : {number_of_duplicates}")


# dropping any NAs

final_covid_data = final_covid_data.dropna()

"""Cleaning the data and converting data types"""

# cleaning strings un countries and territories

def clean_and_convert(s):
    s = s.replace("[","")
    s = s.replace("]","")
    s = s.replace("7","")
    s = s.replace("8","")
    converted = str(s)
    return converted

# converting object to integer dytpe

def convert_to_int(s):
    s = s.replace(",","")
    converted = int(s)
    return converted


#calling the cleaning functions
final_covid_data["Jan 4"] = final_covid_data["Jan 4"].apply(convert_to_int)
final_covid_data["Feb 1"] = final_covid_data["Feb 1"].apply(convert_to_int)
final_covid_data["Mar 1"] = final_covid_data["Mar 1"].apply(convert_to_int)
final_covid_data["Apr 1"] = final_covid_data["Apr 1"].apply(convert_to_int)
final_covid_data["May 1"] = final_covid_data["May 1"].apply(convert_to_int)
final_covid_data["Jun 1"] = final_covid_data["Jun 1"].apply(convert_to_int)
final_covid_data["Jul 1"] = final_covid_data["Jul 1"].apply(convert_to_int)
final_covid_data["Aug 1"] = final_covid_data["Aug 1"].apply(convert_to_int)
final_covid_data["Sep 1"] = final_covid_data["Sep 1"].apply(convert_to_int)
final_covid_data["Oct 1"] = final_covid_data["Oct 1"].apply(convert_to_int)
final_covid_data["Nov 1"] = final_covid_data["Nov 1"].apply(convert_to_int)
final_covid_data["Dec 1"] = final_covid_data["Dec 1"].apply(convert_to_int)

final_covid_data["Countries and Territories"] = final_covid_data["Countries and Territories"].apply(clean_and_convert)

#checking final data types
print(final_covid_data.dtypes)

"""To clean up this data, I had to first convert the data in the Countries and Territories column from objects to strings. I also had to remove symbols and numbers from the data as the original data from the web included footnotes. Second, I converted the case data to integers. In order for the data to be converted to integers, I also had to remove all the commas seen in the data."""

final_covid_data

"""Downloading to a CSV file"""

final_covid_data.to_csv("2020_COVID_Data.csv")

"""# **Data Visualization**"""

countries = final_covid_data["Countries and Territories"].iloc[3:8]

data_for_apr = final_covid_data.loc[5:9, "Apr 1"]

# Create the bar graph

plt.bar(countries, data_for_apr)
plt.xlabel('Country')
plt.ylabel('COVID Cases on April 1, 2020')
plt.title('COVID-19 Cases on April 1, 2020')

"""## Analysis

The above graph displays the number of coronavirus cases for the countries with some of the largest economies in the world on April 1st, 2020. I chose the date April 1st because it was at this point when COVID cases globally began to increase dramatically. As seen in the graph, the United states had some of the highest cases in world at this point. The data in this graph could be important in order to analyze the effectiveness of emergency response measures at the beginning of the pandemic.

One thing that I find interesting about this graph is the low levels of COVID cases in India, one of the most populated countries in the world. This could also be an indicator of which countries were underreporting or misrepresenting COVID cases at the beginning of the pandemic.
"""