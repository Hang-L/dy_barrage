import socket
import struct
import threading
import websocket
import time


def on_message(ws, message):
    #print(message)

    print(message.decode(encoding="utf-8",errors="ignore"))


def on_error(ws, error):
    print(ws)
    print(error)


def dy_encode(msg):
    # 头部8字节，尾部1字节，与字符串长度相加即数据长度
    # 为什么不加最开头的那个消息长度所占4字节呢？这得问问斗鱼^^
    data_len = len(msg) + 9
    # 字符串转化为字节流
    msg_byte = msg.encode('utf-8')
    # 将数据长度转化为小端整数字节流
    len_byte = int.to_bytes(data_len, 4, 'little')
    # 前两个字节按照小端顺序拼接为0x02b1，转化为十进制即689（《协议》中规定的客户端发送消息类型）
    # 后两个字节即《协议》中规定的加密字段与保留字段，置0
    send_byte = bytearray([0xb1, 0x02, 0x00, 0x00])
    # 尾部以'\0'结束
    end_byte = bytearray([0x00])
    # 按顺序拼接在一起
    data = len_byte + len_byte + send_byte + msg_byte + end_byte

    return data
def dy_encode2(msg):
    msg = msg.encode("utf-8")
    data_len = len(msg) + 8
    client_code = 689
    msg_len = struct.pack("<i", data_len)
    msg_head = msg_len + msg_len + struct.pack("<i", client_code) + msg
    print(msg_head)


def on_start(ws):
    print("open")
    login(ws)
    join_group(ws)
    heart_check_thread= threading.Thread(target=heart_check,args=(ws,))
    heart_check_thread.start()

def login(ws):
    req = "type@=loginreq/roomid@=9389523/"
    data= dy_encode(req)
    ws.send(data)

def join_group(ws):
    req = 'type@=joingroup/rid@=1126960/gid@=-9999/'
    data=dy_encode(req)
    ws.send(data)

def heart_check(ws):
    req="type@=mrkl/"
    data=dy_encode(req)
    while True:
        print("heart_check")
        ws.send(data)
        time.sleep(45)



def on_close(ws):
    print(ws)
    print("### closed ###")


if __name__ == '__main__':
    url = "wss://danmuproxy.douyu.com:8506/"
    websocket.enableTrace(True)
    ws=websocket.WebSocketApp(url,on_open=on_start,on_message=on_message,on_error=on_error,on_close=on_close)
    ws.run_forever()


