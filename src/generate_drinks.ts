import { spawn } from "child_process";
import { join, extname, basename } from "path";
import { existsSync } from "fs";

interface CharacterConfig {
  filename: string;
  note: string;
  drink: string;
}

const CHARACTERS: CharacterConfig[] = [
  { filename: "wanessa.JPG", note: "Promotora oficial do caos", drink: "glass of chopp" },
  { filename: "Yaskara.JPG", note: "Organizo, traduzo e ainda pago", drink: "glass of chopp" },
  { filename: "elaine.jpeg", note: "Organizadora de todos os detalhes", drink: "tropical drink cocktail" },
  { filename: "Marcelo.png", note: "Já fiz planilha pra isso", drink: "caipirinha" },
  { filename: "Paulo .jpeg", note: "Depende... todo mundo vai?", drink: "glass of red wine" },
  { filename: "Sandra .PNG", note: "Que dia que é mesmo?", drink: "colorful tropical drink" },
  { filename: "Percio.jpeg", note: "Podem escolher, eu topo", drink: "glass of chopp" },
  { filename: "Nana.jpeg", note: "A gente topa tudo", drink: "glass of whisky" },
  { filename: "Kawan.PNG", note: "Pode parcelar?", drink: "glass of chopp" },
  { filename: "Priscila.jpeg", note: "Tá caro, mas bora", drink: "champagne flute" },
  { filename: "Maria alice.jpeg", note: "Ninguém vai saber que eu tô indo", drink: "glass of whisky" }
];

const INPUT_DIR = join(process.cwd(), "medias", "inputs");
const OUTPUT_DIR = join(process.cwd(), "medias", "outputs");
const CONCURRENCY_LIMIT = 2; // Limite de chamadas simultâneas à API para evitar rate limit

// Retorna uma Promise que resolve quando a execução do CLI terminar
function generateCharacterImage(config: CharacterConfig): Promise<{ success: boolean; file?: string; error?: string }> {
  return new Promise((resolve) => {
    const inputPath = join(INPUT_DIR, config.filename);
    if (!existsSync(inputPath)) {
      resolve({ success: false, error: `Arquivo de entrada não encontrado: ${inputPath}` });
      return;
    }

    // Normaliza o nome base para o arquivo de saída (ex: "Paulo .jpeg" -> "Paulo")
    const cleanBaseName = config.filename.substring(0, config.filename.lastIndexOf(".")).trim();

    // Formular o prompt em inglês de alta fidelidade focado em consistência de identidade
    const prompt = `Transform the subject into a highly detailed hand-drawn sketchbook illustration created with colored pencils, ink lines, cross-hatching, and natural shading. Replace the original outfit with stylish beachwear appropriate for a tropical vacation (swimwear, beach shorts, light beach clothing), while maintaining a natural fit and realistic fabric details. The character must be holding a ${config.drink} and have a handwritten comic-style designer annotation near them containing exactly the phrase: "${config.note}". Render the phrase as playful handwritten sketchbook annotations integrated into the illustration, connected to the character with designer-style arrows, doodles, and concept-art callouts. Use a completely pure white background with no notebook paper, no textures, no scenery, and no environmental elements. Surround the character with playful designer-sketch annotations, hand-drawn arrows, doodles, comic-style notes such as "WOW!" and "COOL!", and concept-art markings. Add a subtle smooth red-to-yellow glowing outline around the character. Maintain a polished sketchbook concept-art aesthetic with warm tones, rough sketch lines, high detail, and professional illustration quality. Keep full-body proportions intact. Preserve the exact identity, facial likeness, hairstyle, body shape, pose, composition, and camera perspective of the original reference image. No extra people, no additional props beyond the specified drink, no logos, no watermarks, no background objects, and no changes to the subject's likeness.`;

    console.log(`[+] Iniciando geração: ${config.filename} -> Bebida: ${config.drink}...`);

    const args = [
      "run",
      "src/cli.ts",
      prompt,
      "-r",
      inputPath,
      "-o",
      cleanBaseName,
      "-d",
      OUTPUT_DIR,
      "-s",
      "1K", // 1K por padrão para velocidade e custo controlado
    ];

    const proc = spawn("bun", args);

    let stdout = "";
    let stderr = "";

    proc.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    proc.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    proc.on("close", (code) => {
      if (code === 0) {
        console.log(`[✔] Concluído com sucesso: ${config.filename} (${cleanBaseName})`);
        resolve({ success: true, file: join(OUTPUT_DIR, `${cleanBaseName}.png`) });
      } else {
        console.error(`[❌] Erro ao processar ${config.filename}. Código de saída: ${code}`);
        console.error(`    Stderr: ${stderr.trim()}`);
        resolve({ success: false, error: stderr.trim() });
      }
    });
  });
}

// Orquestrador de paralelismo limitado
async function main() {
  console.log(`=== Iniciando Pipeline de Geração de Bebidas ===`);
  console.log(`Total de personagens para processar: ${CHARACTERS.length}`);
  console.log(`Concorrência máxima: ${CONCURRENCY_LIMIT}\n`);

  const results: Record<string, { success: boolean; file?: string; error?: string }> = {};
  const queue = [...CHARACTERS];
  const activeWorkers: Promise<void>[] = [];

  const runWorker = async () => {
    while (queue.length > 0) {
      const next = queue.shift();
      if (!next) break;

      results[next.filename] = await generateCharacterImage(next);
    }
  };

  // Cria workers paralelos limitados pela concorrência
  for (let i = 0; i < Math.min(CONCURRENCY_LIMIT, CHARACTERS.length); i++) {
    activeWorkers.push(runWorker());
  }

  // Aguarda todos os workers terminarem
  await Promise.all(activeWorkers);

  console.log(`\n=== Relatório de Geração ===`);
  let successes = 0;
  let failures = 0;

  for (const [filename, res] of Object.entries(results)) {
    if (res.success) {
      successes++;
      console.log(` - ${filename}: [SUCESSO] -> ${res.file}`);
    } else {
      failures++;
      console.error(` - ${filename}: [FALHA] -> ${res.error}`);
    }
  }

  console.log(`\nProcessamento finalizado: ${successes} com sucesso, ${failures} falhas.`);
  if (failures > 0) {
    process.exit(1);
  }
}

main().catch((err) => {
  console.error("Erro fatal na execução do orquestrador:", err);
  process.exit(1);
});
