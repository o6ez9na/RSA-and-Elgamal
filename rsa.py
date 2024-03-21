import random  # Импорт модуля random для генерации случайных чисел
from sympy import isprime  # Импорт функции isprime из модуля sympy для проверки числа на простоту
import shuffles  # Импорт собственного модуля shuffles, предположительно содержащего функции для перестановки байтов


# Функция для преобразования строки в список чисел ASCII-кодов символов
def to_ascii(message):
    result = []
    for i in range(len(message)):
        result.append(ord(message[i]))
    return result


# Функция для генерации простого числа заданной битовой длины
def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if isprime(p):
            return p


# Расширенный алгоритм Евклида для нахождения обратного по модулю числа
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


# Функция для вычисления обратного элемента по модулю
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g == 1:
        return x % m


# Функция для генерации пары ключей RSA
def generate_keypair(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Обычно используют значение e=65537 (2^16 + 1)
    d = modinv(e, phi)
    return (e, n), (d, n), p, q


# Функция для шифрования сообщения с использованием открытого ключа
def encrypt(public_key, plaintext, flag):
    e, n = public_key
    tmp_array = to_ascii(plaintext)
    cipher = []
    if flag:
        result_array = shuffles.byte_shuffle(tmp_array)  # Перестановка байтов, если флаг установлен
        for char in result_array:
            cipher.append(pow(char, e, n))  # Шифрование каждого символа в сообщении
        return cipher
    else:
        for char in tmp_array:
            cipher.append(pow(char, e, n))  # Шифрование каждого символа в сообщении
        return cipher


# Функция для дешифрования сообщения с использованием закрытого ключа
def decrypt(private_key, ciphertext, flag):
    d, n = private_key
    if flag:
        plain = [pow(char, d, n) for char in ciphertext]  # Дешифрование каждого символа в сообщении
        rtl_array = shuffles.byte_unshuffle(plain)  # Обратная перестановка байтов
        result_array = [chr(symbol) for symbol in rtl_array]
        return ''.join(result_array)  # Преобразование списка символов обратно в строку
    else:
        plain = [chr(pow(char, d, n)) for char in ciphertext]  # Дешифрование каждого символа в сообщении
        return ''.join(plain)  # Преобразование списка символов обратно в строку


# Функция для выполнения процесса RSA шифрования/дешифрования сообщения
def rsa_run(message, flag):
    public_key, private_key, p, q = generate_keypair(128)  # Генерация пары ключей с заданной длиной
    encrypted_message = encrypt(public_key, message, flag)  # Шифрование сообщения
    decrypted_message = decrypt(private_key, encrypted_message, flag)  # Дешифрование сообщения
    return encrypted_message, decrypted_message, public_key, private_key, p, q
