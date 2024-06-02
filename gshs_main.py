import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt

# Load your survey data
@st.cache_data
def download_data():
    df = pd.read_excel("data/GSHS_2024_MSHS_629.xlsx", sheet_name="GSHS_2024_MSHS_629 (1)")

    return df


st.set_page_config(layout="wide")

# Set the logo image
logo_image = Image.open("images/GaDOE-Logo-Color-188X100.png")  # Replace with the path to your logo image
# st.image(logo_image, width=100)

# Set the main text
st.markdown(
    "<h1 style='text-align: center; font-size: 36px; font-weight: bold;'>Georgia Student Health Survey Dashboard</h1></br>",
    unsafe_allow_html=True,
)

#default page 
page = 'home'

st.sidebar.image(logo_image, width=150)

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

st.sidebar.title("General Questions")
if st.sidebar.button('How often / I feel ..'):
    page = 'general_questions'

# Check query params to decide which section to display
# query_params = st.query_params
# page = query_params.get('page', ['home'])[0]

survey_data = download_data()

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
elif page == 'general_questions':    

    survey_data['Count'] = 1
    #rename the column "1. Most days I look forward to going to school." to Response 
    survey_data = survey_data.rename(columns={"1. Most days I look forward to going to school.": "Response"})

    col1, col2 = st.columns(2)

    # Plot the first chart in the first column
    with col1:
        #add a dolumn to df with values as all 1    

        #create a chart with the sum of count for each ethnicity and response
        chart = alt.Chart(survey_data).mark_bar().encode(
            x=alt.X('sum(Count)').stack("normalize"),
            y='Ethnicity',
            color='Response'
        ).properties(
            title='Response Distribution by Ethnicity'
        )

        st.altair_chart(chart, use_container_width=True)

    with col2:
        #add a dolumn to df with values as all 1    

        #create a chart with the sum of count for each ethnicity and response
        chart = alt.Chart(survey_data).mark_bar().encode(
            x=alt.X('sum(Count)').stack("normalize"),
            y='Gender',
            color='Response'
        ).properties(
            title='Response Distribution by Gender'
        )

        st.altair_chart(chart, use_container_width=True)


else:
    st.markdown(f"<h2>Welcome to the {page.replace('_', ' ').title()} Page</h2>", unsafe_allow_html=True)
