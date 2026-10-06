# Tapping

#### Category: Crypto - Diff: Medium

#### 1. Overview

* ![image-20261006105624979](images/image-20261006105624979.png)
* `Mục tiêu`: Giải mã cipher
* `Kỹ thuật`: Morse decode

#### 2. Nền tảng cốt lõi	

* Mã Morse

#### 3. Phân tích

* Khi netcat đến server thì ta nhận được một chuỗi các kí tự `.` và  `-`
* ![image-20261006105805305](images/image-20261006105805305.png)
* Và đây là dấu hiệu của mã morse

#### 4. Exploit chain

* Quy trình:
  * Netcat đến server, copy mã morse
  * Dán vào trang [Morse decode](https://morsecode.world/international/translator.html) để giải mã
  * #### Flag: ACADEMY{M0RS3C0D31SFUN218CF979}