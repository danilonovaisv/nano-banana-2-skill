---
name: video-generation-agent
description: Orquestrador de pipelines de geração de vídeo por IA (Kling AI, Seedance 2.0) e processamento pós-geração.
---

# Skill: video-generation-agent

Esta skill gerencia a integração com geradores de vídeo por IA e ferramentas de edição para criar mídia dinâmica.

## Fluxo de Geração Recomendado

### 1. Preparação do Asset de Origem (Text-to-Image / I2I)
Utilize a CLI do `nano-banana` para gerar uma imagem base com o estilo e proporções corretos.

```bash
# Exemplo de geração de imagem de referência widescreen 16:9
nano-banana "futuristic neon city street, cinematic lighting, 8k" -a 16:9 -o base-frame
```

### 2. Conversão de Imagem para Vídeo (I2V)
Chame a API de vídeo (e.g. Seedance 2.0 ou Kling AI) informando a imagem gerada no passo anterior como frame de referência.

```bash
# Exemplo conceitual de chamada de ferramenta ou API para animar a imagem base
muapi-seedance-2 run --input base-frame.png --prompt "neon lights flickering, slow forward camera zoom, rain falling" --duration 5
```

## Engenharia de Prompt para Vídeo
* **Foco no Movimento:** Descreva a física dos elementos (ex: "water flowing", "dust particles floating in light beam").
* **Direção de Câmera:** Especifique o movimento físico da câmera (ex: "cinematic slow panning shot", "360-degree camera orbit").
* **Estética Visual:** Combine descritores estéticos no final do prompt (ex: "highly detailed, raytracing, 8k resolution, cinematic color grading").
