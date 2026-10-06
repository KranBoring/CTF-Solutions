# Mind your Ps and Qs

#### Category: Crypto - Diff: Medium

#### 1. Overview

* ![image-20261005101206541](images/image-20261005101206541.png)
* `Mục tiêu`: Phá giải RSA để giải mã cờ
* `Lỗ hỗng`: N nhỏ,dễ dàng bị phân tích thừa số nguyên tố

#### 2. Nền tảng cốt lõi

* Cần biết quá trình giải mã và mã hóa của RSA

#### 3. Phân tích lỗ hỗng

* Đề này cho ta 3 giá trị gồm:
  * `n`
  * `e`
  * `c`
* Hint: ![image-20261005101802913](images/image-20261005101802913.png)

#### 4. Ý tưởng khai thác

* Lý do RSA được phổ biến sử dụng rộng rãi là vì tính chất của nó
  * RSA sử dụng tính chất `RẤT KHÓ` phân tích các thừa số nguyên tố của 1 số bán nguyên tố khi số nguyên tố đủ lớn `(Áp dụng với công nghệ hiện tại, trong tương lai khi máy tính lượng tử ra mắt thì hầu hết các thuật toán RSA ngày nay đề sẽ bị phá nhanh chóng)` 
  * Khi số `N` bị phân tích thừa số nguyên tố là dấu chấm hết cho dữ liệu bị mã hóa bằng `N`, bởi vì kẻ tấn công có thể giải mã dữ liệu
* Với` N` trong RSA bài này chỉ dài cỡ 100 bit, trong khi `N` được coi là an toàn cần dài 1024 bit trở lên. Có nghĩa là mình chỉ cần phân tích thừa số nguyên tố của`N` là giải quyết được bài toán

#### 5. Exploit chain

* Quy trình:

  * Nhận các giá trị N,e,c
  * Lên trang [factordb.com](https://factordb.com/) để phân tích thừa số nguyên tố của `N`
  * Giải mã RSA

* Script: [Đọc](solve.py)

* #### Flag: academy{sma11_N_n0_g0od_a3ac7152}