import pandas as pd
import streamlit as st

def get_ready_test(RESULTS_PATH: str, uploaded_file):
    
    results = pd.read_csv(RESULTS_PATH)
    results.columns = ['id','real']
    
    test = pd.read_csv(uploaded_file)
    if (test.columns.to_list() != ['Id','Expensive']):
        st.error('Column names must match "Id" and "Expensive" - case sensitive!')
        return 0
    if(test.shape != (1459, 2) ):
        st.error('Your file should contain 1459 rows and 2 columns')
        return 0
    if((test.Expensive.unique().tolist() != [0,1] ) & (test.Expensive.unique().tolist() != [1,0] ) & (test.Expensive.unique().tolist() != [1] ) & (test.Expensive.unique().tolist() != [0] ) ):
        st.error('Predictions should only have values of 0 and 1')
        return 0
    if( (test.Id == results.id).sum() != 1459):
        st.error("Your Id column might be wrong or mixed up. You should have same Id's as the test file. Order of Id's should also be the same.")
        return 0
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
        .merge(test, how='left', on='id')
        .assign(check = lambda df_: df_['real'] == df_['preds'])
        .agg(result = ('check','sum'))
        .assign(
            accuracy = lambda df_: df_['check'] / results.shape[0], 
            participant = st.session_state.text_input, 
            submission_time = pd.Timestamp.now()
            )
        .filter(['participant','accuracy','submission_time'])
        )


def plot_submissions(participant_name): 
    
    participant_submissions = (
        pd.read_pickle('files_to_update/submissions.pkl')
            .query('participant == @participant_name')
            .filter(['submission_time','accuracy'])
            .set_index('submission_time')
            .copy()
        )
    if len(participant_submissions) > 1:
        st.line_chart(participant_submissions)
    else: 
        st.success('Congratulations on your first submission!')


def update_submissions(participant_results: pd.DataFrame):

    (
        pd.concat([
            pd.read_pickle('files_to_update/submissions.pkl'), 
            participant_results
        ])
        .to_pickle('files_to_update/submissions.pkl')
    )


def show_leaderboard(): 

    st.title('LEADERBOARD')

    st.dataframe(
    pd.read_pickle('files_to_update/submissions.pkl')
        .assign(attempts = lambda df_: df_.groupby('participant')['participant'].transform('count'))
        .sort_values(['accuracy'], ascending=False)
        .drop_duplicates(['participant'], keep='first')
        .assign(position = lambda df_: range(1, len(df_)+1)) 
        .set_index('position')  
        .filter(['participant','accuracy','attempts'])
    )
