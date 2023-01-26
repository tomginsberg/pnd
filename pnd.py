import base64
import json
import secrets
import string
from getpass import getpass
from os.path import join
from sys import argv
from os import environ

# check if cryptography package is installed
try:
    import cryptography

    cryptography_installed = True
except ImportError:
    cryptography_installed = False

if cryptography_installed:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def check_crypt_req():
    if not cryptography_installed:
        raise RuntimeError('The cryptography package is required for this functionality (pip install cryptography)')


ROOT = '/private/pass'
PND = join(ROOT, 'pnd')


def load():
    with open(PND, 'r') as f:
        x = json.load(f)
    return x


def generate(length=12):
    assert length >= 8, 'Password must be at least 8 characters long.'
    letters, digits, symbols = string.ascii_letters, string.digits, string.punctuation
    lower, upper = letters[:26], letters[26:]
    base_tokens = length // 4
    password = ''.join(secrets.choice(digits) for i in range(base_tokens))
    password += ''.join(secrets.choice(symbols) for i in range(base_tokens))
    password += ''.join(secrets.choice(lower) for i in range(length - 3 * base_tokens))
    password += ''.join(secrets.choice(upper) for i in range(base_tokens))
    password = secrets.SystemRandom().sample(password, len(password))
    return ''.join(password)


if __name__ == '__main__':
    if len(argv) == 1:
        print('pnd.py <pass name>|add|ls|rm|encrypt|decrypt|generate')
        exit(1)

    if argv[1] == 'add':
        name = input('Name: ')
        x = load()
        if name in x:
            print(f'Name {name} already exists.')
            remove = input('Remove? [y/N]: ')
            if remove.lower() == 'y':
                del x[name]
                print(f'Removed {name}.')
                print('Adding new entry.')
            else:
                exit(1)
        password = getpass('Password (empty to auto generate): ')
        if password == '':
            print('Generating 12 char password...')
            password = generate()
        else:
            confirmation = getpass('Confirm: ')
            if password != confirmation:
                print('Passwords do not match.')
                exit(1)
        print(f'Adding password <{"*" * len(password)}> for {name}')
        x = load()
        x[name] = password
        with open(PND, 'w') as f:
            json.dump(x, f)
    elif argv[1] == 'ls':
        x = load()
        for k in sorted(x.keys()):
            print(k)
    elif argv[1] == 'rm':
        name = input('Name: ')
        x = load()
        if name not in x:
            print(f'Name {name} does not exist.')
            exit(1)
        remove = input(f'Remove {name}? [y/N]: ')
        if remove.lower() == 'y':
            del x[name]
            print(f'Removed {name}.')
            with open(PND, 'w') as f:
                json.dump(x, f)
        else:
            print('Aborting.')
        exit(1)
    elif argv[1] == 'encrypt':
        check_crypt_req()
        print('Encrypting stored passwords...')
        password = getpass('Key: ')
        confirmation = getpass('Confirm Key: ')
        if password != confirmation:
            print('Keys do not match.')
            exit(1)
        data = load()
        json_data = json.dumps(data).encode()
        key = password.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'',
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(key))
        f = Fernet(key)
        encrypted = f.encrypt(json_data)

        print('Encrypted passwords:')
        print(encrypted)

        path = join(ROOT, 'vault')
        print(f'Writing encrypted data to {path}')
        with open(path, 'wb') as f:
            f.write(encrypted)

    elif argv[1] == 'decrypt':
        check_crypt_req()
        password = getpass('Key: ')
        path = join(ROOT, 'vault')
        with open(path, 'rb') as f:
            encrypted = f.read()

        key = password.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'',
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(key))
        f = Fernet(key)
        decrypted = f.decrypt(encrypted).decode()
        json_data = json.loads(decrypted)
        name = argv[2]
        print(json_data[name])

    elif argv[1] == 'generate':
        # generate a random password
        length = 12
        if len(argv) > 2:
            length = int(argv[2])
        assert length >= 8, 'Password must be at least 8 characters'
        print(generate(length))
    else:
        x = load()
        if argv[1] not in x:
            print(f'No password for {argv[1]}')
            exit(1)
        print(x[argv[1]])