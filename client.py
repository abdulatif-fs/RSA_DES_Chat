import socket
import select
import sys
import pick
import threading
import rsa

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nickname = input("Login dengan memasukkan nickname: ")
ip = "127.0.0.1"
port = 8080
privateK, publicK = rsa.main()
kuncides = 51
client.connect((ip, port))
pes = client.recv(1024)
pesan = pick.unpack(pes)
if pesan == 'NICK':
    awal = {'nick':nickname, 'PublicKey':publicK}
    client.send(pick.pack(awal))
elif pesan == 'PublicKey':
    awal = {'nick':nickname, 'PublicKey':publicK}
    client.send(pick.pack(awal))

def receive():
    global kuncides
    while True:
        try:
            pes = client.recv(1024)
            pesan = pick.unpack(pes)
            if pesan['nick'] != 'server':
                if pesan['r'] == 'inikunci':
                    kunci = pesan['key']['keyPu']
                    n = pesan['key']['n']
                    key = (int(kuncides)**int(kunci))%int(n)
                    print(key)
                    r = {'r':'inikuncides', 'nick':nickname, 'key':key, 'n':n}
                    client.send(pick.pack(r))
                elif pesan['r'] == 'inikuncides':
                    kuncide = pesan['key']
                    n = pesan['n']
                    
                    print(pesan['nick'],':' ,kuncide)
                    hasildekrip = rsa.dekrip(int(kuncide), privateK['keyPr'], n)
                    print(pesan['nick'],':', hasildekrip)
                else:
                    print(pesan['nick'],':' ,pesan['r'])
                
            else:
                print(pesan['nick'],':' ,pesan['r'])
                
        except:
            print(f'erorr sodaraa!!!')
            client.close()
            break

def ambilKey(nickname, client):
    r = {'r':'/mintakunci', 'nick':nickname}
    client.send(pick.pack(r))


def write():
    while True:
        inputan = input("")
        if inputan == '/user':
            r = {'r':inputan, 'nick':nickname}
            client.send(pick.pack(r))
        else:
            ambilKey(nickname, client)
            r = {'r':inputan, 'nick':nickname}
            client.send(pick.pack(r))
            # print('anda :', r['r'])

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()