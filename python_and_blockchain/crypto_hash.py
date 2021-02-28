import hashlib
import json

def crypto_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def main():
    print(f"crypto_hash('our data') : {crypto_hash('our data')}")

if __name__ == '__main__':
    main()