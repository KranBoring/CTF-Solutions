# Legendre Symbol

#### Course: Modular Arithmetic

#### 1. Overview

* Bài này hướng dẫn chúng ta cách nhận biết một số có thặng dư bậc 2 bằng dấu hiệu Legendre

#### 2. Nền tảng cốt lõi

* Legendre Symbol: [Đọc](https://en.wikipedia.org/wiki/Legendre_symbol)
* Nhưng dấu hiệu Legendre chỉ cho chúng ta biết rằng số đó có thặng dư bậc 2, chứ không cho ta cách tính
* Có 2 trường hợp khi tìm thặng dư bậc 2 đó là khi `p = 1 mod 4 và p = 3 mod 4`, ở write-up này chúng ta chỉ bàn luận về trường hợp `p = 3 mod 4`
  * Bây giờ, giả sử 1 số `a` thỏa mãn dấu hiệu legendre và có thặng dư bậc 2
  * Vậy sẽ có 1 số `x` thỏa:
  * $$
    x^2 = a \text{ (mod p)}
    $$
  * Theo định lý fermat nhỏ, kết hợp với điều kiện trên, ta có:
  * $$
    a^{p-1} = 1 \text{ (mod p)} \to a^{\frac{(p -1 )}{2}} = (x^{2})^{\frac{(p -1 )}{2}} = x^{p - 1} = 1 \text{  (mod p)}
    $$
  * Như các bạn thấy, bản chất của dấu hiệu legendre được chứng minh thông qua định lý fermat nhỏ:
  * Khi đó, ta có:
  * $$
    x^2 = a \text{ (mod p)}\to x^2 = a * 1\text{ (mod p)} \to x^2 = a * a^{\frac{p-1}{2}}\text{ (mod p)} \to x^2 = a^{\frac{p-1}{2} + 1}\text{ (mod p)} \to x^2 = a^{\frac{p+1}{2}}\text{ (mod p)} \to x = \pm a^{\frac{p+1}{4}}\text{ (mod p)}
    $$
  * Để có thể tính được `x`- `thặng dư bậc 2 của a` , ta cần `p+1` chia hết cho , nên để sử dụng công thức này thì `p` phải thỏa mãn `p mod 4 = 3`

#### 3. Exploit chain

* Ta kiểm tra trong list `ints` có số nào có `(a/p) = 1` hay không, nếu có thì kiểm tra `p có chia 4 dư 3 hay không`, và nếu có thì ta tính `x` là xong!
* Script: [Đọc](solve.py)
* ```
  93291799125366706806545638475797430512104976066103610269938025709952247020061090804870186195285998727680200979853848718589126765742550855954805290253592144209552123062161458584575060939481368210688629862036958857604707468372384278049741369153506182660264876115428251983455344219194133033177700490981696141526
  ```
