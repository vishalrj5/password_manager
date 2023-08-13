from cryptography.fernet import Fernet

key = b'J2-ezxXfvfCdKcO2MuxKyIrZMlvNjsSOfbcoqFnNrN8='

def encrypt_and_save(data):
    cipher_suite = Fernet(key)

    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    enc_lst = [encrypted_data, key]
    return enc_lst
    
def retrieve_and_decrypt(encrypted_data):
    
    
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data    

