from cryptography.fernet import Fernet

def load_key():
    return open(r"D:\Study material\miniproject\PriorNet\PriorNet\resources\Encryption_Decryption\secret.key",
                "rb").read()


def encrypt_message(message):
    """
        Encrypts message using pre stored key
    """
    key = load_key()
    encoded_message = message.encode("utf-8")
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    encrypted_message = encrypted_message.decode("utf-8")
    return encrypted_message

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message with reference to stored key
    """
    encrypted_message = encrypted_message.encode('utf-8')
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    return decrypted_message.decode('utf-8')

#print(encrypt_message(""))
#print(decrypt_message(""))