from cryptography.fernet import Fernet

key = b'8xRgjJf-sCzyGPCHoBgWa7_1ufDEvWg3u0M7hh5zVHs='#Fernet.generate_key()
cipher_suite = Fernet(key)
credentials = "tomsmith"
encrypted_credentials = cipher_suite.encrypt(credentials.encode())

print("Encrypted credentials:", encrypted_credentials)
print("Encryption key:", key)
