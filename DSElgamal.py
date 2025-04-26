import random
import math

def is_prime(n):
    """
    Check if a number is prime.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True

def is_primitive_root(alpha, p):
    """
    Check if alpha is a primitive root modulo p.
    """
    if pow(alpha, p-1, p) != 1:
        return False
    
    # Find the prime factors of p-1
    factors = set()
    n = p - 1
    
    # Find the factors of p-1
    for i in range(2, int(math.sqrt(n)) + 1):
        while n % i == 0:
            factors.add(i)
            n //= i
    if n > 1:
        factors.add(n)
    
    # Check if alpha^((p-1)/q) mod p != 1 for all prime factors q of p-1
    for q in factors:
        if pow(alpha, (p-1) // q, p) == 1:
            return False
    
    return True

def find_primitive_roots(p):
    """
    Find all primitive roots modulo p.
    """
    primitive_roots = []
    
    for alpha in range(2, p):
        if is_primitive_root(alpha, p):
            primitive_roots.append(alpha)
            
    return primitive_roots

def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm to find gcd(a, b) and coefficients x, y such that ax + by = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    else:
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

def mod_inverse(a, m):
    """
    Find the modular multiplicative inverse of a modulo m.
    """
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def elgamal_keygen(p, alpha):
    """
    Generate ElGamal key pair.
    p: prime number
    alpha: primitive root modulo p
    Returns: private key XA, public key YA
    """
    XA = random.randint(1, p-2)  # Private key
    YA = pow(alpha, XA, p)  # Public key
    
    return XA, YA

def elgamal_sign(message, p, alpha, XA, YA):
    """
    Generate ElGamal signature for a message.
    """
    print("\nChữ ký số ElGamal - Ban tạo chữ ký:")
    print(f"Tin nhắn m = {message}")
    
    # Step 1: Let Alice choose K such that 1 < K < p-1 and gcd(K, p-1) = 1
    while True:
        K_input = input(f"\nNhập giá trị K sao cho 1 < K < {p-1} và gcd(K, p-1) = 1: ")
        try:
            K = int(K_input)
            if 1 < K < p-1:
                gcd_value = math.gcd(K, p-1)
                if gcd_value == 1:
                    break
                else:
                    print(f"gcd(K, p-1) = gcd({K}, {p-1}) = {gcd_value} ≠ 1. Vui lòng chọn K khác.")
            else:
                print(f"K phải nằm trong khoảng (1, {p-1}). Vui lòng nhập lại.")
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ.")
    
    print(f"1. Ban chọn K = {K}, ta có gcd({K}, {p-1})={math.gcd(K, p-1)}")
    
    # Step 2: Calculate S1 = alpha^K mod p
    S1 = pow(alpha, K, p)
    print(f"2. Tính S1 = α^K mod p = {alpha}^{K} mod {p} = {S1}")
    
    # Step 3: Calculate K^-1 mod (p-1)
    K_inverse = mod_inverse(K, p-1)
    print(f"3. K^-1 mod(p-1) = {K}^-1 mod {p-1} = {K_inverse}")
    
    # Step 4: Calculate S2 = K^-1 * (m - XA*S1) mod (p-1)
    S2 = (K_inverse * (message - XA * S1)) % (p-1)
    print(f"4. S2 = K^-1 * (m - XA*S1) mod (p-1) = {K_inverse} * ({message} - {XA}*{S1}) mod {p-1} = {S2}")
    
    print(f"5. Chữ ký bao gồm cặp (S1, S2) = ({S1}, {S2})")
    
    return S1, S2

def elgamal_verify(message, S1, S2, p, alpha, YA, verifier_name="Ban Cua Ban"):
    """
    Verify ElGamal signature.
    """
    print(f"\n{verifier_name} xác thực chữ ký:")
    
    # Step 1: Calculate V1 = alpha^m mod p
    V1 = pow(alpha, message, p)
    print(f"1. Tính V1 = α^m mod p = {alpha}^{message} mod {p} = {V1}")
    
    # Step 2: Calculate V2 = (YA)^S1 * (S1)^S2 mod p
    V2 = (pow(YA, S1, p) * pow(S1, S2, p)) % p
    print(f"2. Tính V2 = (YA)^S1 * (S1)^S2 mod p = ({YA})^{S1} * ({S1})^{S2} mod {p} = {V2}")
    
    # Check if V1 = V2
    if V1 == V2:
        print(f"\nChữ ký hợp lệ bởi vì V1 = V2 = {V1}")
        return True
    else:
        print(f"\nChữ ký không hợp lệ bởi vì V1 = {V1} ≠ V2 = {V2}")
        return False



def main():
    print("LƯỢC ĐỒ CHỮ KÝ SỐ ELGAMAL")
    print("=========================")
    
    print("\nChọn chế độ:")
    print("1. Ban tạo chữ ký và Ban cua Ban xác thực")
    print("2. Người khác xác thực chữ ký")
    
    while True:
        mode_input = input("\nNhập lựa chọn (1 hoặc 2): ")
        if mode_input in ["1", "2"]:
            mode = int(mode_input)
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.")
    
    if mode == 1:
        # Mode 1: Alice generates signature and Bob verifies
        # Get prime number p
        while True:
            p_input = input("\nNhập số nguyên tố p (ví dụ:17, 19, 23, 29, 31,...): ")
            try:
                p = int(p_input)
                if is_prime(p):
                    break
                else:
                    print("Số nhập vào không phải là số nguyên tố. Vui lòng nhập lại.")
            except ValueError:
                print("Vui lòng nhập một số nguyên hợp lệ.")
        
        # Find and display primitive roots
        print("Đang tìm các căn nguyên thủy... (có thể mất một chút thời gian nếu p lớn)")
        primitive_roots = find_primitive_roots(p)
        print(f"\nTập các căn nguyên thủy của trường hữu hạn G*_{p}: {primitive_roots}")
        
        # Select alpha
        while True:
            alpha_input = input(f"\nChọn giá trị alpha từ danh sách căn nguyên thủy (ví dụ: {primitive_roots[0] if primitive_roots else 'không có'}): ")
            try:
                alpha = int(alpha_input)
                if alpha in primitive_roots:
                    break
                else:
                    print(f"Giá trị alpha = {alpha} không phải là căn nguyên thủy của {p}. Vui lòng chọn lại.")
            except ValueError:
                print("Vui lòng nhập một số nguyên hợp lệ.")
        
        # Alice's private key (XA)
        while True:
            XA_input = input(f"\nNhập khóa bí mật của Ban (XA) (1 < XA < {p-1}): ")
            try:
                XA = int(XA_input)
                if 1 < XA < p-1:
                    break
                else:
                    print(f"Khóa bí mật phải nằm trong khoảng (1, {p-1}). Vui lòng nhập lại.")
            except ValueError:
                print("Vui lòng nhập một số nguyên hợp lệ.")
        
        # Calculate Alice's public key (YA)
        YA = pow(alpha, XA, p)
        print(f"\nKhóa công khai của Ban: YA = α^XA mod p = {alpha}^{XA} mod {p} = {YA}")
        print(f"Tập khóa công khai: {{p, α, YA}} = {{{p}, {alpha}, {YA}}}")
        print(f"Khóa bí mật của Ban: XA = {XA}")
        
        # Get the message to sign
        while True:
            message_input = input(f"\nNhập tin nhắn m cần ký (0 ≤ m ≤ {p-1}): ")
            try:
                message = int(message_input)
                if 0 <= message <= p-1:
                    break
                else:
                    print(f"Tin nhắn phải nằm trong khoảng [0, {p-1}]. Vui lòng nhập lại.")
            except ValueError:
                print("Vui lòng nhập một số nguyên hợp lệ.")
        
        # Generate the signature
        S1, S2 = elgamal_sign(message, p, alpha, XA, YA)
        
        # Bob verifies the signature
        elgamal_verify(message, S1, S2, p, alpha, YA)
        
    
    else:  # mode == 2
        # Mode 2: Anyone verifies a signature
        # Get verifier's name
        verifier_name = input("\nNhập tên của người xác thực: ")
        
        # Get the public parameters
        while True:
            p_input = input("\nNhập số nguyên tố p (giá trị công khai): ")
            try:
                p = int(p_input)
                if is_prime(p):
                    break
                else:
                    print("Số nhập vào không phải là số nguyên tố. Vui lòng nhập lại.")
            except ValueError:
                print("Vui lòng nhập một số nguyên hợp lệ.")
        
        alpha_input = input("\nNhập giá trị của căn nguyên thủy alpha (giá trị công khai): ")
        alpha = int(alpha_input)
        
        YA_input = input("\nNhập khóa công khai của Ban (YA): ")
        YA = int(YA_input)
        
        message_input = input("\nNhập tin nhắn m cần xác thực: ")
        message = int(message_input)
        
        S1_input = input("\nNhập thành phần S1 của chữ ký: ")
        S1 = int(S1_input)
        
        S2_input = input("\nNhập thành phần S2 của chữ ký: ")
        S2 = int(S2_input)
        
        # Verify the signature
        elgamal_verify(message, S1, S2, p, alpha, YA, verifier_name)
        


if __name__ == "__main__":
    main()