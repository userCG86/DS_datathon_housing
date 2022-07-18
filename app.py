import streamlit as st
import pandas as pd
from students import students
from src.pd_functions import *

# path to results
RESULTS_PATH = 'data/results.csv'

# introduce participant name
text_input_container = st.empty()
text_input_container.text_input(
    "Introduce participant name: ", 
    key="text_input"
    )
if st.session_state.text_input != "": 
    if st.session_state.text_input in students:
        text_input_container.empty()
        st.info('Participant name ' + st.session_state.text_input)
    else: 
        st.write("Please, introduce the your correct student name.")

# upload results file
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None and st.session_state.text_input != "":
    try: 
        # prepare test file
        test = get_ready_test(uploaded_file)
        st.write('### Dataframe uploaded successfully!')
        
       # get participant accuracy and prepare data for leaderboard
        participant_results = get_accuracy(RESULTS_PATH, test)

        # print participant results
        st.write('Participant results:')
        st.dataframe(participant_results)

        # update and show leaderboard
        try: 
            update_and_show_leaderboard(participant_results)
        except: 
            participant_results.to_csv('leaderboard.csv', index=False)
            st.write('First submission!')
        
    except: 
        st.write('The file has a wrong format, please, review it and load it again.')
    