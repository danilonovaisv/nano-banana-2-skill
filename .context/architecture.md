# Repositorio Media & Animation Architecture

## Visão Geral
Este repositório (`nano-banana-2`) fornece recursos de geração de imagens baseados em IA através de uma interface CLI de alta performance e skills extensíveis. Este arquivo de contexto documenta a arquitetura de mídia integrada, com ênfase no pipeline de animação web e geração de vídeo com IA.

## Diretrizes e Padrões Tecnológicos

### 1. Stack de Animação Web (GSAP, Framer Motion, CSS)
* **GSAP (GreenSock):** Utilizado para animações complexas, sequências baseadas em timeline e manipulação fina do DOM / Canvas.
* **Framer Motion:** Preferido para animações de componentes em interfaces baseadas em React, transições de rotas e micro-interações de estado.
* **CSS Puro & Custom Properties:** Usado para animações básicas de transição e performance (e.g. `transform`, `opacity`) tirando proveito da aceleração de hardware.

### 2. Stack de Vídeo e Geração de Mídia por IA
* **Gemini (Flash e Pro):** Modelos nativos integrados no CLI `nano-banana` para geração de imagens ultra-rápidas.
* **Seedance 2.0 (ByteDance) & Kling AI:** Mecanismos sugeridos para animação temporal e conversão de imagem para vídeo (I2V).

## Fluxo Cognitivo da Infraestrutura de Agentes
A camada cognitiva `.agent/` opera orquestrada pelos agentes e scripts definidos para garantir a consistência das saídas geradas:
1. **Orquestrador:** Recebe o prompt criativo e divide a tarefa entre design de movimento e engenharia de vídeo.
2. **Motion Designer Agent:** Codifica ou otimiza o código da animação web.
3. **AI Video Engineer Agent:** Dispara os jobs de geração e edição de vídeo.
4. **Validador (Browser Automation):** Executa o render e captura screenshots do comportamento visual final.
