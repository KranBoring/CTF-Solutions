# Transparency

### Mảng: Crypto | Challenges Catagory: General 

#### 1. Overview

Đây là 1 trong những bài hay nhất mà tui từng làm, nếu giải theo cách thông thường sẽ rất dễ, nhưng làm vậy thì chúng ta sẽ không thể nào tiếp nhận được hàm ý của tác giả khi ra bài này. Nên trong write-up này, tui sẽ làm theo cả 2 cách để các bạn dễ dàng hiểu hơn nhé.

* Mục tiêu của bài : Cung cấp cho ta 1 chứng chỉ TLS đang được đăng kí cho 1 tên miền phụ(subdomain) của cryptohack.org, dựa vào public key của chứng chỉ TLS, tìm tên miền phụ của cryptohack.org để lấy cờ.
* Lỗ hổng cốt lõi: Bất kì trang web gì khi đăng kí chứng chỉ TLS thì đều có thông tin đăng kí tên miền nằm trong CT logs được public trên internet, nên việc giấu 1 trang web đăng kí chứng chỉ TLS là bất khả thi.
* Kỹ thuật khai thác: Dùng công cụ tra cứu CT logs (crt.sh) , tra cứu chứng chỉ TLS đăng kí public key để truy ngược về tên miền đăng ký chứng chủ TLS

#### 2. Nền tảng lý thuyết

Bài này là một dạng Crypto lai với Web/Forencis, nên chúng ta sẽ lấn qua 2 mảng này 1 chút để nắm được bức tranh tổng quát:

* Chứng chỉ TLS là gì?

  Nói 1 cách đơn giản, chứng chỉ TLS của 1 tên miền (domain) có ý nghĩa khá lớn rằng chứng minh tên miền đó an toàn.

* Có các dạng chứng chỉ TLS nào?

  Theo quy định quốc tế hiện hành, chứng chỉ TLS duy nhất và độc nhất là chứng chủ dạng X.509 bao gồm nhiều loại format khác nhau và mang thông tin lưu trữ khác nhau. Các dạng phổ biến như SPKI  bắt đầu bằng header `-----BEGIN PUBLIC KEY-----` (Và đây là dạng chứng chỉ chúng ta sẽ sử dụng để truy ngược subdomain của bài), PKCS#8 Private Key - header `-----BEGIN PRIVATE KEY-----`, X.509 full thông tin hay  - header `-----BEGIN CERTIFICATE-----` và còn nhiều dạng format khác nhau nữa.

* Chứng chỉ X.509 format SPKI là gì? Và ta khai thác được gì từ nó?

  SPKI viết tắt là Subject public key info, đơn giản là format này chứa `khóa công khai` a.k.a `public key` a.k.a dân dã và toán học hơn là cặp số `(N,e)`

