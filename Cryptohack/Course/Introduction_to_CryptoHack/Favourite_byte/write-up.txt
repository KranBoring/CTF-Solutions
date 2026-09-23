Bài này cho ta một đoạn hex string và thông báo rằng có vài dữ liệu mật đã được XOR với 1 byte nhưng byte đó là bí mật

Cách giải:
Ta ở đây là
- Dữ liệu mật = plaintext cần giải mã
- 1 byte bí mật = key
Và đề không cung cấp cho chúng ta key, nhưng vấn đề là byte chỉdài 1 byte. Vậy thì chúng ta chỉ cần thử mọi loại khóa dài 1 byte là được - 256 chìa khóa khác nhau
Script: solve.py

#Flag:crypto{0x10_15_my_f4v0ur173_by7e}
