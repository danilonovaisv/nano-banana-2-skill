---
description: # Workflow: /gerar-imagens
---

# Workflow: /gerar-imagens

Este arquivo documenta as regras operacionais associadas ao comando `/gerar-imagens` para geração autônoma de imagens no ambiente, estruturado de forma independente de qualquer geração de slides ou apresentações.

## Descrição do Fluxo

```
                        [Início]
                            |
                            v
            Verifica `/medias/inputs` e `/medias/prompts`
                            |
     +----------------------+----------------------+
     |                                             |
 (Há imagem de input)                     (Não há imagem de input)
     |                                             |
 Usa imagem de entrada diretamente             Lê instruções de `/medias/prompts/`
 Copia para `/medias/outputs/`                Aplica diretrizes de prompt de imagem
     |                                             |
     |                                             v
     |                                  Dispara Script de Geração de Imagem:
     |                                  `nano-banana` ou script local
     |                                             |
     |                                    +--------+--------+
     |                                    |                 |
     |                             [MOCK_IMAGES=true]   [MOCK_IMAGES=false]
     |                                    |                 |
     |                             Gera mockups PNG      Chama Gemini Nano Banana Pro
     |                                    |                 |
     |                                    +--------+--------+
     |                                             |
     |                                 Salva PNGs em `/medias/outputs/`
     +----------------------+----------------------+
                            |
                            v
                         [Fim]
```

## Instruções de Execução do Comando

1. **Verificação de Entradas (`/medias/inputs` e `/medias/prompts`)**:
   - **Imagem de Entrada (`/medias/inputs/`)**: Antes de rodar qualquer modelo generativo, verifica-se se há arquivos de imagem pré-existentes na pasta de inputs. Se houver, o pipeline adota essa imagem diretamente, ignorando a geração inicial para poupar recursos e créditos, e copia o arquivo para a pasta de saídas `/medias/outputs/`.
   - **Instruções de Prompt (`/medias/prompts/`)**: Verifica-se a presença de arquivos de prompt ou diretrizes textuais (ex: arquivos `.txt` ou `.md`). Caso existam, o conteúdo deles é lido para parametrizar e refinar as instruções do prompt que guiará a geração de imagem.

2. **Engenharia de Prompts**:
   - Se nenhuma imagem de entrada for fornecida, o pipeline formula prompts de imagem com base nas especificações coletadas.
   - Força-se o cumprimento de duas regras fundamentais:
     - **Sem elementos de texto**: Aplica-se um prompt negativo restrito para evitar marcas d'água, letras, assinaturas ou textos sobrepostos.
     - **Alta fidelidade visual**: Resolução mínima de 2K ou superior, adaptando a proporção conforme as diretrizes lidas da pasta de prompts.

3. **Invocação de Mídia e Fallbacks**:
   - O pipeline tenta executar o script de geração.
   - **Automação de Personagens com Bebidas**: Para a geração em lote dos personagens segurando bebidas no estilo sketchbook concept-art, utiliza-se o script `src/generate_drinks.ts` rodando no Bun:

     ```bash
     bun run src/generate_drinks.ts
     ```

     O script mapeia cada personagem da pasta `medias/inputs/` para sua respectiva bebida e aplica o prompt conceitual focado em manter a identidade e o estilo visual de caderno de desenhos com contorno brilhante e fundo branco puro.
   - **Modo de Simulação (Mock)**: Se o ambiente estiver configurado para simulação (`MOCK_IMAGES=true` ou falta de credenciais), o pipeline gera imagens mockadas sólidas no formato PNG na pasta `/medias/outputs/`.
   - **Execução Real**: Caso o sistema esteja integrado com APIs externas ou com a ferramenta local `nano-banana`, o pipeline executa a geração real salvando os PNGs resultantes diretamente em `/medias/outputs/`.
