#!/usr/bin/env python3
"""
Gerador do Pôster PUNTA CANA 2026 - THE LEGENDARY EDITION
Usa a API OpenAI gpt-image-1 (GPT Image 2) com imagens de referência
"""

import os
import base64
import json
from pathlib import Path
from openai import OpenAI

# Configuração
OPENAI_API_KEY = "sk-proj-zh0mLV516RakDBpNstBdblEvL7BfLf4ElScF7O3Me-tB047sTQ1j8UbtI3bYsXQGXkBETZ17_cT3BlbkFJO8UgNqyGcXLQMZhLHp5Fp02GsJ0g_V8t7M-"
OUTPUTS_DIR = Path("/Users/PROJETOS-DEV/GERADOR-DE-IMAGENS/medias/outputs")
POSTER_OUTPUT = OUTPUTS_DIR / "PUNTA_CANA_2026_POSTER_A3.png"

# Portraits disponíveis (na ordem de aparição no pôster)
PORTRAIT_FILES = [
    "Kawan.png",
    "Marcelo.png", 
    "Maria alice.png",
    "Nana.png",
    "Paulo.png",
    "Percio.png",
    "Priscila.png",
    "Sandra.png",
    "Yaskara.png",
    "elaine.png",
    "wanessa.png",
]

def image_to_base64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_all_portrait_refs():
    """Prepara as 10 melhores referências de retratos (limite da API)"""
    refs = []
    # Selecionar até 10 portraits (limite GPT Image 2 edit)
    selected = PORTRAIT_FILES[:10]
    
    for filename in selected:
        path = OUTPUTS_DIR / filename
        if path.exists():
            ext = path.suffix.lower().replace('.', '')
            if ext == 'jpg':
                ext = 'jpeg'
            b64 = image_to_base64(path)
            refs.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/{ext};base64,{b64}"
                }
            })
            print(f"  ✓ Adicionado retrato: {filename}")
    
    return refs


POSTER_PROMPT = """Create a vibrant, premium tropical festival poster in A3 vertical format (portrait orientation, 2:3 ratio). This is a high-quality print-ready poster for a group trip to Punta Cana 2026.

TYPOGRAPHY (exact text, no variations):
- TOP: Large bold arched text "PUNTA CANA" curved upward like a rainbow, thick golden-yellow vintage display font with dark navy blue outline and white highlight. Very large, dominant.
- Below arch: Large bold centered text "2026" in the same golden style
- Below that: Elegant italic text "THE LEGENDARY EDITION" in coral-orange/sunset color

CENTRAL COLLAGE (most important area):
- Arrange ALL the reference characters from the input images in a fun group collage
- Position them in 3 overlapping rows filling the center: back row 4 people, middle row 4 people, front row 3 people
- Each character keeps their sketch-art illustration style, tropical beachwear, and holds their drink
- Characters overlap slightly at edges, with soft white halos blending them together
- Small fun sketch annotations between characters: doodles, stars, wave lines
- The entire group looks like a joyful vacation photo reimagined as illustrated concept art

TROPICAL DECORATIVE ELEMENTS (surrounding the collage):
- Lush colorful illustrated palm trees in corners, coconut trees on sides
- Tropical flowers: hibiscus, plumeria in pink, yellow, orange, red
- Monstera and banana leaves spreading from corners
- Illustrated cocktail glasses, pineapples, starfish scattered
- Sun with radiating rays at top center above the arch
- Sailboat silhouette on the horizon
- Tiki bar illustration on one side
- Colorful tropical birds (toucan, parrot)
- Beach umbrella, flip flops, sunglasses
- Ocean wave border at the bottom transition area

BACKGROUND:
- Warm cream/ivory/sandy white main background
- Subtle watercolor wash gradient: coral pink on left side fading to turquoise on right
- Sandy beach texture at very bottom
- Light tropical pattern dots or confetti in background

BOTTOM NAUTICAL BANNER:
- Solid deep navy blue horizontal band across the full bottom
- Thick decorative rope border on top edge of banner
- Left side: Anchor icon in gold
- Center top: Large bold white serif text "S.F.K"
- Center middle: "SILVA • FERNANDES • KAWASAKI" in white, wide letter-spacing
- Center bottom: "EST. PUNTA CANA 2026" in white smaller text
- Right side: Anchor icon in gold
- Small wave/nautical rope decorations

OVERALL STYLE:
- Premium tropical festival poster aesthetic
- Vibrant, saturated tropical colors (turquoise, coral, golden yellow, lime green, hot pink)
- Sketch-art illustration meets watercolor background
- Playful but sophisticated and print-ready
- Clean, no watermarks, no copyright symbols
- High detail, sharp edges on typography, lush illustrated decorations"""

def generate_poster_with_references():
    """Gera o pôster usando GPT Image 2 com as imagens de referência"""
    print("\n🌴 Gerando Pôster PUNTA CANA 2026 - THE LEGENDARY EDITION")
    print("=" * 60)
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Preparar referências de retratos
    print("\n📸 Carregando retratos de referência...")
    portrait_refs = get_all_portrait_refs()
    print(f"  Total: {len(portrait_refs)} retratos carregados\n")
    
    print("🎨 Enviando para GPT Image 2 (gpt-image-1)...")
    print("   Aguarde, isso pode levar 30-60 segundos...\n")
    
    try:
        # Usar o endpoint de edit com referências
        response = client.images.edit(
            model="gpt-image-1",
            image=[
                # Primeira imagem (primária - Kawan como referência principal)
                open(OUTPUTS_DIR / "Kawan.png", "rb"),
            ],
            prompt=POSTER_PROMPT,
            size="1024x1536",
            n=1,
        )
        
        # Salvar o resultado
        image_data = response.data[0]
        
        if hasattr(image_data, 'b64_json') and image_data.b64_json:
            img_bytes = base64.b64decode(image_data.b64_json)
            with open(POSTER_OUTPUT, 'wb') as f:
                f.write(img_bytes)
            print(f"✅ Pôster salvo em: {POSTER_OUTPUT}")
        elif hasattr(image_data, 'url') and image_data.url:
            import urllib.request
            urllib.request.urlretrieve(image_data.url, POSTER_OUTPUT)
            print(f"✅ Pôster baixado e salvo em: {POSTER_OUTPUT}")
        
        return str(POSTER_OUTPUT)
        
    except Exception as e:
        print(f"❌ Erro na geração: {e}")
        print("\n🔄 Tentando com endpoint text-to-image (sem referências)...")
        return generate_poster_text_only(client)

def generate_poster_text_only(client):
    """Fallback: gera apenas com texto se o edit falhar"""
    response = client.images.generate(
        model="gpt-image-1",
        prompt=POSTER_PROMPT,
        size="1024x1536",
        n=1,
        response_format="b64_json",
    )
    
    image_data = response.data[0]
    img_bytes = base64.b64decode(image_data.b64_json)
    
    with open(POSTER_OUTPUT, 'wb') as f:
        f.write(img_bytes)
    
    print(f"✅ Pôster (text-only) salvo em: {POSTER_OUTPUT}")
    return str(POSTER_OUTPUT)


if __name__ == "__main__":
    result = generate_poster_with_references()
    print(f"\n🎉 Concluído! Arquivo: {result}")
    print(f"   Tamanho: {Path(result).stat().st_size / 1024 / 1024:.1f} MB")
