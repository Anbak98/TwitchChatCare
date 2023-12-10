import livenlp as lvn
from livenlp import normalizer as lvnn
from livenlp import statistics as lvns
import pandas as pd

############################################
############################################
# streamer_name = 'ralo'
# chat_log_name = 'chat_' + streamer_name
path_chat_log  = './chat.log' # set chat_log path what you want parse E.g chat_file_path='./twitch_chat_log/chat_paka.log'
path_original_excel_file = './Dataset.xlsx' # set SAVE path from parsed chat_log E.g. excel_file_path = './유승민/Dataset_Twitch_Chat.xlsx'
path_subword_excel_file = './subword.xlsx' # set SAVE path from parsed chat_log that include subword group E.g. excel_file_path = './유승민/Dataset_Twitch_Chat.xlsx'
path_rareword_excel_file = './rareword.xlsx' # set SAVE path from parsed chat_log that include rareword group
subword_custom = []
subword_iterated = [['ㅋ' , 2],
                    ['ㄱ' , 2],
                    ['ㄷ' , 2],
                    ['전' , 2],
                    ['캬' , 1],
                    ['ㅑ' , 1],
                    ['ㅁㄷㅊㅇ' , 1],
                    ['ㄹㅇ' , 1],
                    ['ㅇㅈ' , 1]] # 정규식에 의거
top_k= 100
############################################
############################################

df = lvn.get_chat_dataframe(path_chat_log)
df_normalized = lvnn.get_df_normalized(df, subword_iterated)
df_normalized_top_k_word = lvnn.get_top_k_words(df_normalized, top_k, subword_iterated)
df_subword, df_rareword = lvnn.get_sub_and_rare(df_normalized, subword_custom, df_normalized_top_k_word, drop=True, cut=False)
# df_merget_subword = lvnn.get_common_subword([df_subword])
# # lvns.show_changepoint()
# lvns.show_word_count(df_normalized, 'ㅋㅋ', diff= False, highlight=False, scaler='R').to_csv('./A.xlsx', index=False)
# lvns.show_word_count(df_normalized, 'ㅋㅋ', diff= False, highlight=True, scaler='R')
df_highlight_time, df_highlight_counter = lvns.get_highlight_time(lvns.show_word_count(df_normalized, 'ㅋㅋ', diff= False, highlight=True, scaler='R'))
df_highlight = lvns.get_highlight_word(df_normalized, df_highlight_time)
df_highlight_delete_word = lvnn.get_df_normalized(df_highlight, [['ㅋㅋ', 0]])
df_word_count_by_datetime = lvns.get_word_count_by_datetime(df_highlight_delete_word)
df_relation_score = lvns.relation_score(df_normalized, df_subword)
print(lvns.df_relation_score(df_word_count_by_datetime, df_relation_score))
# lvns.show_word_count(df_normalized, 'ㅋㅋ', diff= False, highlight=True, scaler='R'
# df_highlight = pd.DataFrame(lvns.get_highlight_continuous(df_normalized, 'ㅋㅋ', diff= False, highlight=True, scaler='R').reset_index())
# df_relation_score.to_csv('./A.xlsx', index=False)