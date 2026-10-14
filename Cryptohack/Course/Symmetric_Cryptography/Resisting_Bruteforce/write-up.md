# Resisting Bruteforce

#### Course: Symmetric Cryptography - Cryptohack

#### 1. Overview

* Bài này cho chúng ta thông tin bảo mật hiện nay của mã hóa `AES`

#### 2. Nền tảng cốt lõi

* Thực tế với sức mạnh tính toán của máy tính hiện nay, việc phá mã AES khi không biết key bằng phương pháp bruteforce gần như là không thể nào phá được. Với độ dài key 128 bit thì dù chuyển toàn bộ sức mạnh của các máy tính đang đào bitcoin hiện nay trên thế giới này cùng phá mã AES thì cũng phải trải qua hàng trăm lần tuổi vũ trũ mới có thể phá được

#### 3. Exploit chain

* Có 1 loại hình tấn công vào AES đã giảm độ khó từ `2^128`còn `2^126.1`. Về mặt lý thuyết, nó giúp giảm tốc độ phá mã lên tới gấp 4 lần, nhưng lượng tính toán vẫn rất khủng khiếp và không thực tế.
* Và tên cuộc tấn công đơn khóa tốt nhất dành cho AES là Biclique attack
* ```
  crypto{biclique}
  ```
