Bài này hướng dẫn về base64
Hiểu 1 cách nôm na thì base64 sẽ giúp chuyển đổi file nhị phân toàn các kí tự không đọc được khi chuyển sang bảng mã ASCII thành file cũng nhị phân nhưng nằm trong bảng chữ cái (64 chữ) đọc được khi chuyển sang bảng mã ASCII.
Khi encode thì file nhả ra bị phình to lên, cứ mỗi 3 kí tự (char 8-bits) thì nhả ra 4 kí tự mới (char 6-bits) theo base64 (phình lên cỡ 1/3 so với file gốc)
Cách nó encode:
Khi lưu chuỗi string dưới dạng binary
Ví dụ:"r\xbc\xa9\xb6\x8f\xc1j\xc7\xbe\xeb\x8f\x84\x9d\xca\x1d\x8ax>\x8a\xcf\x96y\xbf\x92i\xf7\xbf"
Các chuỗi kí tự chứa tiền tố \x?? có nghĩa là kí tự đó có mã hex là ?? nhưng ko thể in ra được (kí tự đổi sang bảng mã ASCII không phải là 1 kí tự đọc được)
Mỗi kí tự char hay \x?? đều chiếm ô nhớ 8 bits, khi encode base64, nó sẽ lấy từ trái qua phải 6 bits rồi chuyển sang kí tự, lần lượng như vậy cho đến hết chuỗi, nếu như tới cuối chuỗi hết kí tự để lấy giá trị bits, nó sẽ tự điền phần còn lại bằng số 0
Có 2 trường hợp xảy ra khi thiếu hụt ô bits để lấy:
Như đã nói, mỗi 3 kí tự char-8 bits encode sang base64 đều nhả ra 4 kí tự, nhưng khi chỉ có 1 hoặc 2 kí tự, nó cũng sẽ encode ra 4 kí tự và cách hoạt động như sau:
TH1: encode base64 cho 1 kí tự char
- Kí tự đầu tiên sẽ lấy đầy đủ 6 bits từ kí tự char, còn lại 2 bits, encode sẽ đệm thêm 4 bits 0 nằm phía bên phải 2 bits còn lại đó để sinh ra kí tự base64 thứ 2, vì đã hết bits để encode nên encode sẽ nhả ra 2 kí tự '=' để báo hiệu là hết bits để encode
Ví dụ:
input: echo -n "a" | base64
output: YQ==
TH2: encode base64 cho 2 kí tự char
- Kí tự đầu tiên lấy đủ, kí tự thứ 2 lấy đủ, kí tự thứ 3 chỉ còn 4 bits để lấy, đệm 2 bits 0 bên phải và kí tự thứ 4 không có bits nào, in ra 1 kí tự đệm '=' 
Ví dụ:
input: echo -n "aa" | base64
output: YWE=

Khi decode, chỉ là đảo ngược quá trình, nhưng khi decode 2 trường hợp đặt biệt trên thì decode base64 sẽ tự động phát hiện để decode thành 1 kí tự hay 2 kí tự
TH1: Gặp chuỗi 4 kí tự base64 có 2 kí tự đệm '=='
- lúc này decode sẽ chỉ ra 1 kí tự char 8 bits, khi đọc đến kí tự thứ 2, nó sẽ loại bỏ các bits 0 đệm bên phải (ở TH này là 2 bits 0),trả về bits gốc, để in đúng dạng decode
TH2: Gặp chuỗi 4 kí tự base64 có 1 kí tự đệm '='
- decode ra 2 kí tự char 8 bits , ki đọc đến kí tự thứ 3, loại bỏ các bits 0 đệm bên phải (ở TH này là 4 bits 0), trả về bits gốc, để in đúng dạng decode

Cách decode lấy flag:
-Đề cung cấp 1 chuỗi hex và gợi ý là base64, ta cần phải chuyển chuỗi hex sang chuỗi binary để encode base64
decode.py trong bài
#Flag:crypto/Base+64+Encoding+is+Web+Safe/
