"""
Otimizador de imagens dos bônus.
Converte b1.png ~ b4.png para WebP de alta qualidade (sem perda visual).
"""
import os
from PIL import Image

folder = r"c:\Users\Mariana\Desktop\VDA LAN 1\saibasobrevda\capas bonus"

files = ["b1.png", "b2.png", "b3.png", "b4.png"]

for filename in files:
    src = os.path.join(folder, filename)
    name, _ = os.path.splitext(filename)
    dst = os.path.join(folder, f"{name}.webp")

    if not os.path.exists(src):
        print(f"Arquivo não encontrado: {src}")
        continue

    original_size = os.path.getsize(src)

    with Image.open(src) as img:
        # Mantém modo original; converte RGBA → transparência preservada no WebP
        img.save(dst, "webp", quality=90, method=6, lossless=False)

    new_size = os.path.getsize(dst)
    reduction = (1 - new_size / original_size) * 100

    print(
        f"{filename} -> {name}.webp  |  "
        f"{original_size / 1024 / 1024:.2f} MB -> {new_size / 1024 / 1024:.2f} MB  "
        f"({reduction:.1f}% menor)"
    )

print("\nPronto! Substitua os <img src=...> no HTML por .webp")
