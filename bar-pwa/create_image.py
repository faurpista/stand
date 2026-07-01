import os
import numpy as np
from PIL import Image, ImageDraw
import pandas as pd

# Biztosítjuk, hogy a mappa létezzen
IMAGE_DIR = "standolasi_kepek"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Beolvassuk a te CSV fájlodat, hogy lássuk, milyen neveket keres a kód
if os.path.exists("adatok.csv"):
    df_csv = pd.read_csv("adatok.csv", sep=";")
    
    print("🎨 Tesztképek legyártása a hiányzó fájlok helyett...")
    for filename in df_csv['image_filename']:
        img_path = os.path.join(IMAGE_DIR, filename)
        
        # Csak akkor gyártjuk le, ha még nem létezik
        if not os.path.exists(img_path):
            # Létrehozunk egy egyszerű színes kockát
            random_color = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
            img = Image.fromarray(random_color)
            img.save(img_path)
    print("✅ Minden tesztkép sikeresen legenerálva a 'standolasi_kepek' mappába!")
