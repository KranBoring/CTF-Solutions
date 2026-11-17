# b00tl3gRSA3

#### Category: Cryptography - Difficulty: Hard - Ngày viết: 11/16/2026

#### 1. Overview

* ![1794842868779](image/write-up/1794842868779.png)
* `Mục tiêu`: Phân tích thừa số nguyên tố $N$, tính $\phi(N)$ và giải mã flag
* `Lỗ hỗng`: Tích nhiều số nguyên tố nhỏ

#### 2. Exploit chain

* Ta sử dụng hàm `factor` đã được tối ưu của sagemath để tìm thừa số nguyên tố $N$, sau đó, ta dùng công thức gốc của euler để tính cấp của nhóm nhân $N$ là $\phi(N) = n \prod_{p \mid n} \left(1 - \frac{1}{p}\right)$
* Script: [Đọc](solve.py)
* ```
  academy{too_many_fact0rs_5984067}
  ```
