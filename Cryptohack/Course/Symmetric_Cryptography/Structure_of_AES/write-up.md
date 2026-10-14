# Structure of AES

#### Course: `Symmetric Cryptography` - Cryptohack

#### 1. Overview

* Đây là bài hướng dẫn chúng ta về quá trình mà mã hóa AES thực hiện

#### 2. Nền tảng cốt lõi

* Biết code thao tác trên ma trận
* Hiểu ma trận là gì

#### 3. Exploit chain

* Bài cho ta 1 bài tập python chứa 1 ma trận 4x4 chứa các bytes, nhiệm vụ là chuyển ma trận 4x4 đó về 1 chuỗi bytes dài 16 bytes để đọc
* Đơn giản là với mỗi hàng, ta lấy hết giá trị ra rồi chuyển đến hàng tiếp theo, lặp lại cho đến khi không còn hàng nào.
* Script: [Đọc](matrix.py)
* ```
  crypto{inmatrix}
  ```
