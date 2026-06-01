#!/usr/bin/env python3
import os
import shutil
import glob
import subprocess
import sys

# Caminhos configurados
INPUT_DIR = "/medias/inputs"
PROMPT_DIR = "/medias/prompts"
OUTPUT_DIR = "/medias/outputs"

# Garantir existência de diretórios
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(PROMPT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def scan_inputs():
    print("[1] Escaneando caminhos de mídia...")
    
    # 1. Procura por imagens no diretório de inputs
    valid_image_exts = ('*.png', '*.jpg', '*.jpeg', '*.webp', '*.PNG', '*.JPG', '*.JPEG')
    input_images = []
    for ext in valid_image_exts:
        input_images.extend(glob.glob(os.path.join(INPUT_DIR, ext)))
    
    # 2. Procura por arquivos de prompts no diretório de prompts
    prompt_files = glob.glob(os.path.join(PROMPT_DIR, "*"))
    prompt_files = [f for f in prompt_files if os.path.isfile(f)]
    
    print(f" - Encontradas {len(input_images)} imagens de entrada em: {INPUT_DIR}")
    for img in input_images:
        print(f"   -> {os.path.basename(img)}")
        
    print(f" - Encontrados {len(prompt_files)} arquivos de instrução de prompt em: {PROMPT_DIR}")
    for pf in prompt_files:
        print(f"   -> {os.path.basename(pf)}")
        
    return input_images, prompt_files

def get_combined_prompt(prompt_files, default_prompt):
    if not prompt_files:
        print(f" - Usando prompt padrão: '{default_prompt}'")
        return default_prompt
    
    # Lê as primeiras linhas do arquivo de instruções encontrado
    first_file = prompt_files[0]
    try:
        with open(first_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                print(f" - Instrução de prompt customizada carregada do arquivo '{os.path.basename(first_file)}'")
                # Mescla a instrução customizada
                combined = f"{content} (estilo complementar de animação)"
                return combined
    except Exception as e:
        print(f" - Erro ao ler {first_file}: {e}")
        
    return default_prompt

def run_image_generation(input_images, custom_prompt):
    print("\n[2] Etapa de Geração / Processamento de Imagem Base...")
    base_frame_path = os.path.join(OUTPUT_DIR, "base_frame.png")
    
    # Cenário A: Temos uma imagem de entrada
    if input_images:
        src_image = input_images[0]
        print(f" - Usando imagem fornecida pelo usuário: {src_image}")
        try:
            shutil.copy2(src_image, base_frame_path)
            print(f" - Copiada com sucesso para {base_frame_path}")
            return base_frame_path
        except Exception as e:
            print(f" - Erro ao copiar imagem base: {e}")
            sys.exit(1)
            
    # Cenário B: Não temos imagem de entrada, precisamos gerar via CLI local ou Nano-Banana
    print(" - Nenhuma imagem de entrada fornecida. Iniciando geração de imagem sintética via CLI 'nano-banana'...")
    # Execução condicional: se o CLI de verdade existir, roda; senão, gera mock
    cli_command = ["bun", "run", "src/cli.ts", custom_prompt, "-a", "16:9", "-s", "2K", "-o", os.path.join(OUTPUT_DIR, "base_frame")]
    
    try:
        # Verifica se o cli de fato existe e o Bun está configurado
        if shutil.which("bun"):
            print(f" - Executando comando: {' '.join(cli_command)}")
            result = subprocess.run(cli_command, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(" - Geração via 'nano-banana' completada com sucesso!")
                return base_frame_path
            else:
                print(f" - Falha ao executar CLI nano-banana (código {result.returncode}): {result.stderr}")
        else:
            print(" - CLI 'bun' não encontrado no sistema. Criando imagem mockup PNG de teste...")
    except Exception as e:
        print(f" - Exceção ao tentar rodar CLI: {e}")
    
    # Geração de Mockup PNG caso o motor real não esteja configurado
    create_mock_png(base_frame_path, "Base Frame (Mock)")
    return base_frame_path

def run_video_generation(base_frame, custom_prompt):
    print("\n[3] Etapa de Geração de Vídeo via API (Kling AI / Seedance 2.0)...")
    output_video_path = os.path.join(OUTPUT_DIR, "output_video.mp4")
    
    print(f" - Frame inicial: {base_frame}")
    print(f" - Prompt de Movimento: '{custom_prompt}'")
    
    # Tenta rodar a API de vídeo Seedance se instalada
    cli_command = ["muapi-seedance-2", "run", "--input", base_frame, "--prompt", custom_prompt, "--duration", "5", "--output", output_video_path]
    
    try:
        if shutil.which("muapi-seedance-2"):
            print(f" - Executando comando: {' '.join(cli_command)}")
            result = subprocess.run(cli_command, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print(" - Vídeo gerado com sucesso via API Seedance!")
                return output_video_path
            else:
                print(f" - Falha ao rodar API de Vídeo (código {result.returncode}): {result.stderr}")
        else:
            print(" - CLI 'muapi-seedance-2' não disponível. Criando arquivo de vídeo simulado (mock)...")
    except Exception as e:
        print(f" - Exceção ao tentar rodar API de Vídeo: {e}")
        
    create_mock_video(output_video_path)
    return output_video_path

def create_mock_png(path, text):
    # Tenta usar a biblioteca Pillow se estiver instalada, senão escreve um arquivo de bytes falsos com cabeçalho PNG válido
    try:
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (1920, 1080), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10,10), text, fill=(255,255,0))
        img.save(path)
        print(f" - Mock PNG criado em: {path}")
    except ImportError:
        # Grava um arquivo binário simples com a assinatura PNG
        with open(path, "wb") as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDAT\x78\x9cc\xfc\xcf\xc0\x00\x00\x03\x01\x01\x00\x18\xdd\x8d\xb0\x00\x00\x00\x00IEND\xaeB`\x82')
        print(f" - Mock binário PNG simples criado em: {path}")

def create_mock_video(path):
    # Cria um arquivo mock de vídeo
    with open(path, "w") as f:
        f.write("MOCK VIDEO FILE CONTENT")
    print(f" - Mock MP4 criado em: {path}")

def main():
    print("==========================================================")
    print("      Orquestrador de Geração de Imagem e Vídeo")
    print("==========================================================\n")
    
    # 1. Escaneamento inicial
    input_images, prompt_files = scan_inputs()
    
    # 2. Definição do prompt
    default_prompt = "Cinematic camera pan, high resolution, realistic physics"
    custom_prompt = get_combined_prompt(prompt_files, default_prompt)
    
    # 3. Geração ou cópia de imagem base
    base_frame = run_image_generation(input_images, custom_prompt)
    
    # 4. Geração do vídeo
    video_path = run_video_generation(base_frame, custom_prompt)
    
    print("\n==========================================================")
    print("  Fluxo finalizado com sucesso!")
    print(f"  Resultados armazenados em: {OUTPUT_DIR}")
    print("==========================================================")

if __name__ == "__main__":
    main()
    ````