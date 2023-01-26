import base64
import json
import secrets
import string
from getpass import getpass
from os.path import join
from sys import argv
from os import environ

HOME = environ['HOME']
VAULT = join(HOME, '.pnd', 'vault')
DATA = join(HOME, '.pnd', 'data')


def load():
    with open(DATA, 'r') as f:
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
        print('\npnd <pass name>|add|ls|rm|encrypt|decrypt|generate')
        print(
            """
→ `sudo pnd <name of password>` prints the password with a matching name to the console.

→ `sudo pnd add` an interactive tool to add/generate new passwords

→ `sudo pnd ls` prints of name of all saved passwords.

→ `sudo pnd rm` an interactive tool to remove passwords.

→ `sudo pnd encrypt` create an encrypted file named `~/.pnd/vault` to store your passwords safely using Fernet
  encryption with a PBKDF2 derived key. This file is safe to back up to the cloud (e.g. google-drive or github)
  
→ `sudo pnd decrypt` read the `~/.pnd/vault` into a `json` format that can replace your existing `pnd` file in
  case of data loss.
  
→ `pnd generate <length>` generate a secure password with a given length.
  Note that `pnd add` also gives you the option to automatically generate passwords.
            """)
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
        with open(DATA, 'w') as f:
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
            with open(DATA, 'w') as f:
                json.dump(x, f)
        else:
            print('Aborting.')
        exit(1)
    elif argv[1] == 'encrypt':
        try:
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        except ImportError:
            raise RuntimeError('The cryptography package is required for this functionality (pip install cryptography)')

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

        print(f'Writing encrypted data to {VAULT}')
        with open(VAULT, 'wb') as f:
            f.write(encrypted)

    elif argv[1] == 'decrypt':
        try:
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        except ImportError:
            raise RuntimeError('The cryptography package is required for this functionality (pip install cryptography)')

        password = getpass('Key: ')
        with open(VAULT, 'rb') as f:
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
        if len(argv) > 2:
            name = argv[2]
            json_data = json.loads(decrypted)
            if name not in json_data:
                print(f'No password for {name}')
                exit(1)
            print(json_data[name])
        else:
            print(decrypted)

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
