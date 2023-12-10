import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import sklearn
import random
import datetime
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from collections import Counter

# Generate synthetic time series data with a changepoint



def show_word_count(df_normalized, word, diff = False, highlight = False, scaler = 'default', timestep = 'S'):
    df_z = df_normalized[df_normalized['message'] == word]
    count_by_time = df_z.resample(timestep, on='datetime').count()
    if diff:
        count_by_time['message'] = count_by_time['message'].diff()
    if scaler == 'R':
        count_by_time['message'] = RobustScaler().fit_transform(count_by_time['message'].values.reshape((-1, 1)))
    elif scaler == 'M':
        count_by_time['message'] = MinMaxScaler().fit_transform(count_by_time['message'].values.reshape((-1, 1)))
    elif scaler == 'S':
        count_by_time['message'] = StandardScaler().fit_transform(count_by_time['message'].values.reshape((-1, 1)))
    # Plot the graph
    if highlight:
        count_by_time['message'] = count_by_time[count_by_time['message'].abs() > count_by_time['message'].abs().mean()+2]['message']
     # Perform changepoint detection using Pelt
    plt.figure(figsize=(15,6))
    plt.plot(count_by_time.index, count_by_time['message'])
    plt.title('Count of "ㅋㅋ" Messages Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Count')
    plt.grid(True)
    plt.show()
    return count_by_time['message'].reset_index()

def get_highlight_continuous(df_normalized, word, diff = False, highlight = False, scaler = 'default', timestep = 'S'):
    df_z = df_normalized[df_normalized['message'] == word]
    count_by_time = df_z.resample(timestep, on='datetime').count()
    if diff:
        count_by_time['message'] = count_by_time['message'].diff()
    if scaler == 'R':
        count_by_time['message'] = RobustScaler().fit_transform(count_by_time['message'].values.reshape((-1, 1)))
    elif scaler == 'M':
        count_by_time['message'] = MinMaxScaler().fit_transform(count_by_time['message'].values.reshape((-1, 1)))
    elif scaler == 'S':
        count_by_time['message'] = StandardScaler().fit_transform(count_by_time['message'].values.reshape((-1, 1)))
    # Plot the graph
    if highlight:
        count_by_time['message'] = count_by_time[count_by_time['message'].abs() > count_by_time['message'].abs().mean()]['message']
    df = pd.DataFrame(count_by_time['message'].dropna())
    df = df.reset_index()
    df['message'] = df['datetime'].diff()
    # Identify rows where the time difference is greater than 1 minute
    threshold = pd.Timedelta(seconds=1)
    df['message'][0].values = threshold
    result = df[df['message'] == threshold]
    result.set_index('datetime', inplace=True)
    df_normalized.set_index('datetime', inplace=True)
    return df_normalized[df_normalized.index.isin(result.index)]

def get_word_count(df, subword_iterated):
    #by datetime
    #by All
    # Combine all messages into a single string
    all_messages = ' '.join(df['message'].astype(str))
    for word, num in subword_iterated:
        all_messages = re.sub('(' + word + ')' + '{'+str(num)+',}', word*num, all_messages)
    # Tokenize the string into words
    words = all_messages.split()
    # Create a DataFrame for word count
    df_word_count = pd.DataFrame(pd.Series(words).value_counts().reset_index())

    df_word_count.columns = ['word', 'count']

    # Sort the DataFrame by count in descending order
    df_word_count = df_word_count.sort_values(by='count', ascending=False).reset_index(drop=True)
    return


def get_highlight_time(data):
    zero_ranges = []
    start_time = None
    data = data.fillna(0)
    for timestamp, value in data.values:
        dt = datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S")

        if float(value) != 0.0:
            if start_time is None:
                start_time = dt
        elif start_time is not None:
            end_time = dt - timedelta(seconds=1)
            zero_ranges.append((start_time, end_time))
            start_time = None

    # Check if the last entry is zero
    if start_time is not None:
        zero_ranges.append((start_time, dt))
    # zero_ranges = get_zero_ranges(data)
    # Round timestamps to the nearest minute
    rounded_times = [(start_time.replace(second=0, microsecond=0), end_time.replace(second=0, microsecond=0)) for start_time, end_time in zero_ranges]

    # Extract start times
    start_times = [start_time for start_time, _ in rounded_times]
 
    # Count occurrences of each start time
    start_time_counts = Counter(start_times)

    # # Print the results
    # for start_time, count in start_time_counts.items():
    #     print(f"Start Time: {start_time}, Count: {count} times")
    # # Print the results
    
    return zero_ranges, start_time_counts

def get_highlight_word(df, time):
    time = pd.DataFrame(time, columns=['datetime', 'count'])
    df_highlight = pd.merge(df, time, on='datetime', how='inner')
    return df_highlight

def get_word_count_by_datetime(df, how='exploded'):
    # Split the messages into words and count the number of words
    df['word_count'] = df['message'].apply(lambda x: len(str(x).split()))

    # Group by datetime and sum the word counts
    word_count_by_datetime = df.groupby('datetime')['word_count'].sum().reset_index()

    if how == 'exploded':
        # Split the messages into words, explode to separate rows
        df_exploded = df.assign(word=df['message'].str.split()).explode('word')

        # Group by datetime and word, count the occurrences
        word_count_by_datetime = df_exploded.groupby(['datetime', 'word']).size().reset_index(name='count')

    # Print the
    return word_count_by_datetime

def relation_score(df, df_drop):
    relation_score = pd.DataFrame(columns=['word', 'count', 'ratio', 'density'])
    
    # Combine all messages into a single string
    all_messages = ' '.join(df['message'].astype(str))
    # Tokenize the string into words
    words = all_messages.split()
    # Create a DataFrame for word count
    df_word_count = pd.DataFrame(pd.Series(words).value_counts().reset_index())
    df_word_count.columns = ['word', 'count']
    # Sort the DataFrame by count in descending order
    df_word_count = df_word_count.sort_values(by='count', ascending=False).reset_index(drop=True)

    relation_score['word'] = df_word_count['word']
    relation_score['count'] = df_word_count['count']
    for n, word in df_drop.iterrows():
        relation_score = relation_score[relation_score['word'] != word['message']]
    relation_score['ratio'] = relation_score['count'] / relation_score['count'].sum()
    return relation_score

def sum(df, float):
    print(df)
    df['score'] += float
    print(df)

    

def df_relation_score(df, relation_score):
    print(df, relation_score)
    # Create a new column 'score' based on the condition
    # Create a new column 'score' in df
    df['score'] = 0

    # Update 'score' column based on the condition
    for i, word in relation_score.iterrows():
        df.loc[df['word'] == word['word'], 'score'] += word['ratio']

    # Group by datetime and sum the scores
    df_relation_score = df.groupby('datetime')['score'].sum().reset_index()

    # Print
    return df_relation_score