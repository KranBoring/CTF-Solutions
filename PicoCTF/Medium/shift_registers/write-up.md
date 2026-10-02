# shift registers

#### Category: Crypto - Diff: Medium

#### 1. Overview

* `Mục tiêu`: Bypass được Linear-feedback shift register để giải mã cờ
* `Lổ hỗng`: Có format cờ sẽ làm lộ ra seed byte khởi đầu mã hóa
* `Kỹ thuật`: Dùng format cờ để phục hồi seed byte đầu tiên

#### 2. Nền tảng cốt lõi

* Hiểu các toán tử bitwise
* Hiểu được khái niệm `Linear-feedback shift register` : [Đọc](https://en.wikipedia.org/wiki/Linear-feedback_shift_register)

#### 3. Phân tích lỗ hổng

* Phân tích hàm `steplfsr`:

* ```python
  def steplfsr(lfsr):
      b7 = (lfsr >> 7) & 1
      b5 = (lfsr >> 5) & 1
      b4 = (lfsr >> 4) & 1
      b3 = (lfsr >> 3) & 1
  
      feedback = b7 ^ b5 ^ b4 ^ b3
      lfsr = (feedback << 7) | (lfsr >> 1)
      return lfsr
  ```

* Hiểu đơn giản là lấy bit thứ 8, 6, 5, 4 xor với nhau, sau đó lùi các bit của byte qua bên trái và đưa bit mới lên đầu

* Đối với hàm `encrypt_lfsr`:

* ```python
  def encrypt_lfsr(pt_bytes):
      output = bytearray()
      lfsr = key & 0xFF
      for p in pt_bytes:
          lfsr = steplfsr(lfsr)
          ks = lfsr
          output.append(p ^ ks)
      return bytes_to_long(bytes(output))
  ```

* Seed khởi đầu của lfsr là bytes đầu tiên của key, có nghĩa là độ dài bytes key không có ý nghĩa ở đây vì khi vào lấy seed cho lfsr thì nó cũng chỉ lấy 1 bytes chính là bytes đầu tiên của key.

* Bắt đầu vòng lặp, chạy hàm `steplfsr` rồi lấy các kí tự cờ xor với bytes mới sau khi seed qua hàm `steplfsr`

* Như ta đã biết là format cờ là `academy{...}`, vậy kí tự `a` sẽ được xor với seed sau 1 lần qua hàm `steplfsr`, và lỗ hổng xuất hiện ở đây.

* Chỉ cần ta lấy kí tự `a` xor với kí tự hex đầu tiên của cipher, ta sẽ lấy được bytes đã xor với kí tự `a` hay chính là seed sau 1 lần qua hàm `steplfsr`. Ta lấy nó làm seed cho các kí tự giải mã tiếp theo, ta sẽ lấy được cờ.

#### 4. Exploit chain

* Quy trình:

  * Khôi phục lại bytes đã xor với kí tự `a` trong cờ, và đặt nó làm seed mới cho `lfsr`
  * Giải mã

* Script: [Đọc](solve.py)

* #### Flag: academy{l1n3ar_f33dback_sh1ft_r3g}

#### 5. Reference

* Linear-feedback shift register: [Đọc](https://en.wikipedia.org/wiki/Linear-feedback_shift_register)