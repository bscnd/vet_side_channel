from aes import AES, bytes2matrix, matrix2bytes, sbox_output, leakage_model_first_round
import os
import numpy as np

def main():
    iv = os.urandom(16)
    master_key = os.urandom(16)
    aes_tool = AES(master_key)

    # Test encryption / decryption
    cipher_text = aes_tool.encrypt_block(b'aaaaaaaaaaaaaaaa')
    plain_text = aes_tool.decrypt_block(cipher_text)
    assert plain_text == b'aaaaaaaaaaaaaaaa'

    # Expand key
    all_keys = AES._expand_key(aes_tool, master_key)
    print(str(all_keys) + "\n")                     # Affiche toutes les clés
    k10 = all_keys[-1]                              # On récupère la dernière clé (k10)
    print("k10 : " + str(k10))                      # On l'affiche
    print("k10 passe du type 'list of bytes' à 'bytes'")
    k10 = b''.join(k10)                             # On passe k10 en bytes
    
    print("Master Key : " + str(master_key))
    print("type master key" + str(type(master_key)) + "\n")

    # Reverse expand key
    i = 10
    for round_key in AES.inverse_expand_key(aes_tool, k10):
        print ("Round " + str(i) + " : " + str(round_key) + "\n")
        i-=1  
    print("First Key : " + str(round_key)) 
    round_key=bytes2matrix(round_key)
    print(round_key)  

    print("Master Key : " + str(master_key))
    master_key=bytes2matrix(master_key)
    print(str(master_key) + "\n")

    # Test sbox_output
    plaintext = b'aaaaaaaaaaaaaaaa'
    master_key = b'aaaaaaaaaaaaaaaa'
    n_octet = 0
    sbox = sbox_output(plaintext[n_octet], master_key[n_octet])  # En décimal, à passer en hexa pour retrouver les valeurs de la table (99 = 0x63)
    print("Sortie de la SBox au premier tour d'AES pour l'octet n° " + str(n_octet) + " : " + str(sbox))

    #Test leakage_model
    data = np.load("D:\Léo\Documents\\0-Etudes\\M2_Cyber\\Projet_SCA\\topic_M2\data\software_traces_k_known\\plaintext.npy")
    result = leakage_model_first_round(data,master_key[n_octet], 0)
    print(result)

   
    
if __name__ == "__main__":
    main()
