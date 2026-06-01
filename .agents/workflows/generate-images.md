# Workflow: /gerar-imagens

Este arquivo documenta as regras operacionais associadas ao slash command `/gerar-imagens` do ecossistema **PPT-CREATOR**.

## Descrição do Fluxo

```
   [Início] -> Creative Visual Specialist lê roteiro.json e DESIGN.md
                |
                v
   Gera prompts visuais (image_prompt) com 40% de White Space e Zero Texto
                |
                v
   Dispara Script TypeScript: npx ts-node src/tools/generate_images.ts
                |
       +--------+--------+
       |                 |
[MOCK_IMAGES=true]   [MOCK_IMAGES=false]
       |                 |
Gera mockups locais PNG   Chama API Gemini Nano Banana Pro
       |                 |
       +--------+--------+
                |
                v
   Salva PNGs em artifacts/images/ e atualiza image_path no roteiro.json
                |
                v
   Avança para o Workflow /deploy-deck
```

## Instruções de Execução do Comando

1. **Geração de Conceitos Criativos**:
   - O `creative-visual-specialist` lê os slides do `roteiro.json` que exigem elementos gráficos.
   - Escreve as diretrizes de prompt estruturado em `image_concept` e `image_prompt`.

2. **Engenharia de Prompts**:
   - Força o cumprimento das duas diretrizes críticas:
     - Sem texto sintético na imagem gerada.
     - Reserva de pelo menos 40% de espaço livre (baixo contraste/gradiente sólido) na lateral correspondente ao posicionamento tipográfico.

3. **Invocação de Mídia**:
   - Rodar o pipeline de imagens via:
     ```bash
     npm run images
     ```
   - **Condição de Fallback**: Se `MOCK_IMAGES=true` no arquivo `.env`, o pipeline desvia as requisições HTTP e escreve diretamente imagens de teste sólidas no formato PNG na pasta `artifacts/images/` para poupar créditos da API Gemini.
   - **Download Real**: Se as credenciais estiverem habilitadas, conecta-se ao Gemini Nano Banana Pro para baixar os arquivos PNG em 4K.

4. **Persistência de Referências**:
   - Gravar os caminhos relativos locais em `image_path` dentro do arquivo `artifacts/roteiro.json`.
   - Avançar o estado e encaminhar para `/deploy-deck`.
