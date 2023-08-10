from pathlib import Path
import hashlib
import json
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


class StoreDecoder:
    def decode_store(self, data):
        encrypted_stores = data['context']['dispatcher']['stores']
        password_key = next(key for key in data.keys() if key not in ["context", "plugins"])
        password = data[password_key]

        encrypted_stores = b64decode(encrypted_stores)
        assert encrypted_stores[0:8] == b"Salted__"
        salt = encrypted_stores[8:16]
        encrypted_stores = encrypted_stores[16:]

        def EVPKDF(password, salt, keySize=32, ivSize=16, iterations=1, hashAlgorithm="md5") -> tuple:
            """OpenSSL EVP Key Derivation Function
            Args:
                password (Union[str, bytes, bytearray]): Password to generate key from.
                salt (Union[bytes, bytearray]): Salt to use.
                keySize (int, optional): Output key length in bytes. Defaults to 32.
                ivSize (int, optional): Output Initialization Vector (IV) length in bytes. Defaults to 16.
                iterations (int, optional): Number of iterations to perform. Defaults to 1.
                hashAlgorithm (str, optional): Hash algorithm to use for the KDF. Defaults to 'md5'.
            Returns:
                key, iv: Derived key and Initialization Vector (IV) bytes.
            Taken from: https://gist.github.com/rafiibrahim8/0cd0f8c46896cafef6486cb1a50a16d3
            OpenSSL original code: https://github.com/openssl/openssl/blob/master/crypto/evp/evp_key.c#L78
            """

            assert iterations > 0, "Iterations can not be less than 1."

            if isinstance(password, str):
                password = password.encode("utf-8")

            final_length = keySize + ivSize
            key_iv = b""
            block = None

            while len(key_iv) < final_length:
                hasher = hashlib.new(hashAlgorithm)
                if block:
                    hasher.update(block)
                hasher.update(password)
                hasher.update(salt)
                block = hasher.digest()
                for _ in range(1, iterations):
                    block = hashlib.new(hashAlgorithm, block).digest()
                key_iv += block

            key, iv = key_iv[:keySize], key_iv[keySize:final_length]
            return key, iv

        key, iv = EVPKDF(password, salt, keySize=32, ivSize=16, iterations=1, hashAlgorithm="md5")

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(encrypted_stores)
        plaintext = unpad(plaintext, 16, style="pkcs7")

        decoded_stores = json.loads(plaintext)
        return decoded_stores
