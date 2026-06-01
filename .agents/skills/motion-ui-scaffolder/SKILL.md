---
name: motion-ui-scaffolder
description: Construtor de interfaces ricas com micro-interações usando Magic UI, Aceternity e Tailwind CSS.
---

# Skill: motion-ui-scaffolder

Esta skill instrui o agente sobre como projetar layouts interativos e visualmente impressionantes de acordo com a estética "Ghost Era".

## Estética "Ghost Era" - Padrões de Design
* **Cores Principais:** 
  * `bluePrimary`: `#0048ff`
  * `blueAccent`: `#4fe6ff`
  * `background`: `#040013`
* **Grid:** Elementos principais sempre estruturados em uma grid padrão (`.std-grid` ou classes `grid-cols`).
* **Visual Premium:** Uso de glassmorphism, gradientes suaves, bordas sutis e contraste controlado.

## Boilerplate de Componente Premium com Tailwind

```html
<div class="relative overflow-hidden rounded-xl border border-white/10 bg-[#040013]/80 p-6 backdrop-blur-md transition-all duration-300 hover:border-[#0048ff]/50 hover:shadow-[0_0_20px_rgba(0,72,255,0.15)]">
  <!-- Efeito de gradiente no hover -->
  <div class="absolute -right-12 -top-12 h-24 w-24 rounded-full bg-gradient-to-br from-[#0048ff] to-[#4fe6ff] opacity-10 blur-xl transition-opacity duration-300 group-hover:opacity-20"></div>
  
  <h3 class="text-xl font-semibold text-white">Ghost Component</h3>
  <p class="mt-2 text-sm text-gray-400">Layout interativo e otimizado com micro-animação.</p>
</div>
```

## Diretrizes de Acessibilidade (A11y)
* Garanta que todos os elementos interativos tenham focos visíveis claros (`focus-visible:ring-2`).
* Respeite a preferência de animações reduzidas do sistema operacional utilizando media queries:
  ```css
  @media (prefers-reduced-motion: reduce) {
    * {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
  ```
