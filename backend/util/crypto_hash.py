import hashlib
import json

def crypto_hash(*args):
    stringified_data = sorted(map(lambda data: json.dumps(data),args))
    joined_data = ''.join(stringified_data)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"crypto_hash('our data') : {crypto_hash('our data', 'bla', [1,2,3])}")

if __name__ == '__main__':
    main()















