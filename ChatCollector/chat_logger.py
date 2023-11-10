import socket
import logging
from emoji import demojize

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

server = 'irc.chat.twitch.tv'
port = 6667
nickname = '' #본인 트위치 닉네임
token = '' #https://twitchapps.com/tmi/ 여기 들어가서 트위치계정으로 로그인하면 'oauth:30dfjl~어쩌구' 이런식으로 토큰이 나옵니다. 그거 복붙하시면 됩니다.
channel = '' #특정 스트리머 아이디 (주소창 클릭 후 아이디만 복붙하시면 됩니다.) ex)#woowakgood <-#붙이고 복붙


def main():
    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\r\n".encode('utf-8'))

    try:
        while True:
            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                # sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                logging.info(demojize(resp))

    except KeyboardInterrupt:
        sock.close()
        exit()

if __name__ == '__main__':
    main()
