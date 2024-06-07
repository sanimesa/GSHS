import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def download_data():
    df = pd.read_excel("data/GSHS_2024_MSHS_629.xlsx", sheet_name="GSHS_2024_MSHS_629 (1)")

    return df

@st.cache_data
def get_data_table_questions(df):
    #get the names for the 16 through 59 columns 
    questions = df.columns[[i for i in range(16, 59)] + [64, 65, 66, 78, 92, 106, 120, 134, 135, 136, 137, 138]]
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
    #get the names for the 39 through 45 columns 
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

    st.markdown(f"<h4>Data Tables:</h4>", unsafe_allow_html=True)

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

#renders a seaborn heatmap 
def render_heatmap(df, questions, labels=None):
    # columns_of_interest = df.columns[45:49]  # Select columns from index 59 to 63 (inclusive)
    # questions = columns_of_interest.tolist()  # Convert to list

    # Create a dataframe for the questions
    df_questions = df[questions]

    # Replace non-numeric responses with a standard value (e.g., 0)
    day_ranges = ['0 days', '1-5 days', '6-10 days', '11-20 days', 'More than 20 days']

    # df_questions.replace(day_ranges, [0, 1, 2, 3, 4], inplace=True)

    # Calculate the percentage of each response per question
    heatmap_data = df_questions.apply(lambda x: x.value_counts(normalize=True) * 100).fillna(0)
    # heatmap_data

    heatmap_data_transposed = heatmap_data.T

    heatmap_data_transposed_non_zero = heatmap_data_transposed.drop('0 days', axis=1)

    heatmap_data_transposed_non_zero.index.name = 'Substance'
    # heatmap_data_transposed_non_zero
    # Plotting the heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(heatmap_data_transposed_non_zero, annot=True, cmap='coolwarm', linewidths=.5)
    plt.title('Heatmap of Substance Use Responses')
    plt.xlabel('Response Category')
    plt.ylabel('Questions')
    plt.xticks(ticks=[0.5, 1.5, 2.5, 3.5], labels=day_ranges[1:])
    # plt.yticks(ticks=range(len(questions)), labels=[f"Q{i+30}" for i in range(len(questions))], rotation=0)
    if labels == None:
        labels = [f"Q{i+30}" for i in range(len(questions))]
    plt.yticks(ticks=range(len(questions)), labels=labels, rotation=0)
    # plt.show()

    return plt

# Function to calculate the percentage of 'Yes' responses for each question per Ethnicity
def calculate_percentages(survey_data, question):
    count_yes = survey_data.groupby('Ethnicity')[question].apply(lambda x: (x == 'Yes').sum())
    total = survey_data['Ethnicity'].value_counts()
    percentage_yes = (count_yes / total * 100).round(2)
    return percentage_yes

#renders the substance abuse questions
def show_substance_abuse_questions():
    print('... in substance abuse questions')
    #"44. Where do you or your friends usually use alcohol, tobacco, or drugs? Check all that apply:    Do Not Use",

    st.markdown(f"<h4>Substance Abuse Related Questions:</h4>", unsafe_allow_html=True)
    st.markdown(f"<b>44. Where do you or your friends usually use alcohol, tobacco, or drugs?</b>", unsafe_allow_html=True)
    # st.text("44. Where do you or your friends usually use alcohol, tobacco, or drugs?")

    #retrieve the data
    survey_data = download_data()

    columns_of_interest = survey_data.columns[59:64]  # Select columns from index 59 to 63 (inclusive)
    questions = columns_of_interest.tolist()  # Convert to list

    # Create a dataframe with Ethnicity and the questions of interest
    df_interest = survey_data[['Ethnicity'] + questions]

    # Calculate the percentages for each question
    percentages = {question: calculate_percentages(df_interest, question) for question in questions}

    # Create a summary dataframe
    summary_df = pd.DataFrame(percentages)

    summary_df.reset_index(inplace=True)

    summary_df.rename(
        columns={c: f"{c[c.index(':')+1:]}" for c in summary_df.columns if c.startswith('44')}, inplace=True
    )

    # Display the final dataframe
    st.dataframe(summary_df, hide_index=True)

    st.empty()

    col1, col2, col3 = st.columns(3)

    with col1:
        columns_of_interest = survey_data.columns[45:49]  # Select columns from index 59 to 63 (inclusive)
        questions = columns_of_interest.tolist()  # Convert to list
        labels = ['Alcohol', 'Cigaretts', 'Other Tobacco', 'Electronic Vapor']

        st.markdown(f"<b>Alcohol and Tobacco Product Usage:</b>", unsafe_allow_html=True)
        plt = render_heatmap(survey_data, questions, labels)
        st.pyplot(plt)

    with col2:
        columns_of_interest = survey_data.columns[49:52]  # Select columns from index 59 to 63 (inclusive)
        questions = columns_of_interest.tolist()  # Convert to list
        labels = ['Marijuana', 'Methamphetamines', 'Heroin']


        st.markdown(f"<b>Drug Abuse:</b>", unsafe_allow_html=True)
        plt = render_heatmap(survey_data, questions, labels)
        st.pyplot(plt)

    with col3: 
        columns_of_interest = survey_data.columns[[52, 53, 55, 56]]  
        questions = columns_of_interest.tolist()  # Convert to list
        labels = ['Painkiller', 'Tranquilizer', 'Stimulant', 'Other']

        st.markdown(f"<b>Prescription Drug Abuse:</b>", unsafe_allow_html=True)
        plt = render_heatmap(survey_data, questions, labels)
        st.pyplot(plt)


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

    # if 'data_table_questions_dropdown' in st.session_state:
    #     menu_index = 1
    # elif 'school_experience_questions_dropdown' in st.session_state:
    #     menu_index = 2
    # elif 'safety_questions_dropdown' in st.session_state:
    #     menu_index = 3
    # else: 
    #     menu_index = 0

    with st.sidebar:
        selected_menu_item = option_menu(
            menu_title=None, # "Main Menu",  # required
            options=["Overview", "Data Tables", "School Experience", "Safety", 'Substance Abuse'],  # required
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
    elif selected_menu_item == 'Substance Abuse':
        page = 'substance_abuse_questions'


    if page == 'home':
        # Display the default content
        st.text("Not implemented yet")
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

    elif page == 'substance_abuse_questions':    
        show_substance_abuse_questions()

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