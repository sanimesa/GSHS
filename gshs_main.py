import streamlit as st
from streamlit_option_menu import option_menu
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
def get_data_table_questions(df):
    #get the names for the 16 through 37 columns 
    questions = df.columns[16:45]
    button_texts = [question[0:50] for question in questions]

    return questions, button_texts


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

#format and display data tabales 
def render_data_table(survey_data, data_table_option):
    #crosstable to get the counts 
    transformed_df = pd.crosstab(survey_data[' SchoolName'], survey_data[data_table_option])
    transformed_df.reset_index(inplace=True)
    transformed_df.columns.name = None

    # Calculate the sums of the response columns 
    column_names = [str(col) for col in transformed_df.columns[1:]]
    sums = transformed_df[column_names].sum()

    # Create a new row with the sums
    all_schools_row = pd.DataFrame([['All Schools'] + sums.tolist()], columns=transformed_df.columns)

    # Append the new row to the original DataFrame
    df_with_all_schools = pd.concat([all_schools_row, transformed_df], ignore_index=True)

    # Add a 'Totals' column
    df_with_all_schools['Totals'] = df_with_all_schools[column_names].sum(axis=1)

    # Display the final dataframe
    st.dataframe(df_with_all_schools, hide_index=True)

#section to show raw data of the survey 
def show_data_tables():
    print("... in data tables")

    #retrieve the data
    survey_data = download_data()

    st.markdown(f"<h4>School Exprience Questions:</h4>", unsafe_allow_html=True)

    questions, button_texts = get_data_table_questions(download_data())

    data_table_option = st.selectbox(
        "Select a question:",
        questions, #button_texts,
        key="data_table_questions_dropdown",
        index=0
    )

    render_data_table(survey_data, data_table_option)


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
        """
        <h1 style='text-align: center; font-size: 36px; font-weight: bold;'>Georgia Student Health Survey Dashboard</h1>
        <h4 style='text-align: center; font-size: 14px; '>Clarke County, Middle and High Schools, 2024</h4></br>
        """,
        unsafe_allow_html=True,
    )

    # Set the logo image
    logo_image = Image.open("images/GaDOE-Logo-Color-188X100.png")  # Replace with the path to your logo image
    st.sidebar.image(logo_image, width=150)

    page = None 

    if 'data_table_questions_dropdown' in st.session_state:
        menu_index = 1
    elif 'school_experience_questions_dropdown' in st.session_state:
        menu_index = 2
    elif 'safety_questions_dropdown' in st.session_state:
        menu_index = 3
    else: 
        menu_index = 0

    with st.sidebar:
        selected_menu_item = option_menu(
            menu_title=None, # "Main Menu",  # required
            options=["Overview", "Data Tables", "School Experience", "Safety"],  # required
            #icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            # default_index=menu_index,  # optional
        )

    # # Add a sidebar with links
    # st.sidebar.title("Dashboard")

    # if st.sidebar.button('Overview'):
    #     # if 'general_questions_dropdown' in st.session_state:
    #     #     st.session_state.general_questions_dropdown = None    
    #     # if 'safety_questions_dropdown' in st.session_state:
    #     #     st.session_state.safety_questions_dropdown = None    

    #     page = 'overview'

    # st.sidebar.title("School Experience")
    # if st.sidebar.button('I feel like ... '):
    #     page = 'school_experience_questions'

    # st.sidebar.title("Safety")
    # if st.sidebar.button('In the last 30 days ...'):    
    #     page = 'safety_questions'

    # if page == None:
    #     if 'school_experience_questions_dropdown' in st.session_state:
    #         page = 'school_experience_questions'
    #     elif 'safety_questions_dropdown' in st.session_state:
    #         page = 'safety_questions'
    #     else: 
    #         page = 'overview'

    if selected_menu_item == 'Overview':
        page = 'overview'
    elif selected_menu_item == 'Data Tables':
        page = 'data_tables'
    elif selected_menu_item == 'School Experience':
        page = 'school_experience_questions'
    elif selected_menu_item == 'Safety':
        page = 'safety_questions'


    if page == 'home':
        # Display the default content
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

        c = (
            alt.Chart(chart_data)
            .mark_circle()
            .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
        )

        st.altair_chart(c, use_container_width=True)
    elif page == 'overview':
        print('... in overview')

        survey_data = download_data()
        survey_data['Count'] = 1
        print(survey_data.columns)

        # You can also add multiple metrics side by side
        col11, col12, col13 = st.columns(3)
        col11.metric("Number of Systems", len(survey_data[' SystemName'].unique()))
        col12.metric("Number of Schools", len(survey_data[' SchoolName'].unique()))
        col13.metric("Number of Students", len(survey_data))

        st.divider()

        col21, col22, col23 = st.columns(3)

        with col21:
            ethnicity_distribution = survey_data.groupby('Ethnicity')['Count'].sum().reset_index()

            chart = alt.Chart(ethnicity_distribution).mark_arc().encode(
                    theta="Count",
                    color="Ethnicity"
                )
            
            st.altair_chart(chart, use_container_width=True)

        with col22:
            gender_distribution = survey_data.groupby('Gender')['Count'].sum().reset_index()

            chart = alt.Chart(gender_distribution).mark_arc().encode(
                    theta="Count",
                    color="Gender"
                )
            
            st.altair_chart(chart, use_container_width=True)

        with col23:
            grade_distribution = survey_data.groupby('Grade')['Count'].sum().reset_index()

            chart = alt.Chart(grade_distribution).mark_arc().encode(
                    theta="Count",
                    color="Grade"
                )
            
            st.altair_chart(chart, use_container_width=True)

    elif page == 'data_tables':    
        show_data_tables()

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