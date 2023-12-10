import pandas as pd
import re

def get_df_normalized(df, normalize_target):
    df_normalized = df
    for word, num in normalize_target:
        df_normalized['message'] = df_normalized['message'].apply(lambda x: re.sub('(' + word + ')' + '{'+str(num)+',}', word*num, str(x)))
    return df_normalized

def get_top_k_words(df, top_k, subword_iterated):
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
    top_k_words = df_word_count.head(top_k)['word'].tolist()
    
    return top_k_words

def get_sub_and_rare(df_normalized, subword_custom, top_k_words, drop = True, cut = True):
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

def get_common_subword(df_list):
    merged_df = df_list[0]
    for i in df_list:
        merged_df = pd.merge(merged_df, i, on='message', how='inner')
    return merged_df

def drop_df(df, df_drop):
    for n, word in df_drop.iterrows():
     print(word['message'])
     df = df[df['message'] != word['message']]
     print(df)
    return df                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      