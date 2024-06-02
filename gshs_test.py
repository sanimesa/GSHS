import streamlit as st

import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt

df = pd.read_excel("data/GSHS_2024_MSHS_629.xlsx", sheet_name="GSHS_2024_MSHS_629 (1)")
source = df

print(df.info())
print(df.dtypes)

#add a dolumn to df with values as all 1    
df['Count'] = 1
print(df.head())
#rename the column "1. Most days I look forward to going to school." to Response 
df = df.rename(columns={"1. Most days I look forward to going to school.": "Response"})
print(df.head())

#create a new dataframe with the sum of count for each ethnicity and response
# df_grouped = df.groupby(['Ethnicity', 'Response']).sum()
# print(df_grouped)

# #reset the index of the dataframe
# df_grouped = df_grouped.reset_index()
# print(df_grouped)

#create a chart with the sum of count for each ethnicity and response
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('sum(Count)').stack("normalize"),
    y='Ethnicity',
    color='Response'
).properties(
    title='Response Distribution by Ethnicity'
)

chart.save('chart.html')


# chart = alt.Chart(source).mark_bar().encode(
#     x=alt.X('sum(Count)').stack("normalize"),
#     y='Ethnicity',
#     color='"1. Most days I look forward to going to school."'
# )

# chart.save('chart.html')

# # Sample data creation
# data = {
#     'Ethnicity': ['Asian', 'Asian', 'Asian', 'Asian', 'Black', 'Black', 'Black', 'Black', 'Hispanic', 'Hispanic', 'Hispanic', 'Hispanic', 'White', 'White', 'White', 'White'],
#     'Response': ['Strongly Agree', 'Somewhat Agree', 'Strongly Disagree', 'Somewhat Disagree', 'Strongly Agree', 'Somewhat Agree', 'Strongly Disagree', 'Somewhat Disagree', 'Strongly Agree', 'Somewhat Agree', 'Strongly Disagree', 'Somewhat Disagree', 'Strongly Agree', 'Somewhat Agree', 'Strongly Disagree', 'Somewhat Disagree'],
#     'Count': [20, 15, 5, 10, 18, 12, 8, 6, 22, 14, 7, 9, 30, 20, 10, 15]
# }

# df = pd.DataFrame(data)

# # Create the chart
# chart = alt.Chart(df).mark_bar().encode(
#     x=alt.X('sum(Count)').stack("normalize"),
#     y='Ethnicity',
#     color='Response'
# ).properties(
#     title='Response Distribution by Ethnicity'
# )

# chart.save('chart.html')