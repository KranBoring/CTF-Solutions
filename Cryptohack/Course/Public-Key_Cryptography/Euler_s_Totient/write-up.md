# Euler's Totient

#### Course: `Public-Key Cryptography`- Cryptohack

#### 1. Overview

* Đây là bài thứ 3 của course. Ở bài này chúng ta sẽ được hướng dẫn về khái niệm Totient.

#### 2. Nền tảng cốt lõi

* Euler's Totient: [Đọc](https://en.wikipedia.org/wiki/Euler%27s_totient_function)
* ![{\displaystyle \varphi (n)=n\prod _{p\mid n}\left(1-{\frac {1}{p}}\right),}](https://wikimedia.org/api/rest_v1/media/math/render/svg/bb6b6388ded7d1e160a3bd82b60c5b593947088a)

#### 3. Exploit chain

* Dựa vào công thức trên. Ta sẽ tính được totient của N từ q,p
* Script: [Đọc](solve.py)
* ```
  882564595536224140639625987657529300394956519977044270821168
  ```
