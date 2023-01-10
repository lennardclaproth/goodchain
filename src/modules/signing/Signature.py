from cryptography.exceptions import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

class Signature:
        
    @staticmethod
    def generate_keys():
        private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
        public_key = private_key.public_key()
        prv_ser = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())
        pbc_ser = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return prv_ser, pbc_ser

    @staticmethod
    def sign(message, private_key):
        message = bytes(str(message), 'utf-8')
        ser_prv_key = serialization.load_pem_private_key(private_key, None)
        signature = ser_prv_key.sign(
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
            )
        return signature

    @staticmethod
    def verify(message, signature, pbc_ser):
        message = bytes(str(message), 'utf-8')
        public_key = serialization.load_pem_public_key(pbc_ser)
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
                )
            return True
        except InvalidSignature:
            return False
        except:
            print("Error executing 'public_key.verify'")
            return False