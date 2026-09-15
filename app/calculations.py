def add(num1: int, num2: int = 2):
    return num1 + num2

def subtract(num1: int, num2: int = 1):
    return num1 - num2

def divide(num1: int, num2: 2):
    return round(num1/ num2)

def multiply(num1: int, num2: int = 2):
    return num1 * num2

class Insufficient_funds(Exception):
    pass

class BankAccount():
    def __init__(self,starting_balance=0):
        self.balance = starting_balance
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        if amount > self.balance:
            raise Insufficient_funds("Insufficient funds")
            # raise ZeroDivisionError
        self.balance -= amount
    def collect_interest(self):
        self.balance *= 1.1
    