from cryptography.fernet import Fernet
from playwright_test.page_objects.helpers.password_vault import k


def decrypt(cred):
    cipher_suite = Fernet(k)
    decrypted_credentials = cipher_suite.decrypt(cred).decode()

    return decrypted_credentials
