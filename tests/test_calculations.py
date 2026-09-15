from app.calculations import add,subtract,divide,multiply

def test_add():
    print("testing add function")
    sum = add(5,7)
    assert sum == 12 

def test_subtract():
    print("testing subtract function")
    result = subtract(8, 3)
    assert result == 6

def test_divide():
    print("testing divide function")
    result = divide(12, 2)
    assert result == 6

def test_multiply():
    print("testing multiply function")
    result = multiply(6,4)
    assert result == 24

