import os
import re
from PIL import Image

folder_path = r"c:\Users\Mariana\Desktop\VDA LAN 1\saibasobrevda\banner home vda astronauta 1"

# Get all jpgs and sort them
files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]
files.sort()

print(f"Total de arquivos iniciais: {len(files)}")

# 1. Delete par index files to reduce by half (we just need to keep every 2nd frame)
keep_files = []
for i, f in enumerate(files):
    filepath = os.path.join(folder_path, f)
    if i % 2 != 0: # Drop odd indexes (meaning we keep 0, 2, 4...) -> wait, let's keep even indexes
        os.remove(filepath)
        print(f"Deletado frame pulado: {f}")
    else:
        keep_files.append(f)

print(f"Restaram {len(keep_files)} arquivos para o novo scroll.")

# 2. Rename and convert to webp sequentially from 000
for new_idx, old_filename in enumerate(keep_files):
    old_filepath = os.path.join(folder_path, old_filename)
    
    # We want format: Astronaut_standing_in_ocean_delpmaspu__000.webp
    new_filename = f"Astronaut_standing_in_ocean_delpmaspu__{str(new_idx).zfill(3)}.webp"
    new_filepath = os.path.join(folder_path, new_filename)
    
    try:
        # Convert to WebP
        img = Image.open(old_filepath)
        img.save(new_filepath, 'webp', quality=85, optimize=True)
        print(f"Convertido e Renomeado: {old_filename} -> {new_filename}")
        
        # Delete original JPG
        img.close()
        os.remove(old_filepath)
        
    except Exception as e:
        print(f"Erro em {old_filename}: {e}")

# 3. Update main.js
js_path = r"c:\Users\Mariana\Desktop\VDA LAN 1\saibasobrevda\src\main.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Update frame count (which is exactly the length of keep_files)
new_frame_count = len(keep_files)
js_content = re.sub(
    r'const frameCount = \d+;',
    f'const frameCount = {new_frame_count};',
    js_content
)

# Update extension in path
js_content = js_content.replace(
    'delpmaspu__${index.toString().padStart(3, \'0\')}.jpg',
    'delpmaspu__${index.toString().padStart(3, \'0\')}.webp'
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"JavaScript atualizado para {new_frame_count} frames webp.")
