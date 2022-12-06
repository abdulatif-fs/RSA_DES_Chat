from Crypto.Cipher import DES
from secrets import token_bytes

key = b'halo1234'

def enkripsi(pesan):
    cipher = DES.new(key, DES.MODE_EAX)
    # print(cipher)
    nonce = cipher.nonce
    cipher_text, tag = cipher.encrypt_and_digest(pesan.encode('utf-8'))
    data= []
    data.append(cipher_text)
    data.append(tag)
    data.append(nonce)
    # print(cipher_text)
    return data

def dekrip(data):
    cipher_text = data[0]
    nonce = data[2]
    tag = data[1]
    cipher = DES.new(key, DES.MODE_EAX, nonce=nonce)
    # print(cipher)
    plain_text = cipher.decrypt(cipher_text)

    try:
        cipher.verify(tag)
        return plain_text.decode('utf-8')
    
    except:
        return 'salah tag'

# pesan = enkripsi(input("masukkan pesan anda: "))
# plain_text = dekrip(pesan)
# print('key = ',key)
# # print(f'Cipher text: {cipher_text}')
# # print('nonce = ', nonce)
# # print('tag = ', tag)

# if not plain_text:
#     print("file corrupt!!")
# else:
#     print(f'plain text: {plain_text}')