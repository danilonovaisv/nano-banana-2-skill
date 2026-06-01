---
description: # Workflow: Audit Motion Performance (`/audit-motion-performance`)
---

# Workflow: Audit Motion Performance (`/audit-motion-performance`)

Este workflow é acionado para perfilar a taxa de quadros, o consumo de recursos e eventuais travamentos (jank) em páginas que possuem animações pesadas.

## Etapas de Execução

### 1. Inicializar Navegador de Teste

Abra uma sessão no Playwright usando a skill `chrome-devtools`.

* *Ação:* Navegar para a URL local ou de produção que contém as animações.

### 2. Executar Captura de Performance (Trace)

Inicie a gravação de trace do Chrome DevTools focando em "Rendering" e "Frames".

* Interaja com a página (execute scroll, cliques em botões animados, hover em elementos de glassmorphism).

### 3. Extrair Métricas de Frame Rate (FPS)

Analise o log do console e os dados de rendering para calcular a taxa de quadros (FPS):

* **Ideal:** Mantido acima de 55 FPS.
* **Jank Detectado:** Quedas repentinas de frames abaixo de 30 FPS durante transições interativas.

### 4. Gerar Relatório de Otimização

Se houver gargalos detectados:

* Verifique se propriedades não otimizadas (e.g. `margin`, `top`/`left`, `width`/`height`) estão sendo animadas.
* Sugira a substituição por propriedades transformadas (`transform: translate3d`).
* Grave screenshots da timeline de frames para o relatório final.
