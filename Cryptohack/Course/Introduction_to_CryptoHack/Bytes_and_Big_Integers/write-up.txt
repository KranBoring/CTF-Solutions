Bài này hướng dẫn về các dạng encode message
Và thứ đặt biệt trong này là cách encode message sang hệ 10

Cách các hàm long_to_bytes và Bytes_to_long hoạt động

- long_to_bytes(<long long number>): đổi số sang binary
Cách đổi:
Hệ bytes được lưu trữ theo Big-Endien
B1: Lưu lại kết quả số chia dư 256
B2: Lấy số chia lấy nguyên cho 256
B3: Loop B1 cho đến khi n = 0
B4: Đảo ngược lại để lưu đúng dạng Big-Endien
Ví dụ minh họa:
Với số N = 6382179:
6382179 (mod 256)  = 99 -> ký tự 'c'
6382179 // 256 = 24930
24930 (mod 256) = 98 -> ký tự 'b'
24930 // 256 = 97
97 (mod 256) = 97 -> ký tự 'a'
97 // 256 = 0 Dừng lại
Gom các byte thu được theo thứ tự ngược lại: [97, 98, 99] -> b"abc"

- bytes_to_long(<binary>): đổi binary sang số
Cách đổi:
Mỗi bytes chứa 8 bits, khi biểu diễn bytes dưới dạng hệ demical thì giá trị có thể biểu diễn từ 0 - 255, thì coi mỗi bytes như 1 con số ở hệ base-256
Quy ước cách lưu trữ bytes cũng là Big-Endien
B1: Tách binary thành aray với mỗi phần tử chứa 1 bytes
B2: Tính tổng theo vị trí hệ cơ số 256 (search mạng)
Ví dụ minh họa:
Giả sử đổi chuỗi byte b"abc" sang số nguyên:
Byte 'a' có mã ASCII là 97 (0x61)
Byte 'b' có mã ASCII là 98 (0x62)
Byte 'c' có mã ASCII là 99 (0x63)
Áp dụng cơ số 256:
N = 97 * 256^2 + 98 * 256^1 + 99 * 256^0
N = 97 * 65536 + 98 * 256 + 99 = 6356992 + 25088 + 99 = 6382179

Cách giải bài lấy cờ:
Số đề bài cung cấp là kết quả từ việc đổi message sang số hệ demical, vậy để lấy cờ, ta chỉ cần đảo ngược quá trình là được.
Script: decrypt.py
#Flag:crypto{3nc0d1n6_4ll_7h3_w4y_d0wn}
