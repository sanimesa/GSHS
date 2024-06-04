import streamlit as st

import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt

df = pd.read_excel("data/GSHS_2024_MSHS_629.xlsx", sheet_name="GSHS_2024_MSHS_629 (1)")
source = df

import altair as alt

# Filter columns based on the pattern
filtered_columns = df.filter(regex='20\. I have felt unsafe at school or on my way to or from school\.'
                                  ' through 29\. How often in the last 30 days has someone bullied me by making fun of me or spreading rumors about me\.', axis=1)

print(len(filtered_columns)) 
print(filtered_columns.head())

# Iterate through each column
for col in filtered_columns:
    # Calculate the proportion of respondents for each unique value
    value_counts = filtered_columns[col].value_counts(normalize=True)

    # Create a DataFrame for the chart
    chart_df = pd.DataFrame({'Response': value_counts.index, 'Proportion of Respondents': value_counts.values})

    # Create a bar chart
    chart = alt.Chart(chart_df, title=col).mark_bar().encode(
        x=alt.X('Response:N', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('Proportion of Respondents:Q'),
        tooltip=['Response', 'Proportion of Respondents']
    ).interactive()

    # Save the chart
    chart.save(f'{col}_bar_chart.json')

# print(df.info())
# print(df.dtypes)

# #add a dolumn to df with values as all 1    
# df['Count'] = 1
# print(df.head())
# #rename the column "1. Most days I look forward to going to school." to Response 
# df = df.rename(columns={"1. Most days I look forward to going to school.": "Response"})
# print(df.head())

# #create a chart with the sum of count for each ethnicity and response
# chart = alt.Chart(df).mark_bar().encode(
#     x=alt.X('sum(Count)').stack("normalize"),
#     y='Ethnicity',
#     color='Response'
# ).properties(
#     title='Response Distribution by Ethnicity'
# )

# chart.save('chart.html')


