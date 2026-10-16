import sys
from PIL import Image

# NES uchun standart ranglar palitrasi (RGB)
# Bu palitra o'yinning asl ranglariga yaqinlashtirilgan
NES_PALETTE = [
    (124, 124, 124), (0, 0, 252), (0, 0, 188), (68, 40, 188),
    (148, 0, 132), (168, 0, 32), (168, 16, 0), (136, 20, 0),
    (80, 48, 0), (0, 120, 0), (0, 104, 0), (0, 88, 0),
    (0, 64, 88), (0, 0, 0), (0, 0, 0), (0, 0, 0),
    (188, 188, 188), (0, 120, 248), (0, 88, 248), (104, 68, 252),
    (216, 0, 204), (228, 0, 88), (248, 56, 0), (228, 92, 16),
    (172, 124, 0), (0, 184, 0), (0, 168, 0), (0, 168, 68),
    (0, 136, 136), (0, 0, 0), (0, 0, 0), (0, 0, 0),
    (248, 248, 248), (60, 188, 252), (104, 136, 252), (152, 120, 248),
    (248, 120, 248), (248, 88, 152), (248, 120, 88), (252, 160, 68),
    (248, 184, 0), (184, 248, 24), (88, 216, 84), (88, 248, 152),
    (0, 232, 216), (120, 120, 120), (0, 0, 0), (0, 0, 0),
    (252, 252, 252), (164, 228, 252), (184, 184, 248), (216, 184, 248),
    (248, 184, 248), (248, 164, 192), (240, 208, 176), (252, 224, 168),
    (248, 216, 120), (216, 248, 120), (184, 248, 184), (184, 248, 216),
    (0, 252, 252), (248, 216, 248), (0, 0, 0), (0, 0, 0)
]

def rgb_to_nes_index(rgb):
    """RGB rangni NES palitrasidagi eng yaqin indeksga o'giradi."""
    min_dist = float('inf')
    best_index = 0
    for i, color in enumerate(NES_PALETTE):
        dist = sum((a - b) ** 2 for a, b in zip(rgb, color))
        if dist < min_dist:
            min_dist = dist
            best_index = i
    return best_index

def png_to_chr(png_path, chr_path):
    """PNG faylini o'qib, NES CHR formatiga o'giradi."""
    img = Image.open(png_path).convert('RGB')
    width, height = img.size
    
    # Rasm o'lchamlari 8 ga karrali bo'lishi kerak
    if width % 8 != 0 or height % 8 != 0:
        print("Xato: Rasm o'lchamlari 8 ga karrali bo'lishi kerak.")
        return

    chr_data = bytearray()
    
    # Har bir 8x8 blokni tahlil qilish
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            tile_pixels = []
            for dy in range(8):
                for dx in range(8):
                    rgb = img.getpixel((x + dx, y + dy))
                    nes_idx = rgb_to_nes_index(rgb)
                    tile_pixels.append(nes_idx)
            
            # NES CHR formati: har bir qator uchun 2 ta bayt (bit-plane)
            for row in range(8):
                byte1 = 0
                byte2 = 0
                for col in range(8):
                    pixel = tile_pixels[row * 8 + col]
                    # Rang indeksining 0-bitini birinchi baytga, 1-bitini ikkinchi baytga yozamiz
                    if pixel & 1:
                        byte1 |= (1 << (7 - col))
                    if pixel & 2:
                        byte2 |= (1 << (7 - col))
                chr_data.append(byte1)
                chr_data.append(byte2)

    # Natijani faylga yozish
    with open(chr_path, 'wb') as f:
        f.write(chr_data)
    print(f"Muvaffaqiyatli! {chr_path} fayli yaratildi.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Foydalanish: python png_to_chr.py <kirish.png> <chiqish.chr>")
        sys.exit(1)
    
    png_path = sys.argv[1]
    chr_path = sys.argv[2]
    png_to_chr(png_path, chr_path)
