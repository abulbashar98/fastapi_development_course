import pytest
from app.calculations import add,subtract,divide,multiply,BankAccount,Insufficient_funds


@pytest.fixture
def uninitialized_bank_account():
    return BankAccount()

@pytest.fixture
def initialized_bank_account_with_hundred():
    return BankAccount(100)


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

def test_default_amount(uninitialized_bank_account):
    assert uninitialized_bank_account.balance == 0

def test_deposit(initialized_bank_account_with_hundred):
    # bank_account = BankAccount(15)
    initialized_bank_account_with_hundred.deposit(25)
    assert initialized_bank_account_with_hundred.balance == 125

def test_withdraw(initialized_bank_account_with_hundred):
    # bank_account = BankAccount(100)
    initialized_bank_account_with_hundred.withdraw(50)
    assert initialized_bank_account_with_hundred.balance == 50

def test_collected_interest(initialized_bank_account_with_hundred):
    # bank_account = BankAccount(50)
    initialized_bank_account_with_hundred.collect_interest()
    assert round(initialized_bank_account_with_hundred.balance, 5) == 110

@pytest.mark.parametrize("deposited, withdrew, final_amount", [
    (26, 13, 13),
    (50, 21, 29),
    (1500, 250, 1250),
    (2100, 900, 1200)
])
def test_bank_transaction(uninitialized_bank_account, deposited, withdrew, final_amount):
    uninitialized_bank_account.deposit(deposited)
    uninitialized_bank_account.withdraw(withdrew)
    assert uninitialized_bank_account.balance == final_amount

def test_insufficient_funds(initialized_bank_account_with_hundred):
    with pytest.raises(Insufficient_funds):
        initialized_bank_account_with_hundred.withdraw(200)