# Headshot

#### Steganography - Event: Deadface 2026 - Ngày viết: 19/10/2026

#### 1. Overview

* ![1792405405943](image/write-up/1792405405943.png)
* Đây là bài đầu tiên của mục Steganography của giải :v
* `Mục tiêu`: Tìm kiếm thông tin flag từ tệp ảnh đã cho

#### 2. Exploit chain

* Khi giải nén tài liệu zip của bài, ta nhận được 4 bức ảnh với bức thứ 3 được chia ra original và bình thường.
* ![1792405532417](image/write-up/1792405532417.png)
* Mình thử chiết xuất metadata để xem có dữ liệu gì không. Thì khi đến ảnh `headshot003.png`thì ta được như sau:
* ![1792405591902](image/write-up/1792405591902.png)
* ```
  deadface{b00m_h34Dsh0TTT}
  ```