* Chúng ta có thể truy tìm thông tin của chứng chỉ TLS này bằng cách nào?

  Bằng cách dùng các trang tra cứu CT logs để tra như crt.sh.

  > Có một câu chuyện thú vị dẫn đến sự ra đời của CT logs - Certificate Transparency
  > Đó chính là vụ bê bối về việc các công ty cung cấp chứng chỉ TLS cho tên miền bị mua chuộc, dẫn đến các trang web lừa đảo, không trong sạch nhận được  chứng chỉ TLS khiến cho nó uy tín trước công chúng. Đơn giản là vì các Hệ Điều Hành như Windows, Linux, MacOS tin tưởng rất nhiều công ty cung cấp chứng chỉ, nên việc chỉ cần một công ty bị hack hoặc là nhân viên công ty bị mua chuộc thì họ có thể cung cấp chứng chỉ cho bất kì tên miền nào! Điển hình là vụ Comodo 2011 và Symantec 2016 được tác giả nhắc đến trong bài này.
  > Nên để công chứng minh bạch thì luật quốc tế về an ninh mạng hiện hành bắt buộc tất cả các công ty khi làm chứng chỉ TLS cho bất kỳ tên miền nào cũng bắt buộc viết 1 bản CT log và nộp lên CT logs.

  #### 3. Phân tích lỗ hổng

  * Hướng 1: Dùng các tool để dò tên miền phụ của Crypto.
    Sự thật là ở hướng 1 này chẳng có gì để nói cả, chúng ta chỉ cần lên web, gõ `how to find subdomain` thì sẽ xuất hiện hàng loạt trang web hỗ trợ tìm miền phụ (Điển hình là `subdomain finder`) hoặc là pro hơn thì dùng cú pháp `site:` của google bằng cách gõ `site:*.cryptohack.org` rồi lướt xuống 1,2 trang sẽ thấy. Ngoài ra chúng ta cũng có thể dùng chính trang crt.sh để tra tên miền gần giống với `cryptohack.org` bằng cách nhập vào ô rồi search.

  * Hướng 2: Dùng public key để tra cứu thông tin chứng chỉ X.509 format SPKI đăng kí cho public key đó để truy ngược về tên miền sử dụng public key này.
    Cách này đòi hỏi chúng ta cần phải trích xuất 1 thứ gọi là dấu vân tay (fingerprint) của public key. Trên trang tra cứu CT logs của crt.sh có rất nhiều cách để tra cứu thông tin chứng chỉ:

    ![image-20260923210252198](images/image-20260923210252198.png)

    Ở mục lớn `CERTIFICATE` có các mục nhỏ hơn như trên đến `SHA-256(Certificate)` . Tui sẽ bàn đến các cách sử dụng các mục phổ biến trong ảnh sau, nhưng giờ chúng ta cần tập trung phân tích cách tra cứu chứng chỉ TLS đăng kí cho cặp khóa public key của chúng ta.
    Format của chứng chỉ là SPKI, vậy thì ta có thể sử dụng 2 mục để tra cứu đó là `SHA-1(SubjectPublicKeyInfo)` hoặc là `SHA-256(SubjectPublicKeyInfo)` để tra cứu. Bằng cách băm public key ở dạng `DER` nhị phân lấy từ chứng chỉ TLS đề cho theo `SHA-1` hoặc `SHA-256` đều có thể sử dụng để tra cứu được.

  #### 4. Exploit Chain

  * Hướng 1: Lên trên mạng search và vào trang subdomain finder:![image-20260923212134647](images/image-20260923212134647.png)

    Sau đó nhập cryptohack.org và start scan:![image-20260923212618381](images/image-20260923212618381.png)

    Ở dòng thứ 4 bạn sẽ thấy 1 tên miền phụ của cryptohack.org ghi là *thetransparencyflagishere* , các bạn nhấp vào và chúng ta lấy được cờ!

    * Hướng 2: Tải file pem của đề bài về, trích xuất fingerprint của public key

      Chúng ta có 2 cách để làm:

      1. Sử dụng openssl:

         Bằng lệnh này:

         ```bash
         openssl pkey -outform der -pubin -in transparency.pem | sha256sum
         ```

         Chúng ta sẽ thu được mã bằm sha256 và cũng chính là fingerprint của public key:
         `29ab37df0a4e4d252f0cf12ad854bede59038fdd9cd652cbc5c222edd26d77d2`

      2.  Sử dụng script python:

         Bằng cách dùng [Script](solve.py) này:

         Bạn cũng có thể lấy được fingerprint của public key:![image-20260923213446696](images/image-20260923213446696.png)\

      Sau đó lên trang `crt.sh` , vào mục advanced, chọn SHA-256(SubjectPublicKeyInfo), rồi copy fingerprint vào ô rồi bắt đầu search:![image-20260923213651835](images/image-20260923213651835.png)

      Chọn 1 mục bất kì `(Không nhất thiết chỉ có 1 id)`![image-20260923213734497](images/image-20260923213734497.png)

    Truy cập vào tên miền được ghi trong chứng chỉ và BÙM:

    ![image-20260923213855923](images/image-20260923213855923.png)

    #### Flag: crypto{thx_redpwn_for_inspiration}