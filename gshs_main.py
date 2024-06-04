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

@st.cache_data
def get_school_experience_questions(df):
    #get the names for the 16 through 37 columns 
    questions = df.columns[16:38]
    button_texts = [question[0:50] for question in questions]

    return questions, button_texts
 
@st.cache_data
def get_safety_questions(df):
    #get the names for the 16 through 37 columns 
    questions = df.columns[38:45]
    button_texts = [question[0:50] for question in questions]

    return questions, button_texts

# function to get corresponding element
def get_corresponding_element(item, lookup_dict):
    return lookup_dict.get(item, "Item not found")

#method for school experience and safety questions 
def render_chart_for_questions(survey_data, question):
    #add a dolumn to df with values as all 1    
    survey_data['Count'] = 1

    survey_data = survey_data.rename(columns={question: "Response"})

    col1, col2 = st.columns(2)

    with col1:
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
        #create a chart with the sum of count for each Gender and response
        chart = alt.Chart(survey_data).mark_bar().encode(
            x=alt.X('sum(Count)').stack("normalize"),
            y='Gender',
            color='Response'
        ).properties(
            title='Response Distribution by Gender'
        )

        st.altair_chart(chart, use_container_width=True)

#renders the school experience questions section 
def show_school_experience_questions():
        print('... in school experience questions')
        if 'school_experience_questions_dropdown' in st.session_state:
            print(st.session_state.school_experience_questions_dropdown)

        #retrieve the data
        survey_data = download_data()

        st.markdown(f"<h4>School Exprience Questions:</h4>", unsafe_allow_html=True)

        selected_school_experience_question = None
        questions, button_texts = get_school_experience_questions(download_data())
        school_experience_question_lookup_dict = dict(zip(button_texts, questions))

        school_experience_option = st.selectbox(
            "Select a question:",
            questions, #button_texts,
            key="school_experience_questions_dropdown",
            index=0
        )

        # if school_experience_option and school_experience_option != 'Select a question':
        #     page = 'general_questions'

        # selected_school_experience_question = get_corresponding_element(school_experience_option, school_experience_question_lookup_dict)

        render_chart_for_questions(survey_data, school_experience_option)

#renders the safety questions section 
def show_safety_questions():
        print('... in safety questions')
        if 'safety_questions_dropdown' in st.session_state:
            print(st.session_state.safety_questions_dropdown)

        #retrieve the data
        survey_data = download_data()

        st.markdown(f"<h4>Safety Questions:</h4>", unsafe_allow_html=True)

        selected_safety_question = None
        questions, button_texts = get_safety_questions(download_data())
        safety_question_lookup_dict = dict(zip(button_texts, questions))

        safety_option = st.selectbox(
            "Select a question:",
            questions, #button_texts,
            key="safety_questions_dropdown",
            index=0
        )

        # selected_safety_question = get_corresponding_element(safety_option, safety_question_lookup_dict)

        render_chart_for_questions(survey_data, safety_option)


def main():

    # Set the title 
    st.markdown(
        "<h1 style='text-align: center; font-size: 36px; font-weight: bold;'>Georgia Student Health Survey Dashboard</h1></br>",
        unsafe_allow_html=True,
    )

    # Set the logo image
    logo_image = Image.open("images/GaDOE-Logo-Color-188X100.png")  # Replace with the path to your logo image
    st.sidebar.image(logo_image, width=150)

    page = None 

    # Add a sidebar with links
    st.sidebar.title("Dashboard")
    if st.sidebar.button('Gender distribution of respondents'):
        # if 'general_questions_dropdown' in st.session_state:
        #     st.session_state.general_questions_dropdown = None    
        # if 'safety_questions_dropdown' in st.session_state:
        #     st.session_state.safety_questions_dropdown = None    

        page = 'gender_distribution'

    st.sidebar.title("School Experience")

    if st.sidebar.button('I feel like ... '):
        page = 'school_experience_questions'

    st.sidebar.title("Safety")
    if st.sidebar.button('In the last 30 days ...'):    
        page = 'safety_questions'

    if page == None:
        if 'school_experience_questions_dropdown' in st.session_state:
            page = 'school_experience_questions'
        elif 'safety_questions_dropdown' in st.session_state:
            page = 'safety_questions'
        else: 
            page = 'gender_distribution'

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
        print('... in gender distribution')
        if 'general_questions_dropdown' in st.session_state:
            print(st.session_state.general_questions_dropdown)
        # Plotting Gender Distribution
        survey_data = download_data()
        gender_distribution = survey_data['Gender'].value_counts()

        plt.figure(figsize=(3, 1))
        gender_distribution.plot(kind='bar', color='skyblue')
        plt.title('Gender Distribution of Respondents')
        plt.xlabel('Gender')
        plt.ylabel('Number of Respondents')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(plt, use_container_width=False)
    elif page == 'school_experience_questions':    
        show_school_experience_questions()

    elif page == 'safety_questions':    
        show_safety_questions()

    else:
        st.markdown(f"<h2>Welcome to the {page.replace('_', ' ').title()} Page</h2>", unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Georgia Student Health Survey Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide"
    )

    print("########################################################")
    print(st.session_state)
    print("########################################################")

    main()