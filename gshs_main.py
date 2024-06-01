import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt

# Load your survey data
survey_data = pd.read_excel("data\GSHS_2024_MSHS_629.xlsx")

# Set the logo image
logo_image = Image.open("images/GaDOE-Logo-Color-188X100.png")  # Replace with the path to your logo image
st.image(logo_image, width=100)

# Set the main text
st.markdown(
    "<h1 style='text-align: center; font-size: 36px; font-weight: bold;'>Georgia Student Health Survey Dashboard</h1>",
    unsafe_allow_html=True,
)

#default page 
page = 'home'

# Add a sidebar with a few links
st.sidebar.title("Navigation")
if st.sidebar.button('Home'):
    # st.experimental_set_query_params(page='home')
    page = 'home'
if st.sidebar.button('Survey Results'):
    # st.experimental_set_query_params(page='survey_results')
    page = 'survey_results'
if st.sidebar.button('About'):
    # st.experimental_set_query_params(page='about')
    page = 'about'
if st.sidebar.button('Gender distribution of respondents'):
    # st.experimental_set_query_params(page='gender_distribution')
    page = 'gender_distribution'

# Check query params to decide which section to display
# query_params = st.query_params
# page = query_params.get('page', ['home'])[0]

if page == 'home':
    # Display the default content
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    c = (
        alt.Chart(chart_data)
        .mark_circle()
        .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
    )

    st.altair_chart(c, use_container_width=True)
elif page == 'gender_distribution':
    # Plotting Gender Distribution
    gender_distribution = survey_data['Gender'].value_counts()

    plt.figure(figsize=(10, 6))
    gender_distribution.plot(kind='bar', color='skyblue')
    plt.title('Gender Distribution of Respondents')
    plt.xlabel('Gender')
    plt.ylabel('Number of Respondents')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)
else:
    st.markdown(f"<h2>Welcome to the {page.replace('_', ' ').title()} Page</h2>", unsafe_allow_html=True)
