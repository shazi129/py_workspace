import socketserver
import socket
import flatbuffers
from Flatbuffers_Proto import Message

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):

        conn = self.request
        addr = self.client_address
        print(conn)
        print(addr)

        while True:
            
            recv_raw_data = bytearray(conn.recv(1024))
            print("recv recv_raw_data:%s  %s" % (len(recv_raw_data), recv_raw_data))

            req = Message.Message.GetRootAsMessage(recv_raw_data, 0)
            msg = req.Msg()
            seq = req.Seq()
            print("recv msg:%s" % msg)

            rsp_msg = "server response msg seq[%s]" % seq
            builder = flatbuffers.Builder(0)
            rsp_msg = builder.CreateString(rsp_msg)

            Message.MessageStart(builder)
            Message.AddSeq(builder, seq)
            Message.AddMsg(builder, rsp_msg)
            rsp = Message.MessageEnd(builder)
            builder.Finish(rsp)

            conn.sendall(builder.Output())

        conn.close()
        

def test_serialize():
    builder = flatbuffers.Builder(0)
    rsp_msg = builder.CreateString("dddd")

    Message.MessageStart(builder)
    Message.AddSeq(builder, 0)
    Message.AddMsg(builder, rsp_msg)
    rsp = Message.MessageEnd(builder)
    builder.Finish(rsp)

    raw_data = builder.Output()
    print("recv recv_raw_data:%s  %s" % (len(raw_data), raw_data))
    req = Message.Message.GetRootAsMessage(raw_data, 0)
    msg = req.Msg()
    seq = req.Seq()
    print("%s   %s" % (seq, msg))


if __name__ == '__main__':
    # 第一步
    #实例化server对象，传入本机ip，以及监听的端口号，还有新建的继承socketserver模块下的BaseRequestHandler类
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 9527), MyServer)
    #激活服务端
    server.serve_forever()
    #test_serialize()