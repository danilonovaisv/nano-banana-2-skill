---
description: # 05 Image Prompts Generation
---

# 05 Image Prompts Generation

## Owner Agent
@creative-visual-specialist

## Purpose
Generate visual prompts for layette slides with no text rules.

## Inputs
artifacts/roteiro.json

## Outputs
artifacts/prompts/image-prompts.json

## Preconditions
roteiro.json is fully updated.

## Steps
1. Formulate 16:9 aspect ratio style prompts.
2. Apply the strict negative prompt: "no text, no letters, no watermark...".
3. Match exactly 59 slides.

## Validation Gates
Prompt gate: no-text constraints verified.

## Failure Modes
Image prompt formatting failure or text content inclusion.

## Rollback / Recovery
Regenerate image prompts from the template.

## Human Approval Required
Review of generated image prompts by Creative Visual Specialist.

## Status
ACTIVE
