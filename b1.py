_a = 16
_b = 3
_c = 5

print("1. Phép toán số học")
print(f"Tổng (_a + _b + _c): {_a + _b + _c}")
print(f"Hiệu (_a - _b): {_a - _b}")
print(f"Nhân (_a * _c): {_a * _c}")
print(f"Chia (_a / _b): {_a / _b}") 
print(f"Lũy thừa (_b ** _c): {_b ** _c}") 
print()

print("2. Toán tử quan hệ:")
print(f"_a > _b: {_a > _b}")
print(f"_b < _c: {_b < _c}")
print(f"_a == 16: {_a == 16}")
print(f"_b != _c: {_b != _c}")
print()

print("3. Toán tử gán:")
temp = _a  # Gán giá trị 16 vào biến temp
temp += _b # Tương đương temp = temp + _b
print(f"Cộng gán (temp += _b): {temp}")
temp /= _c # Tương đương temp = temp / _c
print(f"Chia gán (temp /= _c): {temp}")
temp *= 2  # Tương đương temp = temp * 2
print(f"Nhân gán (temp *= 2): {temp}")
print()


print("4. Toán tử logic:")
print(f"(_a > _b) and (_b < _c): {(_a > _b) and (_b < _c)}")
print(f"(_a < _b) or (_b < _c): {(_a < _b) or (_b < _c)}")
print(f"not (_a > _b): {not (_a > _b)}")
print()

print("5. Toán tử thao tác bit:")
print(f"_a & _b : {_a & _b}")
print(f"_a | _b : {_a | _b}")
print(f"_a ^ _b : {_a ^ _b}")
print(f"~_a : {~_a}")
print(f"_a << 3 : {_a << 3}")
print(f"_a >> 2 : {_a >> 2}")
print()