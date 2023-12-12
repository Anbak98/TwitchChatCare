import pandas as pd
import re

class livechat():
    def __init__(self, df, sentiment=[], normalize_target=[], top_k=100, custom_target = []):
        self.df = df
        self.sentiment = sentiment
        self.nomalize_target = normalize_target
        self.top_k = top_k
        self.df_normalized = self.get_df_normalized(df, normalize_target)
        self.df_normalized_exploded = self.get_df_normalized(df, normalize_target, explode=True)
        self.df_normalized_word_count = self.get_word_count(self.df_normalized)
        self.df_normalized_word_count_by_datetime = self.get_word_count_by_group(self.df_normalized, group='datetime')
        self.df_normalized_word_count_by_username = self.get_word_count_by_group(self.df_normalized, group='username')        
        self.df_normalized_word_count_by_datetime_username = self.get_word_count_by_group2(self.df_normalized, group='username', group2='datetime')       
        self.df_normalized_top_k = self.df_normalized_word_count.head(top_k)['word'].tolist()
        self.df_subword, self.df_rareword = self.get_sub_and_rare(self.df_normalized, custom_target, self.df_normalized_top_k)
    def get_df_normalized(self, df, normalize_target, explode = False):
        df_normalized = df
        for word, num in normalize_target:
            df_normalized['message'] = df_normalized['message'].apply(lambda x: re.sub('(' + word + ')' + '{'+str(num)+',}', word*num, str(x)))
            
        if explode:
            # Tokenize the 'message' column by spaces
            df_normalized['message_tokens'] = df_normalized['message'].apply(lambda x: x.split())

            # Group by 'datetime' and explode the lists of tokenized messages
            df_normalized = df_normalized.explode('message_tokens')
        return df_normalized
    
    def get_word_count(self, df):
        all_messages = ' '.join(df['message'].astype(str))
        words = all_messages.split()
        df_word_count = pd.DataFrame(pd.Series(words).value_counts().reset_index())
        df_word_count.columns = ['word', 'count']     
        df_word_count = df_word_count.sort_values(by='count', ascending=False).reset_index(drop=True)
        return df_word_count           
    def get_sub_and_rare(self, df_normalized, subword_custom, top_k_words, drop = True, cut = True):
        df_subword = pd.DataFrame({'message':[]})
        df_rareword = pd.DataFrame({'message':[]})
        for i in subword_custom:
            df_subword = pd.concat([df_subword, df_normalized[df_normalized['message'] == i]], ignore_index=True)
        for i in top_k_words:
            df_subword = pd.concat([df_subword, df_normalized[df_normalized['message'] == i]], ignore_index=True)

        ## make rareword removing subword from original df
        merged_df = pd.merge(df_normalized['message'], df_subword, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only']
        df_rareword = merged_df.drop(columns=['_merge']).reset_index(drop=True)
        if drop:
            df_subword = df_subword.drop_duplicates(subset='message', ignore_index=True)
            df_rareword = df_rareword.drop_duplicates(subset='message', ignore_index=True)
        if cut:
            df_subword = df_subword['message']
            df_rareword = df_rareword['message']

        return df_subword, df_rareword
    def get_word_count_by_group(self, df, how='exploded', group='datetime'):
        # Split the messages into words and count the number of words
        df['word_count'] = df['message'].apply(lambda x: len(str(x).split()))
  
        # Group by datetime and sum the word counts
        word_count_by_datetime = df.groupby(group)['word_count'].sum().reset_index()

        if how == 'exploded':
            # Split the messages into words, explode to separate rows
            df_exploded = df.assign(word=df['message'].str.split()).explode('word')

            # Group by datetime and word, count the occurrences
            word_count_by_datetime = df_exploded.groupby([group, 'word']).size().reset_index(name='count')

        # Print the
        return word_count_by_datetime
    def get_word_count_by_group2(self, df, how='exploded', group='datetime', group2='username'):
        # Split the messages into words and count the number of words
        df['word_count'] = df['message'].apply(lambda x: len(str(x).split()))
  
        # Group by datetime and sum the word counts
        word_count_by_datetime = df.groupby([group, group2])['word_count'].sum().reset_index()

        if how == 'exploded':
            # Split the messages into words, explode to separate rows
            df_exploded = df.assign(word=df['message'].str.split()).explode('word')

            # Group by datetime and word, count the occurrences
            word_count_by_datetime = df_exploded.groupby([group, group2, 'word']).size().reset_index(name='count')

        # Print the
        return word_count_by_datetime

def get_common_subword(df_list):
    merged_df = df_list[0]
    for i in range(1, len(df_list)):
        merged_df = pd.merge(merged_df, df_list[i], on='message', how='inner')
    return merged_df

def drop_df(df, df_drop):
    for n, word in df_drop.iterrows():
        df = df[df['message'] != word['message']]
    return df                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      