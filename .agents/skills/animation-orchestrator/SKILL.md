---
name: animation-orchestrator
description: Coordenador de animações web interativas de alto desempenho utilizando GSAP, Framer Motion e Lottie.
---

# Skill: animation-orchestrator

Esta skill fornece diretrizes e blocos de código para implementar animações web ricas e interativas.

## Métodos de Animação Recomendados

### 1. Sequenciamento Complexo com GSAP
Ideal para animações interdependentes e orquestração cronometrada em grande escala.

```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Timeline básica com ScrollTrigger
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".section-container",
    start: "top 80%",
    end: "bottom 20%",
    scrub: true
  }
});

tl.from(".box", { opacity: 0, y: 50, duration: 1 })
  .to(".box", { scale: 1.2, duration: 0.5 });
```

### 2. Transições de Estado com Framer Motion
Ideal para componentes de interface dinâmicos e transições de rotas em frameworks React.

```jsx
import { motion } from 'framer-motion';

export const MotionButton = () => (
  <motion.button
    whileHover={{ scale: 1.05, boxShadow: "0px 0px 8px rgb(0,72,255)" }}
    whileTap={{ scale: 0.95 }}
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ duration: 0.3 }}
  >
    Interativo
  </motion.button>
);
```

## Diretrizes de Otimização de Performance
* Utilize sempre propriedades `transform` (`translateX`, `translateY`, `scale`, `rotate`) e `opacity`. Elas não causam repaints na thread principal e rodam diretamente na GPU.
* Limite o uso de eventos como `scroll` e `resize` atrelando-os a `requestAnimationFrame` ou utilizando triggers otimizados como o `ScrollTrigger` do GSAP.
