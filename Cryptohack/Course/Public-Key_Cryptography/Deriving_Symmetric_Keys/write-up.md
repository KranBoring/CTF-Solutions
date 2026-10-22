# Deriving Symmetric Keys

#### Course: `Public-Key Cryptography` - Cryptohack - Ngày viết: 21/10/2026

#### 1. Overview

* Ở bài này chúng ta sẽ sử dụng khóa chung để giải mã ciphertext
* `Mục tiêu`: Giải mã ciphertext

#### 2. Nền tảng cốt lõi

* Cần phải hoàn thành các bài Diffie Hellman trước đó trong Course này.
* Đọc hiểu source code mã hóa flag.

#### 3. Phân tích lỗ hỗng

* Source của đề:
* ```Python
  from Crypto.Cipher import AES
  from Crypto.Util.Padding import pad, unpad
  import hashlib
  import os
  from secret import shared_secret

  FLAG = b'crypto{????????????????????????????}'


  def encrypt_flag(shared_secret: int):
      # Derive AES key from shared secret
      sha1 = hashlib.sha1()
      sha1.update(str(shared_secret).encode('ascii'))
      key = sha1.digest()[:16]
      # Encrypt flag
      iv = os.urandom(16)
      cipher = AES.new(key, AES.MODE_CBC, iv)
      ciphertext = cipher.encrypt(pad(FLAG, 16))
      # Prepare data to send
      data = {}
      data['iv'] = iv.hex()
      data['encrypted_flag'] = ciphertext.hex()
      return data


  print(encrypt_flag(shared_secret))
  ```
* Khóa được dùng trong AES lấy 16 bytes đầu tiên của mã băm từ shared_secret

#### 4. Ý tưởng khai thác/Exploit chain

* Ta tính giá trị shared_secret, sau đó tính được key của AES, sau đó giải mã ciphertext
* Script: [Đọc](solve.py)
* ```
  crypto{sh4r1ng_s3cret5_w1th_fr13nd5}
  ```
* Bạn nào lười có thể quăng luôn vào source decrypt mà đề cho để giải mã :v
