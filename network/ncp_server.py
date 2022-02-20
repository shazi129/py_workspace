import socketserver
import time
import random

#固定回复
reply_list = ["yes", "you are right", "ok", "emm", "I can't understand", "haha"]

class MyServer(socketserver.BaseRequestHandler):

    def setup(self):
        print(self.request)

    def handle(self):
        # 第二步：服务器端阻塞，等待客户端连接
        # 重写父类中的handle方法，主要实现服务端的逻辑代码，，不用写bind() listen() accept()
        while True:
            conn = self.request
            addr = self.client_address
            
            recv_data = str(conn.recv(1024),encoding = 'utf8')
            print("recv from:" + str(addr) + ":" + recv_data)  # ('127.0.0.1', 50565)

            # 服务器端回复数据给客户端
            reply_index = random.randint(0, len(reply_list) - 1)
            reply = reply_list[reply_index]
            print("send:" + reply)
            
            send_data =  bytes(reply, encoding = 'utf8')
            conn.sendall(send_data)

        conn.close()
        
if __name__ == '__main__':

    random.seed(time.time())
    # 第一步
    #实例化server对象，传入本机ip，以及监听的端口号，还有新建的继承socketserver模块下的BaseRequestHandler类
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 9527), MyServer)
    #激活服务端
    server.serve_forever()