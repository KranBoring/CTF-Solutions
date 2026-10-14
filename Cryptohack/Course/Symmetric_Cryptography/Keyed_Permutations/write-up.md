# Keyed Permutations

#### Course: Symmetric Cryptography - Cryptohack

#### 1. Overview

* Bài này giới thiệu cho chúng ta về khái niệm ánh xạ.

#### 2. Nền tảng cốt lõi

* Đối với các bạn sinh viên năm nhất học giải tích thì không lạ gì với khái niệm ánh xạ, nếu các bạn chưa biết thì đơn giản là ánh xạ chia ra 3 khái niệm chính.
  * Đơn ánh: [Đọc](https://vi.wikipedia.org/wiki/%C4%90%C6%A1n_%C3%A1nh)
  * Song ánh: [Đọc](https://vi.wikipedia.org/wiki/Song_%C3%A1nh)
  * Toàn ánh: [Đọc](https://vi.wikipedia.org/wiki/To%C3%A0n_%C3%A1nh)

#### 3. Exploit chain

* Thuật ngữ cho cụm từ `one-to-one`sẽ là đơn ánh -`injection`. Nhưng trong bối cảnh của bài này, thuật ngữ đúng cho cụm từ phải là song ánh - `bijection`bởi bị nếu nó là đơn ánh thì sẽ có những khối dữ liệu không thể ánh xạ qua khối mới. Nhưng thực tế chuyện này lại không xảy ra
* ```
  crypto{bijection}
  ```
