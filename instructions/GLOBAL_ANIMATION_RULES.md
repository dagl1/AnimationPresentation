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