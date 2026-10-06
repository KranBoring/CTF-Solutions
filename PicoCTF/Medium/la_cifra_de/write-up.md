# la cifra de

#### Category: Crypto - Diff: Medium

#### 1. Overview

* ![image-20261006153126394](images/image-20261006153126394.png)
* Đây là 1 bài giải mã ciphertext khá là hay =))))
* `Mục tiêu`: Giải mã ciphertext
* `Kỹ thuật`: Brute Force key, phân tích key

#### 2. Nền tảng cốt lõi

* Bài này các bạn cần phải nhìn ra được loại mã hóa được áp dụng lên ciphertext, có thể dùng tool, nhưng nếu nhận ra được loại mã hóa gì mình cũng nể các bạn thật =)))))
* Tool:
  * Cipher - Identify: [Đọc](https://www.dcode.fr/cipher-identifier)

#### 3. Phân tích/Exploit chain

* Khi netcat đến server, ta nhận được 1 đoạn message bị mã hóa

* ![image-20261006153711833](images/image-20261006153711833.png)

* Hint: ![image-20261006153733146](images/image-20261006153733146.png)

* Khi đọc hint thứ nhất, mình đã nghĩ rằng là đây có thể là mã hóa dịch chuyển đơn kí tự, nên dùng phân tích tần suất để thực hiện `frequency attack`, nhưng khi phân tích thì lại không có ra bản rõ nào cả.

* ![image-20261006154424425](images/image-20261006154424425.png)

* Khi đối chiếu lại ciphertext thì mình thấy các cột mốc năm có 1 từ tiếng anh đó là `in` được mã hóa không đồng đều. Lúc thì `os` lúc sau là `ny` nên mình đã nghĩ đến mã hóa đa khối

* Để nhận dạng nhanh loại mã hóa, mình đã lên trang `cipher - identify của dcode` để xem thử loại mã hóa đó là gì thì đây:

* ![image-20261006154808772](images/image-20261006154808772.png)

* Có xác suất cao là cờ đã bị `mã hóa Vigenere` - một dạng mã khóa đa khối trong mã hóa Caesar

* Khi thử để web `automatic decrypt` thì có hàng loạt có kết quả key khác nhau, không có cái nào phù hợp, nhưng trong số đó có 1 vài trường hợp có vẻ gần đã giải ra ciphertext

* ![image-20261006155203941](images/image-20261006155203941.png)

* Nên mình đã đoán key là `FLAG`, mình đã thử thì đã giải mã được 1 đoạn message

* ![image-20261006155241393](images/image-20261006155241393.png)

* Khi phân tích các kết quả của `automatic decrypt` thì mình nhận thấy các key dường như chỉ là hoán vị của khóa và đã có 1 vài đoạn ciphertext có thể đọc được, nên mình đã thử hoán vị các kí tự của khóa thì mình được như sau:

* ![image-20261006155942091](images/image-20261006155942091.png)

* ![image-20261006155957071](images/image-20261006155957071.png)

* ![image-20261006160014617](images/image-20261006160014617.png)

* #### Flag: academy{b311a50_0r_v1gn3r3_c1ph3r0fff5e61}