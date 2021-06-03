from socket import *
import time 

##################
# 受信側プログラム#
##################

class Client():
    def __init__(self):
        # 受信側アドレスの設定
        # 受信側IP
        SrcIP = "127.0.0.5"
        # 受信側ポート番号                           
        SrcPort = 22222
        # 受信側アドレスをtupleに格納
        SrcAddr = (SrcIP, SrcPort)
        # バッファサイズ指定
        self.BUFSIZE = 1024

        # ソケット作成
        self.udpServSock = socket(AF_INET, SOCK_DGRAM)

        self.udpServSock.setblocking(False)

        # 受信側アドレスでソケットを設定
        self.udpServSock.bind(SrcAddr)

    def receiveStr(self):
        try:
            data, addr = self.udpServSock.recvfrom(self.BUFSIZE) 
            # 受信データと送信アドレスを出力
            # print(data.decode())
            return data.decode()
        except BlockingIOError:
            pass


def main():
    client = Client()
    while True:
        print("wait")
        client.receiveUDP()
        time.sleep(0.01)


if __name__ == "__main__":   
    main()