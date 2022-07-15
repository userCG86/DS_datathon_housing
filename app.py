import streamlit as st
import pandas as pd
import numpy as np

# introduce participant name
text_input_container = st.empty()
text_input_container.text_input(
    "Introduce participant name: ", 
    key="text_input"
    )
if st.session_state.text_input != "":
    text_input_container.empty()
    st.info('Participant name ' + st.session_state.text_input)

# upload results file
uploaded_file = st.file_uploader("### Choose a file")

if uploaded_file is not None and st.session_state.text_input != "":
    try: 
        # prepare test file
        test = (
            pd.read_csv(uploaded_file)
            )
        test.columns = ['id','preds']
        test = (
        test
            .assign(
                id = lambda df_: df_['id'].astype('int32'),
                preds = lambda df_: df_['preds'].astype('object'),
                )
            )
        st.write('### Dataframe uploaded successfully!')
        
        # load real results
        results = pd.read_csv('results.csv')

        # get participant accuracy and prepare data for leaderboard
        participant_results = (
        results
            .assign(
                id = lambda df_: df_['id'].astype('int32'),
                real = lambda df_: df_['real'].astype('object')
            )
            .merge(test, how='inner')
            .assign(check = lambda df_: df_['real'] == df_['preds'])
            .agg(result = ('check','sum'))
            .assign(
                accuracy = lambda df_: df_['check'] / results.shape[0], 
                participant = st.session_state.text_input
                )
            .filter(['participant','accuracy'])\
            .set_index('participant')
        )

        # print participant results
        st.write('Partipiant results:')
        st.dataframe(participant_results)

        # update and show leaderboard
        try: 
            leaderboard = pd.concat(
                [
                    pd.read_csv('leaderboard.csv', index_col='participant'), 
                    participant_results
                ], ignore_index=False
                )
            st.write('Leaderboard:')
            st.dataframe(
                leaderboard
                .sort_values(by='accuracy', ascending=False)
            )
            leaderboard.to_csv('leaderboard.csv')
        except: 
            participant_results.to_csv('leaderboard.csv')
            st.write('First submission!')
        
    except: 
        st.write('The file has a wrong format, please, review it and load it again.')
    