import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import time

# --- PAGE SETUP ---
# Initialize streamlit app
page_title = "PK Non Filer Data"
page_icon = "📄"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered")
csv_file_url = 'https://raw.githubusercontent.com/mzeeshanaltaf/streamlit-pk-nonfiler-eda/d733aa076081f5313b5ca6def0388e838d51e63b/non_filer_pk.csv'


def load_data():
    if "data_frame" not in st.session_state:
        st.session_state.df = None

    start_time = time.time() # Record the start time
    st.session_state.df = pd.read_csv(csv_file_url)
    st.session_state.df['Registration No.'] = st.session_state.df['Registration No.'].astype(str)
    end_time = time.time() # Record the end time
    elapsed_time = round(end_time - start_time) # Calculate the elapsed time
    st.success(f'Data Load Successfully. Time Taken: {elapsed_time} seconds')


def draw_plotly_chart():
    st.divider()
    st.subheader("Select the Chart")
    option = st.selectbox("Select the Chart", ["Non Filers (Male vs Female)", "Non Filers by Province"],
                          label_visibility="collapsed", key='chart_option')
    values = 0
    labels = ''
    if option == "Non Filers (Male vs Female)":
        # Draw a Pie Chart -- Non Filers (Male vs Female)
        st.subheader('Non Filers (Male vs Female)')
        labels = st.session_state.df['Gender'].value_counts().index
        values = st.session_state.df['Gender'].value_counts().values
        fig = px.pie(labels=labels, values=values, title="",
                     names=labels)
        fig.update_layout(width=600, height=600, font=dict(family="Arial, sans-serif", size=15, color="black"),
                          legend_font=dict(family="Arial, sans-serif", size=15, color="black"),
                          margin=dict(l=150, r=0, t=0, b=0, autoexpand=True)
                          )
        fig.update_traces(textposition='outside', textinfo='percent+label',
                          hovertemplate="Gender: %{label} <br>Count: %{value} </br>",
                          hoverlabel=dict(font_size=15, font_family="Arial, sans-serif"),

                          )
        st.plotly_chart(fig)
    elif option == "Non Filers by Province":
        # Draw a Pie Chart -- Non Filers by Province
        st.subheader('Non Filers by Province')
        labels = st.session_state.df['Province'].value_counts().index
        values = st.session_state.df['Province'].value_counts().values
        fig = px.pie(labels=labels, values=values, title="",
                     names=labels, hole=0.4)
        fig.update_layout(width=800, height=800, font=dict(family="Arial, sans-serif", size=15, color="black"),
                          legend_font=dict(family="Arial, sans-serif", size=15, color="black"),
                          margin=dict(l=150, r=0, t=0, b=0, autoexpand=True)
                          )
        fig.update_traces(textposition='outside', textinfo='percent+label',
                          hovertemplate="Gender: %{label} <br>Count: %{value} </br>",
                          hoverlabel=dict(font_size=15, font_family="Arial, sans-serif"),
                          )
        st.plotly_chart(fig)


st.title("Pakistan Non-Tax Filer Data Lookup")
st.write("Search data of Pakistani citizens, who are non tax filers for TY23, using Full Name, "
         "First/Last Name or CNICs.")
st.write("Press load button below to load the data.")
st.info('🛈 Data loading time will vary depending on the speed of your internet connection')
load = st.button("Load Data", type="primary")
if load:
    with st.spinner("Loading Data. Please wait ..."):
        load_data()

# ---- NAVIGATION MENU -----
selection = option_menu(
    menu_title=None,
    options=["Search", "Summary", "About"],
    icons=["bi-search", "bi-pie-chart-fill", "", "app"],  # https://icons.getbootstrap.com
    orientation="horizontal",
)

if selection == "Search":
    try:
        tmp = st.session_state.df.shape[0]  # Accessing the df to check if data has been loaded or not
        st.subheader("Search Options")
        search_option = st.selectbox("Search", ["Full Name", "ID Card Number", "First/Last Name"],
                                     label_visibility="collapsed", key='search_option')
        if search_option == "Full Name":
            full_name = st.text_input("Enter Full Name:")
            if full_name != '':
                result_df = st.session_state.df[st.session_state.df['Name'] == full_name]
                if len(result_df):
                    st.dataframe(result_df, hide_index=True, use_container_width=True)
                else:
                    st.info("No Result Found!")

        elif search_option == "ID Card Number":
            id_card_num = st.text_input("Enter ID Card Number", placeholder="Enter the ID number without dashes ('-')")
            if id_card_num != '':
                if not id_card_num.isdigit() or len(id_card_num) != 13:
                    st.error('Enter the ID card number in correct format')
                else:
                    result_df = st.session_state.df[st.session_state.df['Registration No.'] == id_card_num]
                    if len(result_df):
                        st.dataframe(result_df, hide_index=True, use_container_width=True)
                    else:
                        st.info("No Result Found!")
        elif search_option == "First/Last Name":
            f_l_name = st.text_input("Enter First Name or Last Name:")
            if f_l_name != '':
                result_df = st.session_state.df[st.session_state.df['Name'].str.contains(f_l_name)]
                if len(result_df):
                    st.info(f"Results Found: {len(result_df)}")
                    st.dataframe(result_df, hide_index=True, use_container_width=True)
                else:
                    st.info("No Result Found!")

    except AttributeError:
        st.error("Please load the data by clicking on Load Data button")

if selection == "Summary":
    try:
        tmp = st.session_state.df.shape[0] # Accessing the df to check if data has been loaded or not
        st.subheader("Non-Filer Summary")
        total_non_filers = st.session_state.df.shape[0]
        male_non_filers = st.session_state.df['Gender'].value_counts()['M']
        female_non_filers = st.session_state.df['Gender'].value_counts()['F']
        data = {'Total Non-Filers': [total_non_filers],
                'Males (Non-Filers)': [male_non_filers],
                'Females (Non-Filers)': [female_non_filers]}

        # Create a DataFrame
        df_temp = pd.DataFrame(data)
        st.dataframe(df_temp, hide_index=True, use_container_width=True)

        draw_plotly_chart()

    except AttributeError:
        st.error("Please load the data by clicking on Load Data button")

if selection == "About":
    st.markdown('''
    * **About App:**  
        * Search non-tax filers data of Pakistani citizens   
        * Summary of non-tax filers i.e. total non-filers, males vs female, non-filers by provinces
    * **Data:**
        * Non-Filer data is taken from FBR website: https://www.fbr.gov.pk/Orders/Income-Tax-General-Order/81064?s=08. Released on April 2024.
        * For analysis purpose, converted the PDF into CSV file
    * **Contact:**
        * App code along with CSV file is at:  https://github.com/mzeeshanaltaf/streamlit-pk-nonfiler-eda
        * For any queries, email at zeeshan.altaf@gmail.com 

    ''')