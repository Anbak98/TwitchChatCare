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

def vibe_score(livechat, word):
    df = livechat.df_normalized
    df_z = df[df['message'] == word]
    count_by_time = df_z.resample('T', on='datetime').count()
    return
class statistics():
    def __init__(self, livechat, subword, relation_score_path = None):
        self.highlight                = self.get_highlight(livechat)
        self.highlight_time_group     , self.highlight_time_group_counter = self.get_highlight_time_group(self.highlight)
        self.highlight_word             = self.get_highlight_word(livechat, self.highlight_time_group)
        self.highlight_by_datetime = self.get_word_count_by_datetime(self.highlight_word)
        self.relation_score = self.get_relation_score(livechat, drop_df=subword, relation_score_path=relation_score_path)
        self.highlight_score = self.get_highlight_score(self.highlight_by_datetime, self.relation_score)
        
    def get_highlight(self, livechat, diff = True, highlight = False, show=True, scaler = 'M', timestep = 'T'):
        df_normalized = livechat.df_normalized
        word = "ㅋㅋ"
        df_z = df_normalized[df_normalized['message'] == word]
        count_by_time = df_z.resample(timestep, on='datetime').count()
        result = count_by_time
        title = 'Use: Count'
        ylabel = 'Count'
        if diff:
            count_by_time['message'] = count_by_time['message'].diff()
            title += ' ,diff'
            ylabel = 'diff'
        if scaler == 'R':
            count_by_time['message'] = RobustScaler().fit_transform(count_by_time['message'].values.reshape((-1, 1)))
            title += ' ,Robust'
        elif scaler == 'M':
            count_by_time['message'] = MinMaxScaler().fit_transform(count_by_time['message'].values.reshape((-1, 1)))
            title += ' ,MinMax'
        elif scaler == 'S':
            count_by_time['message'] = StandardScaler().fit_transform(count_by_time['message'].values.reshape((-1, 1)))
            title += ' ,Standart'
        # Plot the graph
        if highlight:
            count_by_time['message'] = count_by_time['message'].apply(lambda row: row if (row >= 0.625) else None)
            title += ' ,highligt'
        if show:
            # Perform changepoint detection using Pelt
            plt.figure(figsize=(15,6))
            plt.plot(count_by_time.index, count_by_time['message'])
            plt.title(title)
            plt.xlabel('Timestamp')
            plt.ylabel(ylabel)
            plt.grid(True)
            plt.show()
        result = count_by_time['message'].reset_index()
        return result
    def get_highlight_time_group(self, data):
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

    def get_highlight_word(self, livechat, time):
        df = livechat.df_normalized
        time = pd.DataFrame(time, columns=['datetime', 'count'])
        df_highlight = pd.merge(df, time, on='datetime', how='inner')
        return df_highlight

    def get_word_count_by_datetime(self, df, how='exploded'):
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

    def get_relation_score(self, livechat, drop_df, relation_score_path):
        if relation_score_path:
            return pd.read_csv(relation_score_path)
        relation_score = pd.DataFrame(columns=['word', 'count', 'ratio', 'density'])
        
        relation_score['word'] = livechat.df_normalized_word_count['word']
        relation_score['count'] = livechat.df_normalized_word_count['count']
        df = livechat.df_normalized_exploded
        if not drop_df.empty:
            # Create a list of messages to drop
            messages_to_drop = drop_df['message'].tolist()
            # Drop rows from df where the 'message' column matches any entry in messages_to_drop
            df = df[~df['message_tokens'].isin(messages_to_drop)]
        for n, word in relation_score.iterrows():
            escaped_word = re.escape(word['word'])
            density = df[df['message_tokens'].str.contains(escaped_word)].reset_index(drop=True)
            density = pd.concat([df.head(1), density], ignore_index=True)
            density = pd.concat([density, df.tail(1)], ignore_index=True)
            result = density['datetime'].diff().diff().abs().std().total_seconds()
            relation_score.at[n, 'density'] = result
        relation_score = relation_score.dropna(subset=['density'])
        relation_score['ratio'] = relation_score['count'] / relation_score['count'].sum()
        relation_score['ratio'] = RobustScaler().fit_transform(relation_score['ratio'].values.reshape((-1, 1)))
        relation_score['density'] = RobustScaler().fit_transform(relation_score['density'].values.reshape((-1, 1)))
        relation_score['ratio'] = pd.DataFrame(relation_score['ratio']).round(5)
        relation_score['density'] = pd.DataFrame(relation_score['density']).round(5)
        return relation_score   

    def get_highlight_score(self, highlight, relation_score):
        # Create a new column 'score' based on the condition
        # Create a new column 'score' in df
        highlight['score'] = 0.0

        # Update 'score' column based on the condition
        for i, word in relation_score.iterrows():
            highlight.loc[highlight['word'] == word['word'], 'score'] += word['density']

        # Group by datetime and sum the scores
        highlight_score = highlight.groupby('datetime')['score'].mean().reset_index()

        # Print
        return highlight_score

    def density(self, df, word):
        density = df[df['message'].str.contains(word, case=False)]
        result = density['datetime'].diff().diff().abs().mean()
        return result.total_seconds()

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


