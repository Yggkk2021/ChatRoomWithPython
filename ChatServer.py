import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.AF_INET是表示IPv4,socket.SOCK_STREAM表示TCP连接

sock.bind(('localhost',5555))
sock.listen(5)

print('server listenning...')

mydict = dict()
mylist = list()

# 把whatToSay传给所有人exceptNum的所有人
def tellOthers(exceptNum,whatToSay):
    for c in mylist:
        if c.fileno() != exceptNum: # fileno()返回一个整型的文件描述符 例如：runoob.txt的文件描述符为3
            try:
                c.send(whatToSay.encode())
            except:
                pass

def subThreadIn(myconnection,connNumber):
    nickname = myconnection.recv(1024).decode() # recv() 接受TCP数据，数据以字符串返回。decode() 方法以 encoding 指定的编码格式解码字符串。
    mydict[myconnection.fileno()] = nickname
    mylist.append(myconnection)
    print('connection:',connNumber,'has nickname:',nickname)
    tellOthers(connNumber,'【系统提示：'+mydict[connNumber]+'进入服务器】')
    while True:
        try:
            recvedMsg = myconnection.recv(1024).decode()
            if recvedMsg:
                print(mydict[connNumber],':',recvedMsg)
                tellOthers(connNumber, mydict[connNumber] + ' :' + recvedMsg)
        except (OSError, ConnectionResetError):
            try:
                mylist.remove(myconnection)
            except:
                pass
            print(mydict[connNumber], 'exit, ', len(mylist), ' person left')
            tellOthers(connNumber, '【系统提示：' + mydict[connNumber] + ' 离开聊天室】')
            myconnection.close()
            return


while True:
    connection, addr = sock.accept()
    print('Accept a new connection', connection.getsockname(), connection.fileno())
    try:
        # connection.settimeout(5)
        buf = connection.recv(1024).decode()
        if buf == '1':
            connection.send(b'welcome to server!')

            # 为当前连接开辟一个新的线程
            mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
            mythread.setDaemon(True)
            mythread.start()

        else:
            connection.send(b'please go out!')
            connection.close()
    except:
        pass