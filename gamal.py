from random import randint
import shuffles
from rsa import isprime


# Функция вычисления значения y по алгоритму Эль-Гамаля
def Y(g, p, x):
    return (g ** x) % p


# Функция генерации простых чисел и ключей
def generate_primary(N):
    while True:
        while True:
            p = randint(1000, N)  # Генерация случайного числа p в диапазоне [1000, N]
            if isprime(p):  # Проверка, является ли p простым числом
                break
        while True:
            g = randint(1000, p)  # Генерация случайного числа g в диапазоне [1000, p]
            if isprime(g):  # Проверка, является ли g простым числом
                break
        while True:
            X = randint(1000, p)  # Генерация случайного числа X в диапазоне [1000, p]
            if isprime(X):  # Проверка, является ли X простым числом
                break
        if p != g and p != X and g != X:  # Условие, чтобы p, g и X были различными
            y = Y(g, p, X)  # Вычисление значения y
            if y > 100:  # Условие на минимальное значение y
                return y, g, p, X


# Функция преобразования сообщения в ASCII
def to_ascii(message):
    result = []  # Создание пустого списка для хранения ASCII кодов символов
    for i in range(len(message)):
        result.append(ord(message[i]))  # Преобразование каждого символа сообщения в его ASCII код и добавление в список
    return result


# Функция шифрования сообщения
def encrypt(g, p, y, message, flag):
    post_message = to_ascii(message)  # Преобразование сообщения в список ASCII кодов
    if flag:
        reg_message = shuffles.byte_shuffle(post_message)  # Перемешивание ASCII кодов символов сообщения
        while True:
            k = randint(1, p - 1)  # Генерация случайного числа k в диапазоне [1, p - 1]
            if isprime(k):  # Проверка, является ли k простым числом
                A = (g ** k) % p  # Вычисление значения A
                B = []  # Создание пустого списка для хранения зашифрованных данных
                for i in range(len(reg_message)):
                    B.append((y ** k) * reg_message[i] % p)  # Вычисление значения B для каждого символа
                return A, B  # Возвращение пары (A, B)
    else:
        while True:
            k = randint(1, p - 1)  # Генерация случайного числа k в диапазоне [1, p - 1]
            if isprime(k):  # Проверка, является ли k простым числом
                A = (g ** k) % p  # Вычисление значения A
                B = []  # Создание пустого списка для хранения зашифрованных данных
                for i in range(len(post_message)):
                    B.append((y ** k) * post_message[i] % p)  # Вычисление значения B для каждого символа
                return A, B  # Возвращение пары (A, B)


def decrypt(A, B, X, p, flag):
    if flag:  # Если флаг установлен
        tmp_array = []  # Создание временного списка для хранения расшифрованных ASCII кодов символов
        for value in B:
            # Расшифровка ASCII кодов символов и добавление в список
            tmp_array.append(int(value * A ** (p - 1 - X) % p))
        byte_array = shuffles.byte_unshuffle(tmp_array)  # Восстановление исходного порядка символов
        result = ''  # Создание пустой строки для хранения расшифрованного сообщения
        for value in byte_array:
            result += chr(value)  # Преобразование ASCII кодов в символы и добавление в строку
        return result  # Возвращение расшифрованного сообщения
    else:  # Если флаг не установлен
        result = ''  # Создание пустой строки для хранения расшифрованного сообщения
        for value in B:
            result += chr(int(value * A ** (p - 1 - X) % p))  # Преобразование ASCII кодов в символы и добавление в строку
        return result  # Возвращение расшифрованного сообщения


def gamal_run(message, flag):
    y, g, p, X = generate_primary(4095)  # Генерация простых чисел и ключей
    A, B = encrypt(g, p, y, message, flag)  # Шифрование сообщения
    return y, g, p, X, A, B, decrypt(A, B, X, p, flag)  # Возвращение результатов шифрования и дешифрования
