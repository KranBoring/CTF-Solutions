# siege

#### Tags: Crypto - Diff: Easy

#### 1. Overview

* Một bài CTF dành cho newbie! Bài tập trung vào việc giải mã RSA và Brute force random seed. Bài này rất hay và thực sự khi giải được bài này, mình phải kiểu "Dude ma, Đỉnh vcl" =))))
* `Mục tiêu`: Giải mã RSA và khôi phục key để giải mã flag
* `Kỹ thuật`: Brute Force, Giải mã RSA, Research

#### 2. Nền tảng cốt lõi

* Đọc hiểu code python
* Hiểu cơ chế của sinh số giả ngẫu nhiên `PRNG`
* Biết cách giải mã `RSA` khi tìm được thừa số N
* Biết cách sử dụng class `AES` của thư viện `Crypto.Cipher`
* **Trong bài này, ae cố gắng nháp ra 1 tờ giấy để biết mình cần làm những gì nhé!, cố gắng tự giải trước khi đọc write-up**

#### 3. Phân tích lỗ hổng

* Đề cho ta 4 số lần lượt là:

  * `N`: Hợp số `(trong trường hợp của đề bài, không phải là số bán nguyên tố)` in dưới dạng hex, thành phần khóa công khai RSA
  * `C_key`: aes_key được mã hóa RSA thành `C_key`
  * `iv`: Vectơ khởi tạo của mã hóa AES
  * `ct`: ciphertext

* Bây giờ chúng ta cùng phân tích xem, để giải mã được ciphertext, ta cần làm những gì:

  * Để giải mã ciphertext, ta cần khởi tạo class AES gồm key và iv giống như trong [main.py](main.py):

  * ```python
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    ```

  * Ta đã có được `iv`, vậy thì ta cần tính được `aes_key`

    * `aes_key` được đổi thành `aes_int` bằng hàm:

    * ```pytho
      aes_int = int.from_bytes(aes_key, 'big')
      ```

    * Sau đó `aes_int` được mã hóa RSA thành `C_key`:

    * ```python
      C_key = pow(aes_int, E, N)
      ```

  * Chúng ta sẽ đi ngược từ các node lên để xem, để giải ciphertext ta cần làm gì:

    * Để giải `C_key` thành `aes_int`, ta cần biết khóa bí mật `D` . Để tìm được `D`, ta cần biết được `T` chính là Phi/Totient của N. Để tìm được `T`, ta phải biết được các thừa số nguyên tố của `N`
    * Để giải được `aes_key`, đơn giản chỉ là đảo ngược phép biến đổi

* Vậy thì để giải mã được flag, bài quy về giải RSA, tới đây mình nghĩ cách duy nhất để giải được challenge đó là tấn công số học vào cách tạo ra `N` để tìm thừa số nguyên tố của `N`

* `N` được tạo ra bằng cách:

* ```python
  primes = []
  for i in range(3, 8):
      seed = secrets.randbelow(2**i)
      rng = random.Random(seed)
      while True:
          p = rng._randbelow(1 << 256) | 1
          if isPrime(p):
              break
      primes.append(p)
  
  N = math.prod(primes)
  ```

* `N` sẽ bằng tích các số trong list `primes` và `primes` được tạo ra  ~~ngẫu nhiên~~ từ các hàm random

* Chú ý dòng 2,3 và 4 của code:

* ```python
  for i in range(3, 8):
      seed = secrets.randbelow(2**i)
      rng = random.Random(seed)
  ```

* `i` được khởi tạo chạy từ 3 đến 7 và `seed` được tính bằng cách random các số dưới `2 mũ i`, không gian số `seed` tối đa có thể nhận là từ [0,2 mũ 8-1] = [0, 127], không gian `seed` rất là nhỏ! (Chú ý chi tiết này)

* Khai báo `rng` là class Random nhận biến `seed` làm seed của class

* Phần còn lại của code chỉ là random cho đến khi nhận được số nguyên tố và đẩy vào list

* Như chúng ta được biết ~~(Không biết thì xuống mục 5)~~, khi class Random nhận 1 seed thì các giá trị tạo ra tiếp theo sau khi khởi tạo 1 seed giống nhau luôn giống nhau trong mọi trường hợp. Vì vậy, ta sẽ brute force không gian seed để tìm ra các thừa số nguyên tố tạo ra `N` !

* Khi phân tích được thừa số nguyên tố N, phần còn lại chỉ là đảo ngược các phép biến đổi.

#### 4. Exploit chain

* Quy trình:
  * Brute Force không gian seed để tìm lại các thừa số nguyên tố tạo ra `N`.
  * Tính Totient của `N` 
  * Khôi phục khóa `D`
  * Giải mã `C_key`
  * Biến đổi `aes_int` thành `aes_key`
  * Giải mã AES
  * unpad flag

* Script: [Đọc](solve.py)

* #### Flag: OSC{5efca16a840359db72cae08a12d2784422f95d8afd12a64346e6ce4ea2431fb8}

#### 5. Reference

* Convert back from int to byte: [Đọc](https://stackoverflow.com/questions/59023249/convert-back-from-int-to-byte)
* AES: [Đọc](https://www.studocu.vn/vn/document/hoc-vien-cong-nghe-buu-chinh-vien-thong/an-toan-ung-dung-web-va-co-so-du-lieu/tim-hieu-ve-advanced-encryption-standard/72096344?sid=56d888d0-c0fd-4741-a76f-24feb99a6d3a1790691286)
* rng: [Đọc](https://en.wikipedia.org/wiki/Random_number_generation)
* Random có ngẫu nhiên? :[Đọc](https://viblo.asia/p/ham-random-trong-python-co-thuc-su-ngau-nhien-ORNZqxvqK0n)
* Padding AES: [Đọc](https://viblo.asia/p/symmetric-ciphers-mat-ma-doi-xung-aes-phan-6-0gdJzD6eVz5)
* Cách tính Totient (nên xem mục này trước khi giải và đọc solve code): [Đọc](https://en.wikipedia.org/wiki/Euler%27s_totient_function)
* Thông tin các hàm Python được sử dụng trong solve và main:
  * class Random: [Đọc](https://docs.python.org/3/library/random.html#:~:text=class%20random.-,SystemRandom,-(%5Bseed))
  * math.prod(): [Đọc](https://www.w3schools.com/python/ref_math_prod.asp)

