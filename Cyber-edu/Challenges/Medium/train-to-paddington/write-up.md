# train-to-paddington

#### Tags: Crypto - Diff: Medium

#### 1. Overview

* `Muc tiêu`: Giải mã ciphertext đã bị xor với key
* `Kỹ thuật`: Khôi phục key bằng format cờ và padding

#### 2. Nền tảng cốt lõi

* Hiểu cách hoạt động của phép xor

#### 3. Phân tích lỗ hổng

* Đây là 1 challenges white box, khi phân tích mã nguồn mã hóa của server, ta có được những điều sau:

  * ```python
    def pad_pt(pt):
        amount_padding = 16 if (16 - len(pt) % 16) == 0 else 16 - len(pt) % 16
        return pt + (b'\x3f' * amount_padding)
    ```

  * Flag sẽ được them pad sao cho độ dài của flag chia hết cho 16

  * ```python
    key = os.urandom(BLOCK_SIZE)
    ```

  * Key là 1 chuỗi bytes dài 16 bytes

  * Output là cờ đã được xor với key

* Ta đã biết format cờ là `TCFCTF{` và đuôi pad là chuỗi kí tự hex `\x3f`, vậy thì ta sẽ khôi phục key từ 2 dữ kiện này. Độ dài của format cố định là 7, nếu như padding có độ dài nhỏ hơn 9 thì ta sẽ brute force các byte key còn lại để tìm ra key đúng.

#### 4. Exploit chain

* Quy trình:

  * Khôi phục key từ pading
  * Tiếp tục khôi phục key dựa vào format
  * Giải mã cờ 

* Script: [Đọc](solve.py)

* Output: `TFCCTF{th3_tr41n_h4s_l3ft_th3_st4t10n}??????????`

* Điều may mắn là padding dài đến tận 10 kí tự, vậy thì ta không cần brute force nữa

* #### Flag: TFCCTF{th3_tr41n_h4s_l3ft_th3_st4t10n}