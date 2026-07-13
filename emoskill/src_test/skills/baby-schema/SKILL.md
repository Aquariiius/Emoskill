---
name: "baby-schema"
description: "Uses Lorenz's baby schema to analyze how infantile proportions in human infants, young animals, or neotenic designs elicit cuteness, approach, and caregiving, while checking distress, danger, and uncanny overrides."
---

# Baby Schema / Kindchenschema
## Purpose
Infer visible vulnerability, benignity, and caregiving demand from infantile proportions, then map them to approach-oriented VA. Age labels or the word 'cute' are not evidence by themselves.
## Routing Card
USE WHEN:
- Neotenic morphology is the main affective source in an infant, young animal, or intentionally infantile design.
- Multiple facial or bodily proportions jointly support low defensiveness, dependence, and caregiving motivation.
DO NOT USE WHEN:
- Danger, injury, crying, attack, or exploitation dominates the image.
- Uncanny mismatch, pathological contamination, or predatory morphology drives the response.
VISUAL TRIGGERS:
- Large head-to-body ratio, high forehead, round face, large low-set eyes, small nose and mouth.
- Short limbs, rounded body, soft material, and low-aggression contour.
NEAR-MISS BOUNDARIES:
- Young subject in danger, illness, or pain -> `cognitive-appraisal`.
- Young animal with attack or venom morphology -> `evolved-fear-module`.

## Core Constructs
- **Baby-schema load**: number and clarity of independent facial and bodily proportion cues.
- **Visible vulnerability**: small size, limited movement or defense, or dependent posture.
- **Benign safety**: whether the subject appears relaxed, protected, healthy, and free from immediate threat.
- **Caregiving and override**: approach, holding, protection, and soothing; distress, danger, or uncanny cues can override positivity.

## Use When
Use when silhouette and proportions alone, without the category label 'baby' or 'young animal', still explain the main approach and caregiving response.
## Do-Not-Use-When Rules
- Mild baby-faced features in adults count only as Weak evidence.
- Do not infer intelligence, personality, health, or real caregiving need from appearance.
- Do not let cuteness erase visible injury, threat, or exploitation.

## Applicability
- **Strong**: at least three independent baby-schema cues in a safe context with no override.
- **Partial**: neoteny is clear, but activity, context, or mild distress competes.
- **Weak**: only stylized cuteness, category labels, or a few proportion cues.
- **Not applicable**: neoteny is unclear or another mechanism dominates; final VA equals Direct.

## Reasoning Steps
1. Identify subject type, but do not treat age or species labels as final evidence.
2. Describe head-to-body ratio, forehead, eye position, facial roundness, nose/mouth size, limb length, and material softness.
3. Count independent infantile features and rule out lens distortion or generic cartoon exaggeration.
4. Infer visible vulnerability from size, defensive capacity, and dependent posture, not actual health.
5. Check safety, caregiver presence, crying, injury, restraint, contamination, and uncanny mismatch.
6. Infer action tendency: approach, hold, protect, soothe, or withdraw because of an override.
7. Derive Valence from benignity and caregiving fulfillment; derive Arousal from activity, crying, and caregiving urgency.
8. Compare cognitive appraisal and animal threat as alternatives, then set applicability and Direct weight.

## VA Mapping
| Visible state | Valence | Arousal |
|---|---:|---:|
| Multiple baby-schema cues; calm and safe | 8.3–10.0 | 3.0–5.5 |
| Clear neoteny with active interaction | 8.0–9.8 | 4.9–7.2 |
| Limited or stylized neoteny | 6.4–8.0 | 3.3–5.5 |
| Crying, injury, danger, or uncanny override | 2.4–5.5 | 5.3–8.7 |

## Direct-Anchor Rule
- First estimate the skill-specific `skill_candidate`, then compute `final = direct + w × (skill_candidate - direct)`.
- Use fixed weights: `strong=0.85`, `partial=0.55`, `weak=0.25`, and `not_applicable=0`; lower fit must remain closer to Direct VA.
- If evidence supports only Valence or only Arousal, the unsupported dimension must use a weight no greater than 0.25; extreme scores require strong fit and multiple convergent cues.
## Boundary Notes
- This skill models morphology-triggered caregiving, not the rule that every young subject is positive.
- At Partial or Weak fit, the baby-schema candidate may only modestly adjust Direct and must not override clear event emotion.

## Worked Example
A round-faced, large-eyed, short-limbed puppy rests on a soft blanket: multiple neotenic proportions and a safe context support caregiving, yielding a high-positive, low-to-moderate candidate. Visible injury would downgrade fit and pull the final score toward Direct.

## Output Format
Return fixed JSON with baby-schema evidence, safety context, override check, caregiving tendency, Direct inputs, candidate VA, blend weight, and final VA.
