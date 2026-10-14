# RSA

#### Category: Crypto - Event: Training 2026 - Ngày viết: 10/12/2026 - Đọc challenges: [Đọc](johan.py)

#### 1. Overview

* Đây là bài tập về nhà của các anh khóa trên giao xuống cho khóa 2k8 tài năng, mình được thg bạn cho ăn nhờ ở đậu nên biết đến file bài tập này. Bài khá là dễ nên mình tiện giải luôn :v
* `Mục tiêu`: Giải mã ciphertext bị mã hóa RSA
* `Lõ hỗng`: Gửi chung 1 bản rõ nhiều lần
* `Kỹ thuật`: Hastad’s Broadcast Attack

#### 2. Nền tảng cốt lõi

* Các bạn nên biết các lỗ hỗng phổ biến khi khóa công khai nhỏ nhé.
* RSA VÀ CÁC HÌNH THỨC TẤN CÔNG : [Đọc](https://hackmd.io/@nomorecaffeine/KCSC_task2). Bài viết do học viện kỹ thuật mật mã viết

#### 3. Phân tích lỗ hỗng

* Bài cho ta 2 file là file `output` và `johan`, file `johan` đơn giản chỉ mã hóa toàn bộ plaintext có trong list `messages`với điểm đặc biệt là tất cả các plaintext đều sử dụng `e = 3`, mở ra khá là nhiều cách tấn công khác nhau vào số mũ e nhỏ.

#### 4. Ý tưởng khai thác.

* Lúc đầu mình nghĩ nó chỉ là 1 bài có plaintext lưu trong ` messages`, chia nhỏ ra và mã hóa RSA và không được kèm theo padding, mình định bruteforce `k`cho 7 trường hợp, sau đó cộng các bytes bruteforce lại với nhau là ra cờ nhưng ngay ở trường hợp đầu tiên, mình đã bị treo máy
* ```Python
  from Crypto.Util.number import *
  import gmpy2

  def CrackingRSA(n,e,c):
      k = 0
      while True:
          root, ok = gmpy2.iroot(c + k * n, e)
          k += 1
          if ok:
              return long_to_bytes(root)
  def readfile(file):
      n = int(file.readline().strip().split(' ')[2])
      e = int(file.readline().strip().split(' ')[2])
      c = int(file.readline().strip().split(' ')[2])
      return n,e,c
  with open("output.txt") as f:
      flag = ""
      for i in range(7):
          n,e,c = readfile(f)
          flag += CrackingRSA(n,e,c)
  print(flag)
  ```
* Khi đọc kỹ lại source code hơn thì mình mới phát hiện là `messages` được lấy trong file `secret` =)))), nó không phải là chuỗi kí tự :v
* Lúc này mình lại nghĩ có khi cả list `messages`đều đang chứa cờ hoặc 1 đoạn tin nhắn nào đó giống nhau. MÌnh chuyển sang thủ thuật Hastad’s Broadcast Attack
* ```Python
  from Crypto.Util.number import *
  import gmpy2
  from sage.all import *

  def readfile(file):
      n = int(file.readline().strip().split(' ')[2])
      e = int(file.readline().strip().split(' ')[2])
      c = int(file.readline().strip().split(' ')[2])
      return (n,e,c)
  list_so = []
  with open("output.txt") as f:
      for i in range(7):
          list_so.append(readfile(f))
  list_mod = []
  list_cipher = []
  for i in list_so:
      list_mod.append(i[0])
      list_cipher.append(i[2])
  M = crt(list_cipher, list_mod)
  m, ok = gmpy2.iroot(M, 3)
  print(long_to_bytes(m))
  ```
* Nhưng rồi mình nhận được 1 đống bytes rác :v, khi in ra thử biến `ok` thì kết quả trả ra là False, có nghĩa là `M` không có căn bậc 3 nguyên. Mình có nghĩ đến các phương pháp tấn công khác như tấn công coppersmith khi biết 1 phần bản rõ nhưng mình thấy không khả thi :v
* Mình thử trường hợp khác, chỉ thử `Hastad’s Broadcast Attack` với 3 ciphertext khác nhau trong file. Mình thử điều này vì mình nghĩ có khi có dữ liệu rác mà tác giả thêm vào `messages` để  làm loạn thông tin. Và đây là trường hợp mình đã giải ra cờ :v

#### 5. Exploit chain

* Quy trình:

  * Nhập n,e,c vào 1 danh sách
  * Xét từng tổ hợp ciphertext chập 3 trong danh sách,  thực hiện `Hastad’s Broadcast Attack`, nếu `M` có căn bậc 3 nguyên thì in `m` ra.
* Script: [Đọc](newsol1.py)
* Kết quả:
* ```
  yes

  ---

  Johan Hastad
  Professor in Computer Science in the Theoretical Computer Science
  Group at the School of Computer Science and Communication at KTH Royal Institute of Technology in Stockholm, Sweden.

  crypto{1f_y0u_d0nt_p4d_y0u_4r3_Vuln3rabl3}
  ```
* ```
  crypto{1f_y0u_d0nt_p4d_y0u_4r3_Vuln3rabl3}
  ```
* Và thực sự anh đức đã bê nguyên challenges từ trên Cryptohack xuống =))))

#### 6. Reference

* RSA VÀ CÁC HÌNH THỨC TẤN CÔNG : [Đọc](https://hackmd.io/@nomorecaffeine/KCSC_task2)
