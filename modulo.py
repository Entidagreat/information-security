def nghich_dao_modulo(a, m):
    m_original = m  # Lưu giá trị m ban đầu
    a_original = a  # Lưu giá trị a ban đầu
    
    # Khởi tạo y0, y1
    y0, y1 = 0, 1
    
    # In tiêu đề bảng
    print(f"{'Bước i':<8} {'m':<8} {'a':<8} {'r':<8} {'q':<8} {'y0':<8} {'y1':<8} {'y':<8}")
    print("-" * 64)
    
    # Tính bước 0
    r = m % a
    q = m // a
    y = y0 - q * y1
    
    # In bước 0
    print(f"{0:<8} {m:<8} {a:<8} {r:<8} {q:<8} {y0:<8} {y1:<8} {y:<8}")
    
    step = 0
    
    # Thuật toán Euclid mở rộng
    while r > 0:
        step += 1
        
        # Cập nhật giá trị cho bước tiếp theo
        m_new = a
        a_new = r
        y0_new = y1
        y1_new = y
        
        # Tính các giá trị mới
        r_new = m_new % a_new if a_new != 0 else 0
        q_new = m_new // a_new if a_new != 0 else None
        y_new = y0_new - q_new * y1_new if q_new is not None else None
        
        # In bước hiện tại
        print(f"{step:<8} {m_new:<8} {a_new:<8} {r_new:<8} {q_new if q_new is not None else '.':<8} {y0_new:<8} {y1_new:<8} {y_new if y_new is not None else '.':<8}")
        
        # Cập nhật giá trị cho vòng lặp tiếp theo
        m = m_new
        a = a_new
        r = r_new
        q = q_new
        y0 = y0_new
        y1 = y1_new
        y = y_new
        
        # Nếu r = 0, kết thúc thuật toán
        if r == 0:
            break
    
    # Kiểm tra xem a có khả nghịch hay không (gcd(a,m) = 1)
    if a != 1:
        return f"{a_original} không khả nghịch theo modulo {m_original}"
    
    # Điều chỉnh y1 để đảm bảo kết quả dương
    while y1 < 0:
        y1 += m_original
    
    return f"Kết quả: Nghịch đảo modulo {m_original} của {a_original} là {y1}. Vậy {a_original}^(-1) mod {m_original} = {y1}"

def main():
    try:
        a = int(input("Nhập số a: "))
        m = int(input("Nhập modulo m: "))
        
        if m <= 0:
            print("Modulo m phải lớn hơn 0")
            return
            
        # Kiểm tra UCLN của a và m
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
            
        if gcd(a, m) != 1:
            print(f"{a} không khả nghịch theo modulo {m} vì gcd({a},{m}) = {gcd(a,m)} != 1")
            return
            
        print(nghich_dao_modulo(a, m))
        
    except ValueError:
        print("Vui lòng nhập số nguyên hợp lệ")

if __name__ == "__main__":
    main()