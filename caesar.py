def create_new_alphabet(keyword, shift):
    # Bảng chữ cái gốc
    original_alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    # Loại bỏ các ký tự trùng lặp trong từ khóa
    unique_keyword = ""
    for char in keyword.lower():
        if char in original_alphabet and char not in unique_keyword:
            unique_keyword += char
    
    # Tạo bảng chữ cái còn lại sau khi loại bỏ các chữ cái trong từ khóa
    remaining_chars = ""
    for char in original_alphabet:
        if char not in unique_keyword:
            remaining_chars += char
    
    # Dịch chuyển sang phải k chữ cái (lấy k chữ cuối đặt lên đầu)
    n = len(remaining_chars)
    k = shift % n  # Đảm bảo k nằm trong phạm vi hợp lệ
    
    shifted_first = remaining_chars[n-k:] if k > 0 else ""
    shifted_remaining = remaining_chars[:n-k] if k > 0 else remaining_chars
    
    # Tạo bảng chữ cái mới: phần đã dịch + từ khóa + phần còn lại
    new_alphabet = shifted_first + unique_keyword + shifted_remaining
    
    return original_alphabet, new_alphabet

def encrypt(plaintext, keyword, shift):
    original_alphabet, new_alphabet = create_new_alphabet(keyword, shift)
    
    # Mã hóa văn bản
    ciphertext = ""
    for char in plaintext.lower():
        if char in original_alphabet:
            index = original_alphabet.index(char)
            ciphertext += new_alphabet[index]
        else:
            ciphertext += char
    
    return ciphertext

def main():
    print("CHƯƠNG TRÌNH MÃ HÓA CAESAR VỚI TỪ KHÓA")
    print("----------------------------------------")
    
    plaintext = input("Nhập văn bản rõ: ")
    keyword = input("Nhập từ khóa: ")
    
    # Nhập k với ràng buộc từ 0-25
    while True:
        try:
            shift = int(input("Nhập độ dịch k (0-25): "))
            if 0 <= shift <= 25:
                break
            else:
                print("Giá trị k phải nằm trong khoảng từ 0 đến 25. Vui lòng nhập lại.")
        except ValueError:
            print("Vui lòng nhập một số nguyên cho độ dịch k.")
    
    ciphertext = encrypt(plaintext, keyword, shift)
    
    print("\nKết quả:")
    print(f"Văn bản rõ: {plaintext}")
    print(f"Từ khóa: {keyword}")
    print(f"Độ dịch k: {shift}")
    
    original_alphabet, new_alphabet = create_new_alphabet(keyword, shift)
    print(f"Bảng chữ cái gốc: {original_alphabet}")
    print(f"Bảng chữ cái mới: {new_alphabet}")
    
    print(f"Văn bản mã hóa: {ciphertext}")

if __name__ == "__main__":
    main()