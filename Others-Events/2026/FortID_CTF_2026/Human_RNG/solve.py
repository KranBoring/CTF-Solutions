import re
import sys

from PIL import Image
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from pyzbar.pyzbar import decode

VERSION = 6
SIZE = 41
ERROR = ERROR_CORRECT_H
MASK = 0
BORDER = 4
SCALE = 10
def read_png(path):
    with Image.open(path) as im:
        im = im.convert("1")
        w,h = im.size
        size = w // 10
        px = im.load()

        bits = []
        for y in range(size):
            for x in range(size):
                pixel_value = px[x * 10 + 5, y * 10 + 5]
                bit = 1 if pixel_value == 0 else 0
                bits.append(bit)
    return bits
def load_keystream(n):
    raw = open("bitstream.txt").read().strip()

    assert "<" not in raw, "bitstream.txt contains the redacted suffix"
    bits = [int(c) for c in raw if c in "01"]

    assert len(bits) >= n
    return bits[-n:]
def bits_to_qr_file(bits):
    output_path="recover.png"
    total_size = SIZE + 2 * BORDER
    img_size = total_size * SCALE
    img = Image.new("1", (img_size, img_size), 1)
    px = img.load()
    for index, bit in enumerate(bits):
        y = index // SIZE
        x = index % SIZE
        if bit == 1:
            start_x = (x + BORDER) * SCALE
            start_y = (y + BORDER) * SCALE
            for dy in range(SCALE):
                for dx in range(SCALE):
                    px[start_x + dx, start_y + dy] = 0
    img.save(output_path)
data = read_png("ciphertext.png")
key = 
plaintext = [a ^ b for a, b in zip(data, key)]
bits_to_qr_file(plaintext)
print(decode(Image.open("recover.png"))[0].data.decode())
