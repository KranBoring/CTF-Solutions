# Chinese Remainder Theorem

#### Course: `Modular Arithmetic`

#### 1. Overview

* Ở bài này chúng ta sẽ học về định lý số dư Trung Hoa. Đối với các bạn lập trình thi đấu ~~(giống mình)~~ thì có vẻ sẽ nghe qua định lý này 1 vài lần khi giải các bài toán rồi :v
* Các bạn có thể đọc chi tiết hơn tại wikipedia: [Đọc](https://vi.wikipedia.org/wiki/%C4%90%E1%BB%8Bnh_l%C3%BD_s%E1%BB%91_d%C6%B0_Trung_Qu%E1%BB%91c)
* Ở đây chúng ta chỉ sài sagemath để giải thôi chứ không đề cập sâu nhé, nhưng mình khuyên là các bạn nên đọc hiểu định lý này trước khi tự động hóa nó bằng code.

#### 2. Exploit chain

* Lập ra 2 list gồm các giá trị và module
* Tìm nghiệm của hệ phương trình đồng dư bằng hàm `crt` trong sagemath
* Script: [Đọc](solve.py)
* ```
  872
  ```
