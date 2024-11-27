import threading
import random
import time

class Bank:
    def __init__(self):
        self.balance = 0  
        self.lock = threading.Lock() 

    def deposit(self):
        for _ in range(100):
            amount = random.randint(50, 500) 
            with self.lock:  
                self.balance += amount
                print(f"Пополнение: {amount}. Баланс: {self.balance}")
            time.sleep(0.001)  

    def take(self):
        for _ in range(100):
            amount = random.randint(50, 500)  
            print(f"Запрос на {amount}")
            with self.lock:  
                if amount <= self.balance: 
                    self.balance -= amount
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                else:
                    print("Запрос отклонён, недостаточно средств")
                   
                    while amount > self.balance:
                        self.lock.release()  
                        time.sleep(0.001)  
                        self.lock.acquire()  


bk = Bank()


th1 = threading.Thread(target=bk.deposit)
th2 = threading.Thread(target=bk.take)


th1.start()
th2.start()


th1.join()
th2.join()


print(f'Итоговый баланс: {bk.balance}')
