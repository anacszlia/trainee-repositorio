import hashlib

while True:
    resposta = input("Digite uma palavra: ")
    if (resposta == ""):
        break
        
    hash_sha1resposta = hashlib.sha1(resposta.encode())
    hash_hex_resposta = hash_sha1resposta.hexdigest()
    print("Hash SHA-1:", hash_hex_resposta)