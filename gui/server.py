from socket import *

##################
# 送信側プログラム#
##################


class Server():
    def __init__(self):
        # 送信側アドレスの設定
        # 送信側IP
        SRC_IP = "127.0.0.1"
        # 送信側ポート番号
        SRC_PORT = 11111
        # 送信側アドレスをtupleに格納
        SRC_ADDR = (SRC_IP, SRC_PORT)

        # 受信側アドレスの設定
        # 受信側IP
        DST_IP = "127.0.0.5"
        # 受信側ポート番号
        DST_PORT = 22222
        # 受信側アドレスをtupleに格納
        self.DST_ADDR = (DST_IP, DST_PORT)

        # ソケット作成
        self.udp_clnt_sock = socket(AF_INET, SOCK_DGRAM)
        # 送信側アドレスでソケットを設定
        self.udp_clnt_sock.bind(SRC_ADDR)

    def send_str(self, str):
        # 送信データの作成
        # self.data = str
        # バイナリに変換
        self.data = str.encode('utf-8')
        # 受信側アドレスに送信
        self.udp_clnt_sock.sendto(self.data, self.DST_ADDR)


if __name__ == "__main__":
    server = Server()
    server.sendUDP("aaaa")
