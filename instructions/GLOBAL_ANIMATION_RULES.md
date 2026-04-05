ANIMATION_RULES:

Structure per scene:
1. Create objects (no animation)
2. Introduce base elements
3. Main transformation
4. Emphasis
5. Transition

Continuity:
- ALWAYS reuse objects if possible
- Prefer Transform() over FadeOut/FadeIn
- Duplicate only for comparison

Positioning:
- Use next_to(), align_to(), arrange()
- Avoid absolute coordinates

Complexity:
- Max 3 simultaneous animations
- Break complex ideas into steps

Transitions:
- Prefer morphing (Transform)
- Use slide-out for tables/genes

- ALWAYS reuse objects (Transform > FadeOut/FadeIn)
- Keep metabolic model persistent until Step 5
- Toy networks must be identical copies (use duplicate)

- Arrow colors:
   ↑ = orange
   ↓ = purple

- Highlight:
   ONLY yellow glow (never change object color)

- Flux:
   encoded ONLY via line thickness

- Scene pacing:
   ~8–10 seconds per major step

- Avoid clutter:
   max 3 simultaneous animations