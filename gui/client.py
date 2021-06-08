from socket import *
import time

##################
# 受信側プログラム#
##################


class Client():
    def __init__(self):
        # 受信側アドレスの設定
        # 受信側IP
        SRC_IP = "127.0.0.5"
        # 受信側ポート番号
        SRC_PORT = 22222
        # 受信側アドレスをtupleに格納
        SRC_ADDR = (SRC_IP, SRC_PORT)
        # バッファサイズ指定
        self.BUFSIZE = 1024

        # ソケット作成
        self.udp_serv_sock = socket(AF_INET, SOCK_DGRAM)

        self.udp_serv_sock.setblocking(False)

        # 受信側アドレスでソケットを設定
        self.udp_serv_sock.bind(SRC_ADDR)

    def receive_str(self):
        try:
            data, addr = self.udp_serv_sock.recvfrom(self.BUFSIZE)
            # 受信データと送信アドレスを出力
            # print(data.decode())
            return data.decode()
        except BlockingIOError:
            pass


def main():
    client = Client()
    while True:
        print("wait")
        client.receive_udp()
        time.sleep(0.01)


if __name__ == "__main__":
    main()
