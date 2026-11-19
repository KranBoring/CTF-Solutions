# Very Smooth

#### Category: Cryptography - Difficulty: Hard - Ngày viết: 11/18/2026

#### 1. Overview

* ![1795017316271](image/write-up/1795017316271.png)
* `Mục tiêu`: Giải mã ciphertext
* `Lỗ hỗng`: $N$ có $p$ và $q$ là các số nguyên tố có $p -1, q - 1$ là các số trơn

#### 2. Nền tảng cốt lõi

* Các bạn cần biết thuật toán phân tích $N$ khi cấu trúc $N$ gồm các số nguyên tố lớn nhưng trơn
* Thuật toán `pollard p - 1` để phân tích $N$: [Đọc](https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm)

#### 3. Phân tích lỗ hỗng

* Mã nguồn server: [Đọc](gen.py)
* Bài này đồng tác giả với bài NSA_Backdoor, nên phương pháp sinh 2 số nguyên tố $p$ và $q$ của 2 bài hoàn toàn giống nhau. Các bạn có thể qua đọc phần phân tích lỗ hỗng của mình về cấu trúc số $N$: [Đọc](../NSA_Backdoor/write-up.md)

#### 4. Ý tưởng khai thác

* Ta chỉ cần thực hiện đòn tấn công `pollard p - 1`để phân tích thừa số $N$, sau đó chỉ là quá trình giải mã ciphertext

#### 5. Exploit chain

* Quy trình:
  * Phân tích thừa số $N$ bằng `pollard p - 1`
  * Giải mã ciphertext
* Script [Đọc](solve.py) - `Sử dụng toolkit cá nhân, thuật toán pollard p - 1 đã được wikipedia giải thích chi tiết:`[Xem tại đây](https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm)
* ```
  academy{p0ll4rd_f4ct0r1z4at10n_FTW_1e448555}
  ```
