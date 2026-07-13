---
name: "baby-schema"
description: "Analyze caregiving affect from infantile morphology: large head ratio, high forehead, round face, large low-set eyes, small nose/mouth, short limbs, and soft proportions. Infer schema load, then check realism, safety, distress, danger, and uncanny overrides. Do not equate young age or the word baby with positive affect."
---

# Baby Schema / Kindchenschema

## Applicability Gate

REQUIRED:
- The dominant subject is a human infant, young animal, or deliberately neotenic character/object.
- Multiple infantile proportions are visible and plausibly drive tenderness or caregiving.
- Morphology remains affectively important after considering the surrounding situation.

REJECT:
- Adult face, ordinary small object, or culturally labeled "cute" subject without neotenic structure.
- Predatory morphology, contamination, body action, or social event is the primary mechanism.
- Severe distress, danger, illness, or uncanny wrongness fully determines affect; keep schema only as a modifier.

NEAR MISS:
- Adult expressive portrait -> facial-expression-affect; neutral adult portrait -> none.
- Young animal with credible attack threat -> evolved-fear-module.
- Infant visibly endangered or suffering -> cognitive-appraisal becomes primary.

## Visual Variables

- **Head/body proportion**: relatively large rounded head, short compact body.
- **Facial configuration**: high forehead, round face, large low-set eyes, chubby cheeks, small nose/mouth.
- **Limb/body form**: short limbs, rounded torso, soft contours, low angularity.
- **Realism/design**: real infant/young animal versus plush toy, chibi, doll, or robot.
- **Safety and overrides**: relaxed posture, care contact, play, sleep versus crying, injury, restraint, threat, uncanny likeness.

## Inference Procedure

1. Qualify the subject and list only visible infantile proportions.
2. Integrate features into low/medium/high schema load; category membership is insufficient.
3. Confirm the morphology supports approach/caregiving rather than threat or avoidance.
4. Check safety, distress, exploitation, and uncanny overrides.
5. Judge VA with the anchors; schema is a positive prior, context sets the branch.

## Arousal Gate

Cuteness is warm and LOW-activation: resting or gently posed subjects sit at 3.4-4.6. Raise
arousal above 5 only for visible energetic play, active approach, or distress. Big eyes and
soft fur are NOT activation cues. No activation cue -> arousal <= 4.5.

## VA Anchors (1-9)

| Case | Valence | Arousal |
|---|---:|---:|
| High schema load, safe/benign context | 7.2-8.2 | 3.8-5.0 |
| Moderate schema load, safe context | 6.5-7.4 | 3.4-4.6 |
| Energetic play with clear schema | 7.0-8.0 | 5.0-5.8 |
| Distress/danger/uncanny override | 3.0-4.5 | 5.0-6.0 |
| Weak fit | 5.2-6.2 | 3.5-4.5 |

Anchors are typical bands, not forced outputs; interpolate, and with thin evidence stay at the
band edge closest to neutral.

## Worked Examples

- **Calm**: A puppy with a large rounded head, big eyes, and short legs sleeps on a blanket in
  soft light. -> converging proportions, sleep, benign context; activation_evidence [].
  **V 7.6, A 3.6**, strong.
- **Active**: A laughing toddler crawls quickly toward the camera reaching out. -> high schema
  load plus visible energetic approach; activation_evidence ["fast crawling", "reaching
  motion"]. **V 7.8, A 5.4**, strong.

## Output Contract

In the shared JSON separate visible proportions, schema load, caregiving tendency,
safety/override cues, and top-level `activation_evidence` (empty list if none). Never infer
health, worth, or actual vulnerability.
