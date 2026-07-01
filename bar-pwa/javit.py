import os
from PIL import Image

# Kép beolvasása
input_image_path = "soproni70.jpg"  # Cseréld ki a kép nevére
output_image_path = "soproni_distStandard_ang0.jpg"

if os.path.exists(input_image_path):
    orig_img = Image.open(input_image_path).convert("RGB")
    
    # 1. LÉPÉS: A palack FELÁLLÍTÁSA (90 fokos elforgatás balra)
    # Az 'expand=True' miatt a kép szélessége és magassága megcserélődik, így nem vágódik le az üveg
    img_upright = orig_img.rotate(14, resample=Image.Resampling.BICUBIC, expand=True)
    
    # Most, hogy az üveg már áll, lekérjük az új méreteket
    width, height = img_upright.size
    
    # 2. LÉPÉS: Távolság korrekciója ~50 cm-es standard távolságra
    # Mivel közelebbi a fotó, 0.82-es arányban lekicsinyítjük, hogy távolabb kerüljön
    scale = 0.82
    new_w, new_h = int(width * scale), int(height * scale)
    img_scaled = img_upright.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Új üres háttér létrehozása (az álló kép méretében), és a kicsinyített kép középre helyezése
    # A hátteret egy semleges szürkésbarna színnel töltjük ki, ami passzol a falhoz/asztalhoz
    img_standard = Image.new("RGB", (width, height), (160, 150, 140))
    offset = ((width - new_w) // 2, (height - new_h) // 2)
    img_standard.paste(img_scaled, offset)
    
    # Mentés
    img_standard.save(output_image_path, quality=95)
    print(f"✅ A palack sikeresen FEL LETT ÁLLÍTVA és elmentve ide: {output_image_path}")
else:
    print(f"A megadott forráskép nem található: {input_image_path}")
