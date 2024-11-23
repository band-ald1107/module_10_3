import threading
import time
import random


class Bank:
    def __init__(self):
        self.balance = 0  # Баланс банка
        self.lock = threading.Lock()  # Объект блокировки потоков

    def deposit(self):
        for _ in range(100):  # 100 транзакций пополнения
            amount = random.randint(50, 500)  # Случайное число от 50 до 500
            self.lock.acquire()  # Захватываем замок

            self.balance += amount
            print(f"Пополнение: {amount}. Баланс: {self.balance}")

            # Проверяем условие для разблокировки
            if self.balance >= 500:
                self.lock.release()  # Разблокируем, если баланс >= 500
                break

            self.lock.release()  # Освобождаем замок
            time.sleep(0.001)  # Имитация скорости выполнения

    def take(self):
        for _ in range(100):  # 100 транзакций снятия
            amount = random.randint(50, 500)  # Случайное число от 50 до 500
            print(f"Запрос на {amount}")

            self.lock.acquire()  # Захватываем замок

            if amount <= self.balance:
                self.balance -= amount
                print(f"Снятие: {amount}. Баланс: {self.balance}")
            else:
                print("Запрос отклонён, недостаточно средств")
                self.lock.release()  # Освобождаем замок, если недостаточно средств
                # Ждем, пока не станет достаточно средств
                while amount > self.balance:
                    time.sleep(0.001)  # Ожидание, чтобы не загружать процессор
                self.lock.acquire()  # Повторный захват, чтобы выполнить снятие
                self.balance -= amount
                print(f"Снятие: {amount}. Баланс: {self.balance}")

            self.lock.release()  # Освобождаем замок
            time.sleep(0.001)  # Имитация скорости выполнения


# Создаем объект класса Bank
bk = Bank()

# Создаем потоки для методов deposit и take
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

# Запускаем потоки
th1.start()
th2.start()

# Ожидаем завершения потоков
th1.join()
th2.join()

# Выводим итоговый баланс
print(f'Итоговый баланс: {bk.balance}')