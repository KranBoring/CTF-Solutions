# Extended GCD

#### 1. Overiew

Đây là bản mở rộng của thuật toán tìm gcd của 2 số nguyên dương Euclid hay Extended Euclid' algorithm.

#### 2. Nền tảng cốt lõi

[Xem thêm thuật toán mở rộng Euclid tại đây](https://wiki.vnoi.info/algo/algebra/euclid.md#:~:text=%C2%B6-,Thu%E1%BA%ADt%20to%C3%A1n%20Euclid%20m%E1%BB%9F%20r%E1%BB%99ng,-V%E1%BB%9Bi%20hai%20s%E1%BB%91) 

Tóm tắt về Extended Euclid' algorithm thì với 2 số nguyên dương a,b, thuật toán sẽ viết d = gcd(a,b) dưới dạng **tổ hợp tuyến tính**, sẽ tồn tại 1 số x,y thỏa mãn:

![lagrida_latex_editor](images/lagrida_latex_editor.png)

#### 3. Phân tích

Bài này chúng ta sẽ sử dung python để tính `x,y` thỏa mãn tổ hợp tuyến tính ở trên. Ý tưởng giải sẽ như sau:

* Ta đặt `a0` và `b0` là 2 số khởi đầu của hàm tìm `x,y` thỏa mãn tổ hợp tuyến tính trên, bắt đầu quá trình tìm gcd theo thuật toán Euclid.

* Ta gọi cặp số `u,v` thỏa (Trường hơp cơ sở: `u = 1, v = 0`):

  ![lagrida_latex_editor (3)](images/lagrida_latex_editor3.png)

* Ta gọi cặp số `h,k` thỏa (`Trường hợp cơ sở: h = 0, k = 1`):

  ![lagrida_latex_editor (2)](images/lagrida_latex_editor2.png)

* Phân tích `b` ta được như sau:

  ![lagrida_latex_editor (4)](images/lagrida_latex_editor4.png)

  ![lagrida_latex_editor (5)](images/lagrida_latex_editor5.png)

* Và bây giờ chạy thuật toán Euclid, đồng thời lưu lại các biến thỏa mãn tổ hợp tuyến tính. Biến `r` được tính bằng cách sau đây, vậy ta sẽ lặp lại cho đến khi `r = 0` hay là `a = 0` trong vòng lăp :

  ![lagrida_latex_editor (7)](images/lagrida_latex_editor7.png)

  ![lagrida_latex_editor (8)](images/lagrida_latex_editor8.png)

  #### 4. Exploit chain / Script:

  Phân tích như trên, ta chỉ cần viết script thôi:

  [Đọc script](./script.py)

  * Mở rộng: Ngoài cách giải như trên, thư viện sagemath cũng hỗ trợ 1 hàm là `xgcd` để trả về gcd, và cả cặp số x,y thỏa mãn tổ hợp tuyến tính trên:

    [Đọc script](./solve.py)

  #### Nmber: -8404

  #### 5. Reference

  Một số cách tính x,y:[Đọc](https://web.archive.org/web/20230511143526/http://www-math.ucdenver.edu/~wcherowi/courses/m5410/exeucalg.html)

  VNOI Euclid's algorithm: [Đọc](https://wiki.vnoi.info/algo/algebra/euclid.md)
  Wikipedia Euclid: [Đọc](https://en.wikipedia.org/wiki/Euclidean_algorithm)

  

  