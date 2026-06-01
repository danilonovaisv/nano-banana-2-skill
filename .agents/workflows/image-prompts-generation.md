---
description: # Workflow: Geração de Prompts de Imagem
---

# Workflow: Geração de Prompts de Imagem (`image-prompts-generation`)

Este workflow detalha a preparação, refinamento e consolidação de prompts de imagem usados no pipeline de síntese visual e animação de vídeo.

## Owner Agent

@creative-visual-specialist

## Purpose

Gerar, enriquecer e validar os prompts textuais de imagem que serão fornecidos aos motores de IA, incorporando instruções personalizadas fornecidas pelo usuário e garantindo a conformidade estética.

## Inputs

- `/medias/prompts/` (arquivos de instruções customizadas, ex: `prompt.txt`)
- `/medias/inputs/` (imagens de referência do usuário para guiar o estilo, se houver)

## Outputs

- `/medias/outputs/refined-prompts.json` ou `/medias/outputs/prompt_log.txt` (prompts consolidados e higienizados)

## Preconditions

- Diretórios de mídias (`/medias/inputs`, `/medias/prompts` e `/medias/outputs`) devidamente inicializados.

## Steps

1. **Varredura e Coleta de Inputs**:
   - Escanear `/medias/prompts/` para identificar diretrizes específicas (estilo artístico, proporção, iluminação, paleta de cores).
   - Escanear `/medias/inputs/` para analisar imagens que sirvam de guia ou semente estilística.

2. **Formulação do Prompt Consolidado**:
   - Combinar as instruções de estilo coletadas com prompts padrão de alta qualidade estética (ex: renderização 3D detalhada, cinematográfica, fotorrealista).
   - Ajustar proporções e parâmetros técnicos com base nas diretrizes.
   - **Interação com o Usuário (Personagens)**: Para cada personagem presente na cena descrita ou no prompt, o agente deve obrigatoriamente questionar o usuário qual bebida esse personagem estará segurando antes de finalizar a formulação.

3. **Aplicação de Regras de Prompt Negativo**:
   - Adicionar de forma mandatória instruções negativas estritas para remover anomalias e elementos indesejados: `"no text, no letters, no watermark, no signatures, bad anatomy, low quality"`.

4. **Persistência de Metadados**:
   - Salvar os prompts estruturados finais em um arquivo de log ou configuração de saída em `/medias/outputs/` para auditoria do pipeline de geração.

## Validation Gates

- **Filtro de Texto**: Garantir que nenhum prompt solicite a renderização de caracteres tipográficos explícitos.
- **Validação de Sintaxe**: Verificar se os prompts estão formatados em strings limpas e prontas para as APIs de geração.

## Status

ACTIVE
