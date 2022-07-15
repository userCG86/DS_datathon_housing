import streamlit as st
import pandas as pd
import numpy as np

text_input_container = st.empty()
text_input_container.text_input("Introduce participant name: ", key="text_input")

if st.session_state.text_input != "":
    text_input_container.empty()
    st.info('Participant name ' + st.session_state.text_input)

uploaded_file = st.file_uploader("### Choose a file")

if uploaded_file is not None and st.session_state.text_input != "":
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
    results = pd.DataFrame([
                [1, 'a'],
                [2, 'b'],
                [3, 'a'],
                [4, 'a'],
                [5, 'a'],
            ], 
        columns=['id','real']
    )
    
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

    st.write('Partipiant results:')
    st.dataframe(participant_results)

    try: 
        leaderboard = pd.concat(
            [
                pd.read_csv('leaderboard.csv', index_col='participant'), 
                participant_results
            ], ignore_index=False
            )
        st.write('### Leaderboard:')
        st.dataframe(
            leaderboard
            .sort_values(by='accuracy')
        )
        leaderboard.to_csv('leaderboard.csv')
    except: 
        participant_results.to_csv('leaderboard.csv')
        st.write('First submission!')
    