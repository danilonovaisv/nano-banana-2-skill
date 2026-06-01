# Workflow: Geração de Ativos de Vídeo (`generate-video-assets`)

Este workflow é acionado quando o usuário deseja automatizar o pipeline de Image-to-Video (I2V) usando ferramentas locais e mecanismos de IA de vídeo, estruturado inteiramente em torno do processamento de imagens e vídeos locais.

## Etapas de Execução

### 1. Verificação de Inputs e Prompts Existentes

Antes de iniciar qualquer geração, o sistema deve escanear as pastas de mídias:

* **Imagem de Entrada (`/medias/inputs`):**
  - Verifica se há arquivos de imagem compatíveis (ex: `.png`, `.jpg`, `.jpeg`, `.webp`) no diretório `/medias/inputs/`.
  - Se uma imagem for encontrada, ela será adotada diretamente como o frame inicial (`base_frame`), pulando a etapa de geração de imagem sintética (Etapa 2), servindo como referência de estilo e conteúdo para o vídeo.
  
* **Prompt de Instrução (`/medias/prompts`):**
  - Verifica se há arquivos de instrução (ex: `.txt`, `.json`, `.md`) no diretório `/medias/prompts/`.
  - Se houver, o conteúdo destes arquivos deve ser lido e mesclado com as diretrizes criativas de animação (câmera, física, movimento) para guiar o motor de vídeo de forma precisa.

### 2. Geração da Imagem Base (`nano-banana`) - Condicional

* **Cenário A: Sem imagem de entrada em `/medias/inputs`**
  - Caso não exista imagem pré-fornecida, executa a CLI `nano-banana` para criar o frame inicial de altíssima qualidade a partir do prompt de conceito visual.
  - *Comando:*
    ```bash
    bun run src/cli.ts "[PROMPT VISUAL]" -a [ASPECT_RATIO] -s 2K -o /medias/outputs/base_frame
    ```
  - Isso gerará o arquivo `/medias/outputs/base_frame.png`.

* **Cenário B: Com imagem de entrada em `/medias/inputs`**
  - Ignora a geração de imagem sintética e copia a imagem fornecida para o diretório de saídas como frame base:
    ```bash
    # Identifica o primeiro arquivo de imagem no diretório de inputs
    INPUT_IMAGE=$(find /medias/inputs -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.webp" \) | head -n 1)
    cp "$INPUT_IMAGE" /medias/outputs/base_frame.png
    ```

### 3. Geração do Vídeo via API (Kling AI / Seedance 2.0)

Passa a imagem base `/medias/outputs/base_frame.png` para a API de vídeo juntamente com as instruções de movimento.

* **Construção do Prompt de Movimento:**
  - O prompt de movimento deve priorizar as diretrizes lidas dos arquivos de instrução em `/medias/prompts/` (ex: `prompt.txt`), complementando-as com parâmetros de dinâmica de câmera.
  - *Exemplo de leitura de prompt de instrução:*
    ```bash
    # Lê a instrução personalizada, senão recorre ao prompt de movimento padrão
    IF_PROMPT=$(cat /medias/prompts/* 2>/dev/null | head -n 10)
    PROMPT_MOVIMENTO="${IF_PROMPT:-[PROMPT DE MOVIMENTO PADRÃO]}"
    ```
* *Exemplo de Chamada de SDK/API:*
  ```bash
  muapi-seedance-2 run --input /medias/outputs/base_frame.png --prompt "$PROMPT_MOVIMENTO" --duration 5 --output /medias/outputs/output_video
  ```

### 4. Pós-Processamento e Salvamento das Saídas

* Garanta que todos os artefatos resultantes (frame de referência, arquivos de vídeo finais `.mp4`, prompts consolidados e logs) sejam salvos de forma organizada no diretório `/medias/outputs/`.
