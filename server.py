import socket
import socketserver
from _thread import *
import pick
import select
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


ip = "127.0.0.1"
port = 8080

server.bind((ip, port))
server.listen(5)
print( '%s is Activated ...' % ip)
print('Listening on port %s ...' % port)
clients = []
nicknames =[]
puK = []
publickKey ={}
pesan = {}
a = 0
def handle(client, nickname):
    while True:
        try:
            pes = client.recv(1024)
            pesan = pick.unpack(pes)
            if pesan['r'] == '/user':
                daf = f'{nickname} : /user \ndaftar user aktif = '
                daf1 = pick.pack(daf)
                print('nickname yang terhubung = ', nicknames)
                r = {'r':nicknames, 'nick':'server'}
                client.send(pick.pack(r))
                    
            elif pesan['r'] == '/mintakunci':
                # nama = pesan.split(' ')[0]
                pengirim = pesan['nick']
                if pengirim == nicknames[1]:
                    penerima = nicknames[0]
                    a = 0
                    for pen in nicknames:
                        if penerima == nicknames[a]:
                            break
                        else:
                            a = a+1
                    kunci = puK[a]
                elif pengirim == nicknames[0]:
                    penerima = nicknames[1]
                    a = 0
                    for pen in nicknames:
                        if penerima == nicknames[a]:
                            break
                        else:
                            a = a+1
                    kunci = puK[a]
                r = {'r':'inikunci', 'nick':penerima, 'key':kunci}
                client.send(pick.pack(r))
            else:
                # pengirim = pesan['nick']
                # print(pesan['nick'], ':', pesan['r'])

                if pesan['nick'] == nicknames[1]:
                    penerima = nicknames[0]
                    a = 0
                    for pen in nicknames:
                        if pen == penerima:
                            break
                        else:
                            a = a+1
                    recv = clients[a]
                    recv.send(pick.pack(pesan))
                else:# pengirim == nicknames[0]:
                    penerima = nicknames[1]
                    a = 0
                    for pen in nicknames:
                        if pen == penerima:
                            break
                        else:
                            a = a+1
                    recv = clients[a]
                    recv.send(pick.pack(pesan))

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def tambahKey(*args):
    new_data = {}
    dict_data = args[0]
    for pair in dict_data:
        key, value = pair.split(':')
        if value.isdigit():
            value = int(value)
        new_data[key] = value
    return new_data


def receive():
    global a
    while len(nicknames)<=2:
        client, address = server.accept()
        print(f'{str(address)} Terhubung!')

        # client.send(pick.pack('NICK'))
        # nicknam = client.recv(1024)
        # nickname = pick.unpack(nicknam)
        r = {'r':'PublicKey', 'nick':'kosong'}
        client.send(pick.pack('PublicKey'))
        Key = pick.unpack(client.recv(1024))
        publickKey[a] = Key
        nickname = publickKey[a]['nick']
        public = publickKey[a]['PublicKey']
        nicknames.append(nickname)
        puK.append(public)
        clients.append(client)
        print(f'nickname client: {nickname}')
        print(f'public key {nickname} adalah {public}')

        if len(nicknames)<=1:
            r = {'r':'tunggu partner anda bergabung!', 'nick':'server'}
            tunggu = pick.pack(r)
            client.send(tunggu)

            thread = threading.Thread(target=handle, args=(client, nickname))
            thread.start()
        else:
            r = {'r':'anda dapat berkirim pesan!', 'nick':'server', 'kosong':'kosong'}
            terhubung = pick.pack(r)
            for clien in clients:
                clien.send(terhubung)


            thread = threading.Thread(target=handle, args=(client, nickname))
            thread.start()
        a+=1
receive()
