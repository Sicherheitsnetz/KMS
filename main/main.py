import requests
import base64
import random
from flask import Flask, render_template, request

app = Flask(__name__)

deks = []
enc_deks = []
chunks = []
cipher = []

kek = ""
ckek = ""
a = ""
hex1 = ["0"]
hex2 = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

def createKek(ekmurl):
    print(" Getting user provided key ... ")
    x = requests.get(ekmurl)
    print(type(x))
    tmp = x.text
    kek = tmp.strip('"')
    print(type(kek))
    print(" [ KEK: " + kek + " ] " + "\n")
    return kek


def encryption(input):
    encrypted = ""
    dek = '0x' + str(random.choice(hex1)) + str(random.choice(hex2))
    deks.append(dek)
    print(" [ DEK: " + dek + " ] ", end= " ") 
    enc_deks.append(en_kek(dek))


    for i in range(len(input)):
        char = input[i]
        encrypted += chr((ord(char) + int(dek, base=16)))
    return encrypted

def decryption(input):
    decrypted = ""
    start = 5
    int_kmk = de_kek(input[:5])

    for i in range(start, len(input)):
        char = input[i]
        decrypted += chr(ord(char) - int(int_kmk, base=16) )

    return decrypted

def en_kek(dek):  
    enc_dek = hex(int(dek, base=16) + int(kek,base=16))
    return enc_dek

def de_kek(dek):
    dec_dek = hex(int(dek, base=8) - int(kek,base=16))
    return dec_dek


@app.route('/')
def showEkm():
    return render_template('index_copy_3.html', input=a, kek=kek, enc_deks=enc_deks, chunks=chunks, cipher=cipher, deks=deks)

@app.route('/envelope1')
def envelope1():
    return render_template("envelope1.html")

@app.route('/envelope')
def envelope():
    return render_template("envelope.html")

@app.route('/get', methods=["POST"])
def encrypt():
    result = request.form
    a = result["input"]
    kms = result["ekm"]
    ekmurl = request.form.get('URL')
    deks.clear()
    enc_deks.clear()

    global kek, ckek
    kek1 = "0x15"
    if kms == "Cust":
        kek2 = createKek(ekmurl)
        kek = hex(int(kek1, base=16) + int(kek2,base=16))
    else:
        kek = kek1

    cipher = []
    print(" Chunking and encrypting ... \n")
    chunks = (a.split())
    for i in range(len(chunks)):
        cipher.append(encryption(chunks[i]))
        print(" Chunk " + str(i) + ": " + cipher[i])
    return render_template('index_copy_3.html', input=a, kek=kek, enc_deks=enc_deks, chunks=chunks, cipher=cipher, deks=deks)

if __name__ == "__main__":
	app.run(host="localhost", port=int("8080"), debug=True)
