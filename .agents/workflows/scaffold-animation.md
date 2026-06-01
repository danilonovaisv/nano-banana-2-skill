---
description: # Workflow: Scaffold Animation (`/scaffold-animation`)
---

# Workflow: Scaffold Animation (`/scaffold-animation`)

Este workflow é acionado quando o usuário deseja estruturar animações e transições complexas em uma página web ou componente.

## Etapas de Execução

### 1. Descoberta de Stack

Verifique se o projeto atual utiliza React, Next.js, HTML estático ou outra biblioteca de frontend.

* *Ação:* Ler o arquivo `package.json` do diretório de destino.

### 2. Escolha do Engine de Animação

* Se o projeto for **React / Next.js**, utilize **Framer Motion** para transições de componentes e **GSAP** para sequências complexas de scroll.
* Se o projeto for **HTML estático / Vanilla JS**, utilize **GSAP** ou **CSS Keyframes** nativos.

### 3. Injeção de Boilerplate

Gere um template de arquivo correspondente à stack selecionada.

* **Exemplo GSAP (Vanilla):**

  ```html
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <script>
    document.addEventListener("DOMContentLoaded", () => {
      gsap.from(".animate-item", {
        opacity: 0,
        y: 30,
        stagger: 0.2,
        duration: 1,
        ease: "power2.out"
      });
    });
  </script>
  ```

* **Exemplo Framer Motion (React):**

  ```jsx
  import { motion } from "framer-motion";
  
  export const FadeInList = ({ items }) => (
    <motion.ul initial="hidden" animate="visible" variants={{
      visible: { transition: { staggerChildren: 0.1 } }
    }}>
      {items.map((item, i) => (
        <motion.li key={i} variants={{
          hidden: { opacity: 0, y: 10 },
          visible: { opacity: 1, y: 0 }
        }}>
          {item}
        </motion.li>
      ))}
    </motion.ul>
  );
  ```

### 4. Validação Visual

Utilize a ferramenta de Browser Automation para carregar a página e confirmar que não há erros de runtime no console e que a animação renderiza corretamente.
