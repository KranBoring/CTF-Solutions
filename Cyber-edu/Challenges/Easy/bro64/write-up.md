# bro64

#### Tags: Cryptography - Diff: easy

#### 1. Overview

* `Mục tiêu`: giải mã ciphertext
* `Kỹ thuật`: Nhận diện đối số của các thuật toán mã hóa hiện đại

#### 2. Nền tảng

* Bài này nền tảng rất rộng, bởi vì để nhớ hết các đối số hoặc biết đến hết các phương pháp mã hóa hiện đại là 1 điều không tưởng. Vì vậy, tôi sẽ nêu đích danh thuật toán mã hóa trong bài này là ChaCha20

#### 3. Phân tích

* Khi gửi request lên server thì ta nhận được 1 file json gồm: 
  * `nonce`
  * `key`:Fidel_Alejandro_Castro_Ruz_Cuba!
  * `ciphertext`
* Ta nhận thấy được ngay ~~(nếu bạn cheat giống tôi)~~ `nonce` và `key` chính là đối số của thuật toán mã hóa ChaCha20 và trong đề bài cũng đã Hint cho ta về thuật toán mã hóa này
* ***Betaflash let’s go in Cuba and dance amigo !!***
* ChaCha nghe khá giống các bài nhảy dân gian, đơn giản vậy thôi

#### 4.Exploit chain

* Quy trình:

  * Gửi request lên server để lấy file json
  * Giải mã base64 cho `ciphertext` và `nonce`
  * Tạo object đối với thuật toán mã hóa ChaCha20 với đối số là `key` và `nonce`
  * Giải mã

* #### Flag: ctf{f38deb0782c0f252090a52b2f1a5b05bf2964272f65d5c3580be631f52f4b3e0}



