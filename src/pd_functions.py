import pandas as pd
import streamlit as st

def get_ready_test(uploaded_file):

    test = pd.read_csv(uploaded_file)
    test.columns = ['id','preds']
    return (
    test
        .assign(
            id = lambda df_: df_['id'].astype('int32'),
            preds = lambda df_: df_['preds'].astype('object'),
            )
        )

def get_accuracy(RESULTS_PATH: str, test: pd.DataFrame):

    results = pd.read_csv(RESULTS_PATH)
    results.columns = ['id','real']

    return (
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
        .filter(['participant','accuracy'])
        )

def update_and_show_leaderboard(participant_results: pd.DataFrame): 

    leaderboard = (
        pd.concat([
            pd.read_csv('data/leaderboard.csv'), 
            participant_results
        ], ignore_index=True
        )
        .sort_values(['participant','accuracy'], ascending=False)
        .drop_duplicates(['participant'], keep='first')
        )
    
    st.write('Leaderboard:')
    st.dataframe(leaderboard)

    leaderboard.to_csv('data/leaderboard.csv', index=False)