# i_am_scared (h4ckc0n 2026)

#### Mảng: Crypto / Misc, Độ khó: Easy - Medium

---

### 1. Phân tích đề bài

Tệp [scary.txt](file:///home/kran-rpg/Hacker_Space/CTF/Others-Events/2026/h4ckc0n/i_am_scared/scary.txt) gồm 45 dòng với hai dạng dữ liệu:
* Dạng `NUMBER[INDEX]`: Ví dụ `839[6]`, `479[8]`, `275[5]`...
* Dạng `<cant_find_letter>`: Xuất hiện xen kẽ giữa các nhóm ký tự.

Gợi ý từ tác giả:
> *note - `<cant_find_letters>` are just an underscore or { or }*
> *a bit of a misc crypto (:*

### 2. Ý tưởng giải mã (Book Cipher - SCP Foundation Series 1)

1. Tên bài toán `i_am_scared` kết hợp với gợi ý về các số `NUMBER[INDEX]` chỉ đến danh sách các mục của **SCP Foundation (Series 1: SCP-001 đến SCP-999)** trên Wikidot (`https://scp-wiki.wikidot.com/scp-series`).
2. Với mỗi dòng `NUMBER[INDEX]`:
   - `NUMBER`: Mã số của đối tượng SCP.
   - `INDEX`: Vị trí ký tự thứ `INDEX` (chỉ số 0-based) trong tiêu đề chính thức (Title) của SCP đó.
3. Ký tự `<cant_find_letter>`:
   - Ký tự đầu tiên: `{` (sau tiền tố `d4rk`)
   - Ký tự cuối cùng: `}`
   - Tất cả các vị trí ở giữa: `_` (dấu gạch dưới phân tách từ).

### 3. Bảng tra cứu và giải mã từng ký tự

| Dòng | Dữ liệu gốc | Tiêu đề SCP Series 1 | Ký tự trích xuất |
| :---: | :--- | :--- | :---: |
| 1 | `839[6]` | Candied Worms | `d` |
| 2 | `479[8]` | Hallway 4, D-Class Dorms, Site 14 | `4` |
| 3 | `317[1]` | Cretaceous Physicist | `r` |
| 4 | `275[5]` | Ironskin | `k` |
| 5 | `<cant_find_letter>` | `{` | `{` |
| 6 | `937[8]` | Walking Sticks | `S` |
| 7 | `344[14]` | Schrödinger's Can Opener | `C` |
| 8 | `320[29]` | Higgs Field Acceleration Manipulator | `p` |
| 9 | `173[4]` | The Sculpture - The Original | `S` |
| 10 | `<cant_find_letter>` | `_` | `_` |
| 11 | `370[0]` | A Key | `A` |
| 12 | `712[19]` | The Impossible Colors | `r` |
| 13 | `335[22]` | One Hundred and Fifty 3.5" Floppy Disks | `3` |
| 14 | `<cant_find_letter>` | `_` | `_` |
| 15 | `214[15]` | Hemotopian Virus | `s` |
| 16 | `898[8]` | Memetic Counter-Agent | `C` |
| 17 | `180[19]` | Identity-Thieving Hat | `a` |
| 18 | `334[6]` | Stellar Vulpine | `r` |
| 19 | `103[2]` | Rhys' Head / Mara's Heart | `y` |
| 20 | `<cant_find_letter>` | `_` | `_` |
| 21 | `296[23]` | Armed Containment Site-03 | `0` |
| 22 | `420[3]` | Aggressive Skin Condition | `r` |
| 23 | `<cant_find_letter>` | `_` | `_` |
| 24 | `806[8]` | Resurrection Projection | `t` |
| 25 | `948[1]` | The Workaholic | `h` |
| 26 | `178[1]` | "3-D" Specs | `3` |
| 27 | `536[2]` | Physical Quirks | `y` |
| 28 | `<cant_find_letter>` | `_` | `_` |
| 29 | `838[10]` | The Dream Job | `J` |
| 30 | `551[12]` | Impossible Puzzle | `u` |
| 31 | `111[7]` | Dragon-Snails | `S` |
| 32 | `443[0]` | Thought-streaming Crayons | `T` |
| 33 | `<cant_find_letter>` | `_` | `_` |
| 34 | `24[8]` | Game Show of Death | `w` |
| 35 | `479[32]` | Hallway 4, D-Class Dorms, Site 14 | `4` |
| 36 | `347[5]` | The Invisible Woman | `n` |
| 37 | `494[10]` | Matter Transference Gloves | `n` |
| 38 | `998[13]` | Missing Aircraft | `a` |
| 39 | `<cant_find_letter>` | `_` | `_` |
| 40 | `429[12]` | Clockwork Teleporter | `l` |
| 41 | `332[4]` | The 1976 Kirk Lonwood High School Marching Band | `1` |
| 42 | `678[10]` | Trauma Harvester | `v` |
| 43 | `434[4]` | A Meeting with Myself | `e` |
| 44 | `31[12]` | What is Love? | `?` |
| 45 | `<cant_find_letter>` | `}` | `}` |

---

### 4. Mã nguồn giải mã

Xem chi tiết tại [solve.py](file:///home/kran-rpg/Hacker_Space/CTF/Others-Events/2026/h4ckc0n/i_am_scared/solve.py).

---

### 5. Flag

`d4rk{SCpS_Ar3_sCary_0r_th3y_JuST_w4nna_l1ve?}`
