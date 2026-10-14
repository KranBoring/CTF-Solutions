# Passwords as Keys

#### Course: `Symmetric Cryptography`- Cryptohack

#### 1. Overview

* Đây là bài thứ 2 chúng ta bắt đầu thấy được rằng, việc đảm bảo khóa mã hóa của AES cần phải bảo mật đến mức nào. Chỉ cần biết được khóa được tạo ra 1 cách không ngẫu nhiên thì sẽ bị crack key ngay lập tức
* `Mục tiêu`: Khôi phục key mã hóa AES
* `Kỹ thuật`: Brute Force không gian tạo khóa

#### 2. Nền tảng cốt lõi

* Hiểu được luồng logic của code python

#### 3. Phân tích lỗ hỗng

* ```Python
  from Crypto.Cipher import AES
  import hashlib
  import random


  # /usr/share/dict/words from
  # https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words
  with open("/usr/share/dict/words") as f:
      words = [w.strip() for w in f.readlines()]
  keyword = random.choice(words)

  KEY = hashlib.md5(keyword.encode()).digest()
  FLAG = ?


  @chal.route('/passwords_as_keys/decrypt/<ciphertext>/<password_hash>/')
  def decrypt(ciphertext, password_hash):
      ciphertext = bytes.fromhex(ciphertext)
      key = bytes.fromhex(password_hash)

      cipher = AES.new(key, AES.MODE_ECB)
      try:
          decrypted = cipher.decrypt(ciphertext)
      except ValueError as e:
          return {"error": str(e)}

      return {"plaintext": decrypted.hex()}


  @chal.route('/passwords_as_keys/encrypt_flag/')
  def encrypt_flag():
      cipher = AES.new(KEY, AES.MODE_ECB)
      encrypted = cipher.encrypt(FLAG.encode())

      return {"ciphertext": encrypted.hex()}
  ```
* Ở bài này, key được tạo ra bằng cách lấy mã băm của 1 kí tự ngẫu nhiên trong file `words`.

#### 4. Ý tưởng khai thác

* Ở bài này, nếu chúng ta dùng đúng bản chất để nêu lên lỗ hỗng ở đây, thì số lượng khóa cần phải thử chỉ có trong không gian các khóa trong file `words`. Bởi vì các `word`trong file `words`được ánh xạ đến không gian `keys`. Chỉ với 1 `word`sẽ tạo ra 1 `key`, thử mọi giá trị trong file `words`. chắc chắn ta sẽ gặp được `key`đã mã hóa cờ. Bước băm ở đây không hề có  ý nghĩa gì về  mặt bảo mật ở đây :v

#### 5. Exploit chain

* Đầu tiên ta cần phải có tệp file words trước đã.
* Link chứa file `words` là: `https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words`. Ta gửi request đến để lấy file
* ```Shell
  curl https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words > words.txt
  ```
* Khi đã có tệp `words`, ta băm mọi từ có trong tệp bằng hàm băm `md5`, lưu thành tập danh sách `key`, ta thử mọi loại `key`cho đến khi ta gặp được cờ
* Script: [Đọc](solve.py)
* ```
  crypto{k3y5__r__n07__p455w0rdz?}
  ```
