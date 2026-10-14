# Round Keys

#### Course: `Symmetric Cryptography` - Cryptohack

#### 1. Overview

* Bài này bắt đầu cho ta thấy sự phức tạp của mã hóa AES

#### 2. Exploit chain

* Đối  với bài tập ở mục này thì chỉ đơn giản là xor 2 ma trận với nhau tạo ra ma trận mới, sau đó là in ma trận ra dưới dạng bytes. Thay gì sử dụng hàm `matrix2bytes`thì mình tích hợp cách giải vào luôn hàm `add_round_key`:v
* Script: [Đọc](add_round_key.py)
* ```
  crypto{r0undk3y}
  ```

#### 3. Ngoài lề

* Mình từ bài Bringing It All Together quay trở về bài này để nhắc nhở những ai đang học Course này, hãy cố gắng làm theo hướng dẫn của bài và đừng tự chế như mình =)))), debug mệt lắm
