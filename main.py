import random
from math import gcd
def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def is_prime(n, tests=5):
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(tests):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n -1:
            continue
        for _ in range(r -1):
            x = pow(x, 2, n)
            if x == n -1:
                break
        else:
            return False
    return True

def generate_prime_number(length=16):
    while True:
        p = generate_prime_candidate(length)
        if is_prime(p):
            return p
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd_, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd_, x, y

def modinv(e, phi):
    gcd_, x, _ = egcd(e, phi)
    if gcd_ != 1:
        raise Exception('Нет обратного элемента')
    else:
        return x % phi
def generate_keys():
    print("Генерация простых чисел p и q...")
    p = generate_prime_number()
    q = generate_prime_number()
    while q == p:
        q = generate_prime_number()

    print(f"p={p}, q={q}")

    n = p * q
    phi = (p -1) * (q -1)
    e = 65537
    if gcd(e, phi) != 1:
        e = random.randrange(2, phi)
        while gcd(e, phi) != 1:
            e = random.randrange(2, phi)

    d = modinv(e, phi)

    public_key = (e, n)
    private_key = (d, n)

    print(f"Публичный ключ: {public_key}")
    print(f"Приватный ключ: {private_key}")

    return public_key, private_key

def encrypt(public_key, plaintext):
    e, n = public_key
    plaintext_bytes = plaintext.encode('utf-8')
    cipher_numbers = [pow(byte, e, n) for byte in plaintext_bytes]
    return cipher_numbers

def decrypt(private_key, ciphertext):
    d, n = private_key
    decrypted_bytes = bytes([pow(c, d, n) for c in ciphertext])
    return decrypted_bytes.decode('utf-8')

if __name__ == "__main__":
    public_key, private_key = generate_keys()

    message = "Привет! Это тестовое сообщение."
    
    print(f"\nИсходное сообщение: {message}")
    
    encrypted_message = encrypt(public_key, message)
    
    print(f"\nЗашифрованное сообщение: {encrypted_message}")
    
    decrypted_message = decrypt(private_key, encrypted_message)
    
    print(f"\nРасшифрованное сообщение: {decrypted_message}")


    print("Конец")
