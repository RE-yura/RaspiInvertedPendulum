from socket import *

##################
# 送信側プログラム#
##################
class Server():
    def __init__(self):
        # 送信側アドレスの設定
        # 送信側IP
        SrcIP = "127.0.0.1"
        # 送信側ポート番号
        SrcPort = 11111
        # 送信側アドレスをtupleに格納
        SrcAddr = (SrcIP,SrcPort)

        # 受信側アドレスの設定
        # 受信側IP
        DstIP = "127.0.0.5"
        # 受信側ポート番号
        DstPort = 22222
        # 受信側アドレスをtupleに格納
        self.DstAddr = (DstIP,DstPort)

        # ソケット作成
        self.udpClntSock = socket(AF_INET, SOCK_DGRAM)
        # 送信側アドレスでソケットを設定
        self.udpClntSock.bind(SrcAddr)

    def sendStr(self, str):
        # 送信データの作成
        # self.data = str
        # バイナリに変換
        self.data = str.encode('utf-8')
        # 受信側アドレスに送信
        self.udpClntSock.sendto(self.data,self.DstAddr)


if __name__ == "__main__":   
    server = Server()
    server.sendUDP("aaaa")