import pytest
from app.calculations import add,subtract,divide,multiply,BankAccount


@pytest.mark.parametrize("num1, num2, expected", [
    (4,5,9),
    (12,5,17),
    (31,5,36),
    (17,15,32)
])
def test_add(num1, num2, expected):
    assert add(num1,num2) == expected 

def test_subtract():
    print("testing subtract function")
    result = subtract(8, 3)
    assert result == 5

def test_divide():
    print("testing divide function")
    result = divide(12, 2)
    assert result == 6

def test_multiply():
    print("testing multiply function")
    result = multiply(6,4)
    assert result == 24

def test_set_initial_balance():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_starting_balance():
    bank_account = BankAccount()
    assert bank_account.balance == 0

def test_deposit():
    bank_account = BankAccount()
    bank_account.deposit(25)
    assert bank_account.balance == 25

def test_withdraw():
    bank_account = BankAccount(100)
    bank_account.withdraw(50)
    assert bank_account.balance == 50

def test_collected_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 5) == 55