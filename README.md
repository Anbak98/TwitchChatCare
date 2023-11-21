Do stream with your digital pet that care your twitch chat  
# How to get dataset using twitch chat
1. run 'chat_logger.py' in directory '/TwitchChatCare/ChatCollector/'  
  **!!!Waring!!! berfore run 'chat_logger.py', you must modify line 12, 13, 14 in 'chat_logger.py'**
3. run 'chat_parser.py' in directory '/TwitchChatCare/ChatCollector/'
4. now you have 'example.xlsx' in directory '/TwitchChatCare/'

# Label
- intention: 
  - 0: 일반대화
  - 1: 감정표현
  - 2: 질문
  - 3: 의견제시
- is_sarcasm: 
  - 0: True, 중의적이다
  - 1: false, 중의적이지 않다
- sentiment: 
  - 0: 중립
  - 1: 긍정
  - 2: 부정
- agreement: 
  - 0: True, 동의
  - 1: false, 비동의
# Reference
If you need use pre-trained model: [huggingface.co](https://huggingface.co/)

If you need know offical Twitch API: [dev.twitch.tv](https://dev.twitch.tv/docs/irc/ ) 

If you need know python twitchAPI Document: [twitchAPI.twitch](https://pytwitchapi.dev/en/stable/modules/twitchAPI.twitch.html#twitchAPI.twitch.Twitch.get_chatters)

If you need use Twitch Chat Log Downloader: [twitchchatdownloader](https://www.twitchchatdownloader.com/  )

[How to Stream Text Data from Twitch with Sockets in Python](https://github.com/LearnDataSci/articles/tree/master/How%20to%20Stream%20Text%20Data%20from%20Twitch%20with%20Sockets%20in%20Python)

[Short Text Classification: A Quick Guide | Levity](https://levity.ai/blog/short-text-classification)

[We need Datase like this](https://www.kaggle.com/datasets/mowglii/twitch-chat-test-data/data)
https://medium.com/coders-camp/nlp-for-whatsapp-chats-data-science-machine-learning-python-c9e2c81ef2ed
