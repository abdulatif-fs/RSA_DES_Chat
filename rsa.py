def find_e(z:int):
    e = z
    while e>=0:
        # print('e= ',e)
        if gcd(e, z)==1:
            break
            
        e-=1
    return e

def gcd(x:int, y:int):
    kecil, besar = (x, y) if x<y else (y, x)
    while kecil !=0:
        tmp = besar %kecil
        besar = kecil
        kecil = tmp
        # print('tmp: ',tmp)
    return besar

def find_d(e:int, z:int):
    d= 2
    while d<z:
        # print('d= ',d)
        if ((d*e)%z) == 1:
            return d
        d+=1
def main():
    # messege = input("masukkan pesan: ")
    p,q = 11, 17
    n = p*q
    on = (p-1)*(q-1)
    e= find_e(on)
    d = find_d(e, on)
    publicKey = {'keyPu':e, 'n':n}
    privateKey = {'keyPr':d, 'n':n}
    return privateKey, publicKey

def enkrip(messege, publicKey, n):
    data = ((int(messege))**publicKey['keyPu']) % n
    return data

def dekrip(data, privateKey, n):
    # print("enkrip = ", enkrip)
    data = (enkrip**privateKey['keyPr']) % n
    return data
    # print("dekrip = ",dekrip)