#!/usr/bin/env python3
"""
Compositor FINAL v3 - PUNTA CANA 2026 POSTER
Estratégia: Usa o melhor pôster base e compõe os retratos reais
com recorte baseado em crop central sem remover pixels escuros.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageChops

# ─── Paths ───────────────────────────────────────────────────────────────────
OUTPUTS_DIR = Path("/Users/PROJETOS-DEV/GERADOR-DE-IMAGENS/medias/outputs")

# Usa o pôster com pessoas que tem melhor composição
POSTER_BASE = Path(
    "/Users/danilonovais/.gemini/antigravity-ide/brain/"
    "f54a37d0-75d5-4033-92b9-d0131a690e24/"
    "punta_cana_poster_com_pessoas_1780335648067.png"
)

OUTPUT_FINAL = OUTPUTS_DIR / "PUNTA_CANA_2026_POSTER_FINAL_A3.png"

# A3 @ 150dpi: 1748 × 2480 px
A3_W, A3_H = 1748, 2480


def crop_character(img: Image.Image, target_h: int, margin_pct: float = 0.16) -> Image.Image:
    """
    Recorta o personagem do centro da imagem, removendo margens laterais
    com anotações de texto. Mantém todos os pixels — não remove escuros.
    """
    w, h = img.size
    margin = int(w * margin_pct)
    # Crop lateral para remover anotações
    cropped = img.crop((margin, int(h * 0.03), w - margin, h))
    
    cw, ch = cropped.size
    # Redimensiona mantendo proporção
    ratio = target_h / ch
    new_w = int(cw * ratio)
    return cropped.resize((new_w, target_h), Image.LANCZOS)


def create_character_with_feathered_edges(img: Image.Image) -> Image.Image:
    """
    Cria uma máscara com bordas suavizadas ao redor do personagem.
    Estratégia: detecta branco puro e cria alpha, sem afetar pixels escuros.
    """
    img_rgba = img.convert("RGBA")
    w, h = img_rgba.size
    
    # Cria máscara: começa com tudo opaco
    mask = Image.new("L", (w, h), 255)
    draw = ImageDraw.Draw(mask)
    
    # Pixels brancos puros → transparentes
    pixels = img_rgba.load()
    mask_pixels = mask.load()
    
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # Somente branco puro ou quase-puro (todos os canais > 248)
            if r >= 248 and g >= 248 and b >= 248:
                mask_pixels[x, y] = 0
            elif r >= 240 and g >= 240 and b >= 240:
                # Borda suave
                darkness = 255 - min(r, g, b)
                mask_pixels[x, y] = min(255, darkness * 8)
    
    # Suaviza a máscara nas bordas
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    
    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    result.paste(img_rgba, (0, 0))
    result.putalpha(mask)
    return result


def add_portrait_with_shadow(canvas: Image.Image, portrait: Image.Image, x: int, y: int) -> Image.Image:
    """Cola o retrato no canvas com sombra suave embaixo"""
    pw, ph = portrait.size
    
    # ─ Sombra ─
    shadow_alpha = portrait.split()[3] if portrait.mode == "RGBA" else Image.new("L", portrait.size, 200)
    shadow_alpha_blurred = shadow_alpha.filter(ImageFilter.GaussianBlur(12))
    shadow = Image.new("RGBA", (pw, ph), (20, 15, 50, 120))
    shadow.putalpha(shadow_alpha_blurred)
    
    shadow_canvas = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sx = max(0, x + 8)
    sy = max(0, y + 12)
    pw2 = min(pw, canvas.width - sx)
    ph2 = min(ph, canvas.height - sy)
    if pw2 > 0 and ph2 > 0:
        shadow_crop = shadow.crop((0, 0, pw2, ph2))
        shadow_canvas.paste(shadow_crop, (sx, sy), shadow_crop)
    
    result = Image.alpha_composite(canvas, shadow_canvas)
    
    # ─ Retrato ─
    portrait_canvas = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    px2 = max(0, x)
    py2 = max(0, y)
    pw3 = min(pw, canvas.width - px2)
    ph3 = min(ph, canvas.height - py2)
    if pw3 > 0 and ph3 > 0:
        portrait_crop = portrait.crop((0, 0, pw3, ph3))
        portrait_canvas.paste(portrait_crop, (px2, py2), portrait_crop)
    
    return Image.alpha_composite(result, portrait_canvas)


# ─── Layout dos retratos ─────────────────────────────────────────────────────
# Formato: (filename, row, col_index, phrase)
LAYOUT = [
    # FUNDO
    ("Kawan.png",        0, 0, "Pode parcelar?"),
    ("Percio.png",       0, 1, "Podem escolher,\neu topo"),
    ("Marcelo.png",      0, 2, "Já fiz planilha\npra isso"),
    ("Paulo.png",        0, 3, "Depende...\ntodo mundo vai?"),
    # MEIO
    ("elaine.png",       1, 0, "Organizadora de\ntodos os detalhes"),
    ("Maria alice.png",  1, 1, "Ninguém vai saber\nque eu tô indo"),
    ("Nana.png",         1, 2, "A gente\ntopa tudo"),
    ("Sandra.png",       1, 3, "Que dia\nque é mesmo?"),
    # FRENTE
    ("Priscila.png",     2, 0, "Tá caro,\nmas bora"),
    ("Yaskara.png",      2, 1, "Organizo, traduzo\ne ainda pago"),
    ("wanessa.png",      2, 2, "Promotora oficial\ndo caos"),
]

# Configurações de cada fila (relativo ao A3)
ROW_CFG = {
    0: dict(
        n=4,
        height_pct=0.40,   # 40% da altura do poster
        y_start_pct=0.38,  # começa em 38% do poster
        margin_pct=0.18,   # corta 18% das margens laterais
        spacing_factor=1.0,
    ),
    1: dict(
        n=4,
        height_pct=0.50,
        y_start_pct=0.46,
        margin_pct=0.16,
        spacing_factor=1.0,
    ),
    2: dict(
        n=3,
        height_pct=0.60,
        y_start_pct=0.54,
        margin_pct=0.14,
        spacing_factor=1.0,
    ),
}

def draw_phrase(canvas: Image.Image, text: str, x: int, y: int, font):
    """Desenha o texto com uma borda branca para leitura fácil"""
    draw = ImageDraw.Draw(canvas)
    
    # Calcula bounding box para centralizar
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    # Posiciona texto: centralizado no x fornecido
    tx = x - tw // 2
    ty = y - th // 2
    
    # Borda branca (stroke/outline)
    outline_color = (255, 255, 255, 220)
    for adj_x in range(-3, 4):
        for adj_y in range(-3, 4):
            if adj_x == 0 and adj_y == 0: continue
            draw.multiline_text((tx + adj_x, ty + adj_y), text, font=font, fill=outline_color, align="center")
            
    # Texto em azul escuro marinho (para combinar com S.F.K)
    draw.multiline_text((tx, ty), text, font=font, fill=(20, 30, 60, 255), align="center")
    return canvas


def compose_v3():
    print("\n🌴 COMPOSITOR v3 — PÔSTER PUNTA CANA 2026")
    print("=" * 50)
    
    # Garante a fonte
    font_path = Path("/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf")
    
    from PIL import ImageFont
    try:
        font = ImageFont.truetype(str(font_path), 36)
    except:
        font = ImageFont.load_default()
    
    # Carrega e redimensiona o pôster base
    print("📄 Carregando pôster base...")
    base = Image.open(POSTER_BASE).convert("RGBA")
    
    # O pôster base é quadrado — estende verticalmente para A3
    bw, bh = base.size
    # Redimensiona para A3_W mantendo proporção, depois adiciona espaço
    scale = A3_W / bw
    new_h = int(bh * scale)
    base_resized = base.resize((A3_W, new_h), Image.LANCZOS)
    
    # Cria canvas A3 com fundo creme
    canvas = Image.new("RGBA", (A3_W, A3_H), (255, 252, 240, 255))
    
    # Cola o pôster base centrado verticalmente (ou do topo)
    y_offset = 0  # Começa do topo
    canvas.paste(base_resized, (0, y_offset), base_resized)
    
    print(f"   Base: {A3_W}×{new_h}px → canvas {A3_W}×{A3_H}px")
    
    # ─ Zona de colagem ─
    # Preserva header (0-35%) e banner (83-100%)
    COL_TOP = int(A3_H * 0.36)
    COL_BTM = int(A3_H * 0.82)
    COL_L = int(A3_W * 0.02)
    COL_R = int(A3_W * 0.98)
    COL_W = COL_R - COL_L
    COL_H = COL_BTM - COL_TOP
    
    print(f"\n📸 Zona da colagem: ({COL_L},{COL_TOP}) → ({COL_R},{COL_BTM})")
    print(f"   Tamanho: {COL_W}×{COL_H}px\n")
    
    # ─ Processa retratos por fila ─
    layers = []
    
    for filename, row, col, phrase in LAYOUT:
        path = OUTPUTS_DIR / filename
        if not path.exists():
            print(f"   ⚠️  Não encontrado: {filename}")
            continue
        
        cfg = ROW_CFG[row]
        n = cfg["n"]
        target_h = int(A3_H * cfg["height_pct"])
        y_start = int(A3_H * cfg["y_start_pct"])
        
        # Carrega, recorta e prepara
        raw = Image.open(path).convert("RGBA")
        char = crop_character(raw, target_h, margin_pct=cfg["margin_pct"])
        char_fe = create_character_with_feathered_edges(char)
        
        cw, ch = char_fe.size
        
        # Posição X: distribui uniformemente
        slot_w = COL_W // n
        x_center = COL_L + slot_w * col + slot_w // 2
        
        # Alternância Y para profundidade
        y_alt = int(ch * 0.05) if col % 2 == 1 else 0
        
        x = x_center - cw // 2
        y = y_start + y_alt
        
        # Clipa às bordas
        x = max(COL_L - int(cw * 0.12), min(x, COL_R - int(cw * 0.88)))
        y = max(COL_TOP, min(y, COL_BTM - int(ch * 0.4)))
        
        layers.append({
            "img": char_fe, 
            "pos": (x, y), 
            "z": row, 
            "name": filename, 
            "phrase": phrase,
            "center_x": x + cw // 2,
            "center_y": y + int(ch * 0.15) # Texto perto da altura dos ombros/cabeça
        })
        print(f"   [R{row}C{col}] {filename} → ({x},{y}) size={cw}×{ch}")
    
    # ─ Compõe em ordem z (fundo primeiro) ─
    print(f"\n🖌️  Compondo {len(layers)} retratos e frases...")
    layers.sort(key=lambda l: l["z"])
    
    for layer in layers:
        # 1. Desenha sombra e retrato
        canvas = add_portrait_with_shadow(canvas, layer["img"], *layer["pos"])
        # 2. Desenha frase do personagem (um pouco para o lado)
        offset_x = -90 if layer["pos"][0] > (A3_W // 2) else 90
        px = layer["center_x"] + offset_x
        py = layer["center_y"]
        canvas = draw_phrase(canvas, layer["phrase"], px, py, font)
    
    # ─ Salva ─
    print(f"\n💾 Salvando...")
    final = canvas.convert("RGB")
    final.save(OUTPUT_FINAL, "PNG", dpi=(150, 150))
    
    mb = OUTPUT_FINAL.stat().st_size / 1024 / 1024
    print(f"✅ {OUTPUT_FINAL.name}")
    print(f"   {A3_W}×{A3_H}px @ 150dpi | {mb:.1f} MB")
    return OUTPUT_FINAL


if __name__ == "__main__":
    result = compose_v3()
    print(f"\n🎉 CONCLUÍDO: {result}")
