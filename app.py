import streamlit as st
import pandas as pd
from src.pd_functions import *
from src.utils import validate_csv_file

# Constants
RESULTS_PATH = 'data/true_y.csv'

def main():
    st.title('Housing Classification App')
    st.write('Welcome to the housing classification app. Please enter your name and upload your results file to check your accuracy and see the leaderboard.')

    participant_name = get_participant_name()

    if participant_name:
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

        if uploaded_file:
            process_uploaded_file(uploaded_file, participant_name)
        else:
            st.warning('Please upload a file.')
    else:
        st.warning('Please enter your participant name.')

    display_leaderboard()

def get_participant_name():
    text_input_container = st.empty()
    participant_name = text_input_container.text_input(
        "Enter your participant name: ",
        key="text_input"
    )
    return participant_name

def process_uploaded_file(uploaded_file, participant_name):
    if validate_csv_file(uploaded_file):
        try:
            uploaded_file.seek(0)  # Reset file pointer to the beginning
            test = get_ready_test(RESULTS_PATH, uploaded_file)
            if isinstance(test, pd.DataFrame):
                participant_results = get_accuracy(RESULTS_PATH, test)
                st.success('Dataframe uploaded successfully!')
                display_participant_results(participant_results)
                update_and_plot_submissions(participant_results, participant_name)
                
        except Exception as e:
            st.error(f'The file could not be processed. Error: {e}')
    else:
        st.error('The uploaded file has the wrong format. Please, review it and ensure it contains the required columns.')



def display_participant_results(participant_results):
    st.title('Participant results')
    st.dataframe(participant_results)

def update_and_plot_submissions(participant_results, participant_name):
    try:
        update_submissions(participant_results)
        plot_submissions(participant_name)
    except:
        participant_results.to_pickle('files_to_update/submissions.pkl')

def display_leaderboard():
    try:
        show_leaderboard()
    except:
        st.write("There are no submissions.")

if __name__ == "__main__":
    main()
