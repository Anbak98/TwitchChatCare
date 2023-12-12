import livenlp as lvn
from livenlp import livechat as lvc
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
custom_target = []
normalize_target = [['ㅋ' , 2],
                    ['ㄱ' , 2],
                    ['ㄷ' , 2],
                    ['전' , 2],
                    ['캬' , 1],
                    ['ㅑ' , 1],
                    ['ㅁㄷㅊㅇ' , 1],
                    ['ㄹㅇ' , 1],
                    ['ㅇㅈ' , 1],
                    ] # 정규식에 의거
sentiment = [{'재미' : ['ㅋㅋ']}, 
            {'감탄' : ['캬', '와']},
            {'의문' : ['?']},
            {'놀람' : ['ㄷㄷ', '헉', '어어']},
            {'동의' : ['ㄹㅇ', 'ㅇㅇ', 'ㄹㅇㅋㅋ']},
            {'답답' : ['아니', '아오']},
            {'실망' : ['아']},
            {'비웃음': ['ㅋ']}]
top_k= 100
############################################
############################################

df_paka = lvn.get_chat_dataframe("./log/chat_paka.log")
df_mstrat = lvn.get_chat_dataframe("./log/chat_mstrat.log")
df_ralo = lvn.get_chat_dataframe("./log/chat_ralo.log")

paka = lvc.livechat(df_paka, sentiment=sentiment, normalize_target=normalize_target, top_k=top_k, custom_target=custom_target)
mstrat = lvc.livechat(df_mstrat, sentiment=sentiment, normalize_target=normalize_target, top_k=top_k, custom_target=custom_target)
ralo = lvc.livechat(df_ralo, sentiment=sentiment, normalize_target=normalize_target, top_k=top_k, custom_target=custom_target)

subword = lvc.get_common_subword([paka.df_subword, mstrat.df_subword, ralo.df_subword])
print(subword)
# df_merget_subword = lvc.get_common_subword([df_subword])
# # lvns.show_changepoint()
# lvns.show_word_count(df_normalized, 'ㅋㅋ', diff= False, highlight=False, scaler='R').to_csv('./A.xlsx', index=False)
# lvns.show_word_count(df_normalized, 'ㅋㅋ', diff= False, highlight=True, scaler='R')

# print(lvns.density(paka.df_normalized, "엄신"))
# print(lvns.density(paka.df_normalized, "ㅎㅎㅈㅅ"))
# lvns.show_word_count(paka.df_normalized, 'ㅋㅋ', diff= True, highlight=True, scaler='M')
df_highlight_time, df_highlight_counter = lvns.get_highlight_time(lvns.show_word_count(paka.df_normalized, 'ㅋㅋ', diff= False, highlight=True, scaler='R'))
df_highlight = lvns.get_highlight_word(paka.df_normalized, df_highlight_time)
df_word_count_by_datetime = lvns.get_word_count_by_datetime(df_highlight)

paka_relation_score = lvns.relation_score(paka, subword)

print(lvns.df_relation_score(df_word_count_by_datetime, paka_relation_score))
# # lvns.show_word_count(df_normalized, 'ㅋㅋ', diff= False, highlight=True, scaler='R'
# df_highlight = pd.DataFrame(lvns.get_highlight_continuous(df_normalized, 'ㅋㅋ', diff= False, highlight=True, scaler='R').reset_index())
paka_relation_score.to_csv('./A.xlsx', index=False)