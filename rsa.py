import math

def gcd(a, b):
    """Tính ước chung lớn nhất của a và b."""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """Thuật toán Euclid mở rộng để tìm giá trị d sao cho d*a ≡ 1 (mod b)."""
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(e, phi):
    """Tìm nghịch đảo modulo của e trong mod phi."""
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise Exception('Không tồn tại nghịch đảo modulo')
    else:
        return x % phi

def is_prime(num):
    """Kiểm tra một số có phải số nguyên tố hay không."""
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def power_mod(base, exponent, modulus):
    """Tính (base^exponent) % modulus hiệu quả."""
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def generate_keys_with_custom_values(p, q, e=None):
    """Tạo khóa RSA với p, q cho trước và tùy chọn e."""
    # Xác nhận p và q là số nguyên tố
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("p và q phải là số nguyên tố")
        
    # Tính n và phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    # Nếu e không được cung cấp, cho phép người dùng nhập
    if e is None:
        while True:
            try:
                e = int(input(f"Nhập giá trị e (1 < e < {phi_n} và gcd(e, {phi_n}) = 1): "))
                if 1 < e < phi_n and gcd(e, phi_n) == 1:
                    break
                else:
                    print(f"Lỗi: e phải thỏa mãn 1 < e < {phi_n} và gcd(e, {phi_n}) = 1")
            except ValueError:
                print("Vui lòng nhập một số nguyên hợp lệ.")
    else:
        # Xác minh e và phi(n) là nguyên tố cùng nhau
        if not (1 < e < phi_n and gcd(e, phi_n) == 1):
            raise ValueError(f"e phải thỏa mãn 1 < e < {phi_n} và gcd(e, {phi_n}) = 1")
    
    # Tính d
    d = mod_inverse(e, phi_n)
    
    # Khóa công khai và khóa riêng
    public_key = (n, e)
    private_key = (n, d)
    
    return n, phi_n, e, d, public_key, private_key

def encrypt(message, public_key):
    """Mã hóa tin nhắn sử dụng khóa công khai."""
    n, e = public_key
    return power_mod(message, e, n)

def decrypt(ciphertext, private_key):
    """Giải mã bản mã sử dụng khóa riêng."""
    n, d = private_key
    return power_mod(ciphertext, d, n)

def main():
    print("=== Mã hóa bất đối xứng RSA ===")
    
    # Nhập p và q từ người dùng
    while True:
        try:
            p = int(input("Nhập số nguyên tố p: "))
            if is_prime(p):
                break
            else:
                print("Lỗi: p phải là số nguyên tố.")
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ.")
    
    while True:
        try:
            q = int(input("Nhập số nguyên tố q: "))
            if is_prime(q):
                break
            else:
                print("Lỗi: q phải là số nguyên tố.")
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ.")
    
    print(f"\nChọn 2 số nguyên tố p = {p}, q = {q}")
    
    try:
        # Tính các giá trị RSA
        n, phi_n, e, d, public_key, private_key = generate_keys_with_custom_values(p, q)
        
        print(f"\nTính n = p.q = {p}*{q} = {n}")
        print(f"Tính φ(n) = (p - 1).(q - 1) = {p-1}*{q-1} = {phi_n}")
        print(f"Chọn e = {e} (thỏa mãn 1 < e < φ(n) và gcd(e, φ(n)) = 1)")
        print(f"Tính d sao cho (d.e) mod φ(n) = 1 => d = {d}")
        print(f"\nKhóa công khai (public key): {public_key}")
        print(f"Khóa riêng (private key): {private_key}")
        
        # Yêu cầu người dùng nhập bản rõ
        while True:
            try:
                M = int(input("\nNhập bản rõ M = "))
                break
            except ValueError:
                print("Lỗi: Vui lòng nhập một số nguyên hợp lệ cho bản rõ M.")
            
        # Mã hóa
        C = encrypt(M, public_key)
        print(f"Mã hóa M thành C = {C}")
        
        # Giải mã
        M_decrypted = decrypt(C, private_key)
        print(f"Giải mã C thành M = {M_decrypted}")
        
        # Cho phép người dùng thử các giá trị khác nếu muốn
        while True:
            try:
                choice = input("\nBạn có muốn thử với một bản rõ khác không? (y/n): ")
                if choice.lower() not in ['y', 'n']:
                    print("Vui lòng nhập 'y' hoặc 'n'.")
                    continue
                
                if choice.lower() == 'n':
                    break
                
                M = int(input("Nhập bản rõ M = "))
                C = encrypt(M, public_key)
                print(f"Mã hóa M thành C = {C}")
                
                M_decrypted = decrypt(C, private_key)
                print(f"Giải mã C thành M = {M_decrypted}")
                
            except ValueError:
                print("Lỗi: Vui lòng nhập một số nguyên hợp lệ.")
            
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()