# Bringing It All Together

#### Course: Symmetric Cryptography - Cryptohack

#### 1. Overview

* Đây là bài sẽ cho chúng ta tự code một thuật toán giải mã AES trong thực tế =))) và sẽ tái sử dụng các code thực hiện các bước mã hóa AES ở các bài trước. Ở các bài trước mình đã tự ý code theo cách riêng của mình, nên khi copy qua bài này để sử dụng, mình đã phải debug khá là khê mới có thể giải bài này. Nếu bạn nào đang đọc wu này thì cố gắng hoàn thành đúng theo các bước mà Cryptohack trình bày nhé

#### 2. Nền tảng cốt lõi

* Các bài trước bài này trong Course, các bạn phải hoàn thành đủ
* Có thể các bạn chưa biết, đây là thuật toán mã hóa AES chế độ ECB. Các bạn có thể đọc thêm tại đây: [Đọc](https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#ecb-mode)

#### 3. Exploit chain

* Chúng ta sẽ hoàn thành bài này bằng cách copy tất cả các hàm đã được viết và sử dung trong các bài tập trước đó:

  * Hàm `bytes2matrix`và `mamtrix2bytes`ở bài `Structure of AES`.[Đọc write-up](../Structure_of_AES/write-up.md)
  * Hàm `add_round_key`ở bài `Round Keys`.[Đọc write-up](../Round_Keys/write-up.md)
  * Hàm `sub_bytes`ở bài `Confusion through Substitution`.[Đọc write-up](../Confusion_through_Substitution/write-up.md)
  * Hàm `inv_shift_rows` và `inv_mix_columns`ở bài `Diffusion through Permutation`.[Đọc write-up](../Diffusion_through_Permutation/write-up.md)
* Sau đó hoàn thành theo khung đã được Cryptohack hướng dẫn:
* ```Python
  def decrypt(key, ciphertext):
      round_keys = expand_key(key) # Remember to start from the last round key and work backwards through them when decrypting

      # Convert ciphertext to state matrix

      # Initial add round key step

      for i in range(N_ROUNDS - 1, 0, -1):
          pass # Do round

      # Run final round (skips the InvMixColumns step)

      # Convert state matrix to plaintext

      return plaintext
  ```
* Và mình đã hoàn thành nó như sau:
* ```Python
  def decrypt(key, ciphertext):
      round_keys = expand_key(key) # Remember to start from the last round key and work backwards through them when decrypting

      # Convert ciphertext to state matrix
      ciphertext = bytes2matrix(ciphertext)

      # Initial add round key step
      add_round_key(ciphertext,round_keys[N_ROUNDS])

      for i in range(N_ROUNDS - 1, 0, -1):
          inv_shift_rows(ciphertext)
          sub_bytes(ciphertext, inv_s_box)
          add_round_key(ciphertext, round_keys[i])
          inv_mix_columns(ciphertext)

      # Run final round (skips the InvMixColumns step)
      inv_shift_rows(ciphertext)
      sub_bytes(ciphertext, inv_s_box)
      add_round_key(ciphertext, round_keys[0])

      # Convert state matrix to plaintext
      ciphertext = matrix2bytes(ciphertext)
      return ciphertext
  ```
* Script: [Đọc](aes_decrypt.py)
* ```
  crypto{MYAES128}
  ```

#### 4. Ngoài lề

* Ở bài này, chế độ mã hóa AES là chế độ ECB, chỉ có 1 đối số là `key`. Ta có thể sử dụng hàm có sẵn trong thư viên `Crypto.Cipher`để giải mã bài này. Nhưng đây là cách cheat, mình khuyên là các bạn không nên giải bài này lấy cờ bằng cách này, nó sẽ làm mất sự 'hay' của bài này :v
* ```Python
  from Crypto.Cipher import AES

  key        = b'\xc3,\\\xa6\xb5\x80^\x0c\xdb\x8d\xa5z*\xb6\xfe\\'
  ciphertext = b'\xd1O\x14j\xa4+O\xb6\xa1\xc4\x08B)\x8f\x12\xdd'

  print(AES.new(key, AES.MODE_ECB).decrypt(ciphertext))  #crypto{MYAES128}
  ```
