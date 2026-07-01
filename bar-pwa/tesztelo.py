import os
import torch
import torchvision.models as models
import torch.nn as nn
from torchvision import transforms
from PIL import Image

# --- BEÁLLÍTÁSOK ---
MODEL_PATH = "bar_leltar_modell.pth"  # A betanított ResNet50 alapú modell súlyfájlja
TEST_IMAGE_PATH = "soproni_ures_szembol.jpg" # A frissen korrigált kép
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- 1. MODELL ARCHITEKTÚRA DEFINIÁLÁSA ---
# Pontosan meg kell egyeznie a tanításkor használt struktúrával!
class BarBottleLevelPredictor(nn.Module):
    def __init__(self):
        super(BarBottleLevelPredictor, self).__init__()
        resnet = models.resnet50(weights=None) # Nem kell az ImageNet súly, mert a sajátunkat töltjük be
        self.feature_extractor = nn.Sequential(*list(resnet.children())[:-1])
        
        self.regressor = nn.Sequential(
            nn.Linear(2048, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid() # A kimenetet 0.0 és 1.0 közé szorítja
        )
        
    def forward(self, x):
        features = self.feature_extractor(x)
        features = features.view(x.size(0), -1)
        return self.regressor(features)

# --- 2. MODELL BETÖLTÉSE ---
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Nem található a modell súlyfájlja: {MODEL_PATH}")

model = BarBottleLevelPredictor().to(DEVICE)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.eval() # Átállítjuk kiértékelési módba (kikapcsolja a dropoutot)
print("✅ A modell súlyai sikeresen betöltve.")

# --- 3. KÉP ELŐKÉSZÍTÉSE ---
# Ugyanaz a normalizálás és átméretezés kell, mint amit a teszthalmaz kapott
test_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# --- 4. PREDIKCIÓ (TIPPELÉS) ---
if os.path.exists(TEST_IMAGE_PATH):
    # Kép megnyitása és előkészítése
    image = Image.open(TEST_IMAGE_PATH).convert('RGB')
    input_tensor = test_transforms(image).unsqueeze(0).to(DEVICE) # Batch dimenzió hozzáadása (1, 3, 224, 224)
    
    # Gradiens számítás kikapcsolása a gyorsabb futásért
    with torch.no_grad():
        output = model(input_tensor)
        
        # Mivel a modell kimenete 0.0 és 1.0 között van, megszorozzuk 100-zal, hogy százalékot kapjunk
        predicted_percentage = output.item() * 100.0

    print("\n----------------------------------------")
    print(f"📷 Tesztelt kép: {TEST_IMAGE_PATH}")
    print(f"🤖 A modell tippje a töltöttségre: {predicted_percentage:.1f}%")
    print("----------------------------------------")
    
    # Értékelési segítség a látvány alapján (A kép alapján kb. 50%-on áll a folyadék)
    valodi_szint = 0.0 
    elteres = abs(valodi_szint - predicted_percentage)
    print(f"📉 Becsült tévedés a valósághoz képest: {elteres:.1f}%")

else:
    print(f"❌ A tesztelni kívánt kép nem található: {TEST_IMAGE_PATH}")
