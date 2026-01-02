import zlib
import struct
import random
import io
import base64
from IPython.display import Image, display

def generate_random_image_bytes(width=10, height=10): #ここで解像度を調整してください。8×8~20×20がおすすめです。また、解像度は低い方がランダム生成の違いが分かりやすい上、綺麗な模様になります。
    def png_chunk(chunk_type, data):
        return (
            struct.pack(">I", len(data)) +
            chunk_type +
            data +
            struct.pack(">I", zlib.crc32(chunk_type + data) & 0xffffffff)
        )

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)

    # 画像データ生成
    rows = []
    for y in range(height):
        row = bytearray()
        for x in range(width):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            a = random.randint(0, 255)
            row.extend([r, g, b, a])
        rows.append(b"\x00" + row)

    raw_data = b"".join(rows)
    compressed_data = zlib.compress(raw_data)

    png = (
        b"\x89PNG\r\n\x1a\n" +
        png_chunk(b"IHDR", ihdr) +
        png_chunk(b"IDAT", compressed_data) +
        png_chunk(b"IEND", b"")
    )
    return png

def main():
    img_bytes = generate_random_image_bytes()
    output_filename = "infinity_image.png"
    with open(output_filename, "wb") as f:
        f.write(img_bytes)
    print(f"画像が保存されました: {output_filename}")

    print("生成された画像をここに表示します:")
    display(Image(filename=output_filename))

if __name__ == "__main__":
    main()
