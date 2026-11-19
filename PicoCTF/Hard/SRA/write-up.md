# SRA

#### Category: Cryptography - Difficulty: Hard - Ngày viết: 11/19/2026

#### 1. Overview

* ![1795052577114](image/write-up/1795052577114.png)
* Đây là 1 bài khá là hay khi mà chúng ta không có $N$ :v
* `Mục tiêu`: Giải mã ciphertext khi không có modulus $N$
* `Lỗ hỗng`: Kích thước $q, p$ nhỏ
* `Kỹ thuật`: Tìm các ứng cử viên $a$ là số nguyên tố và dài 128 bits, trong đó, $a - 1$ là ước của $ed - 1$

#### 2. Nền tảng cốt lõi

* Các bạn cần nắm được cách tính phi_euler trong RSA

#### 3. Exploit chain

* Mã nguồn server: [Đọc](chal.py) - `(đã được chuẩn hóa tên và biến)`
* Server chỉ cung cấp cho ta $C, d, e$, không cung cấp cho ta $N$ để giải mã $C$
* Ta biết được rằng $e \cdot d \equiv 1 \pmod {\phi(N)} \to ed - 1 = k \cdot (p - 1) \cdot (q  - 1)$
* Bởi vì $q, p$ chỉ có độ lớn 128 bits, ta kiểm tra toàn bộ các ước số của $ed - 1$, nếu như ước số $a - 1$ của $ed-1$ có độ lớn $127-128$ bits - ($127 < log2(a) < 128$) và $a$ là 1 số nguyên tố, thì ta đưa $a$ vào danh sách ứng viên làm số nguyên tố $q, p$
* Khi thu được toàn bộ các ứng viên $a$, ta ghép tổ hợp 2 ứng viên $a$ làm cặp $q , p$ và thử giải mã flag, nếu giải mã thành công (decode utf-8 thành công), $N$ chính là tích của cặp số nguyên tố $a$ đó.
* Script: [Đọc](solve.py)
* ```
  academy{7h053_51n5_4r3_n0_m0r3_6c44937a}
  ```

#### 4. Ngoài lề

* Các bạn có thể thử giải bài phiphai ở Wanna_game Freshman năm 2025 khi bài đó khung ý tưởng ra đề khá là giống nhưng cách giải khác 1 chút: [Xem thêm](https://github.com/KranBoring/CTF-Solutions/blob/main/Others-Events/2025/Wannagame_Freshman_2025/phiphai/source.py)
