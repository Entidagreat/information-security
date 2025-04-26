def rotate_right(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def sigma0(x):
    return rotate_right(x, 2) ^ rotate_right(x, 13) ^ rotate_right(x, 22)

def sigma1(x):
    return rotate_right(x, 6) ^ rotate_right(x, 11) ^ rotate_right(x, 25)

def gamma0(x):
    return rotate_right(x, 7) ^ rotate_right(x, 18) ^ (x >> 3)

def gamma1(x):
    return rotate_right(x, 17) ^ rotate_right(x, 19) ^ (x >> 10)

def ch(x, y, z):
    return (x & y) ^ (~x & z)

def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def pad_message(message):
    message_bytes = [ord(c) for c in message]
    original_len_bits = len(message_bytes) * 8
    message_bytes.append(0x80)

    while (len(message_bytes) * 8 + 64) % 512 != 0:
        message_bytes.append(0x00)

    length_bytes = []
    for i in range(8):
        length_bytes.insert(0, original_len_bits & 0xFF)
        original_len_bits >>= 8

    return message_bytes + length_bytes

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def sha256(message):
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    padded = pad_message(message)
    print(f"[+] Bước 1 - Padding ({len(padded)} bytes / {len(padded)*8} bits):")
    print("Padded (hex):", ' '.join(f'{b:02x}' for b in padded))
    print()

    for chunk_start in range(0, len(padded), 64):
        chunk = padded[chunk_start:chunk_start + 64]
        print(f"[+] Bước 2 - Xử lý chunk từ byte {chunk_start} đến {chunk_start+63}")
        
        w = []
        for i in range(16):
            word = (chunk[4*i] << 24) | (chunk[4*i+1] << 16) | (chunk[4*i+2] << 8) | chunk[4*i+3]
            w.append(word)
        for i in range(16, 64):
            val = (gamma1(w[i-2]) + w[i-7] + gamma0(w[i-15]) + w[i-16]) & 0xFFFFFFFF
            w.append(val)

        print("[+] W[0..63]:")
        for i in range(64):
            print(f"  W[{i:02}] = {w[i]:08x}")
        print()

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        print("[+] Bước 5 - Vòng lặp chính:")
        for i in range(64):
            T1 = (h + sigma1(e) + ch(e, f, g) + K[i] + w[i]) & 0xFFFFFFFF
            T2 = (sigma0(a) + maj(a, b, c)) & 0xFFFFFFFF
            h = g
            g = f
            f = e
            e = (d + T1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xFFFFFFFF

            print(f"  Round {i:02}: a={a:08x}, b={b:08x}, c={c:08x}, d={d:08x}, e={e:08x}, f={f:08x}, g={g:08x}, h={h:08x}")

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

        print(f"[+] Kết thúc chunk: h0={h0:08x}, h1={h1:08x}, ..., h7={h7:08x}\n")

    final_hash = ''.join(f'{x:08x}' for x in [h0, h1, h2, h3, h4, h5, h6, h7])
    print(f"[✓] Kết quả SHA-256: {final_hash}")
    return final_hash

if __name__ == "__main__":
    input_text = input("Nhập chuỗi cần mã hóa SHA-256: ")
    sha256(input_text)
