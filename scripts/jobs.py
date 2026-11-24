"""Prompt sweep for Vulpix full-art outpainting. Same padded canvas each time."""

TRIGGER = ("Outpaint the image: replace the solid gray areas with a seamless continuation of the scene, "
           "keeping the existing picture unchanged.\nScene: ")

TAIL = (" Soft pastel palette, smooth 3D storybook shading, gentle depth of field, cohesive single illustration, "
        "no text, no border, no watermark, no sticker, no other characters.")

JOBS = [
    dict(name="a_spring_202", seed=202, prompt=TRIGGER +
         "a small six-tailed fire fox sitting on a pale winding path in a lush spring garden. Continue the path "
         "behind it into a bright, hazy clearing between leafy bushes, and extend upward into a luminous canopy of "
         "fresh green leaves with gentle sunbeams from the upper right. Below, continue the meadow into a foreground "
         "of clover, grass blades and softly blurred coral and white wildflowers. Warm cream light, sage and mint "
         "greens, delicate orange accents, floating pollen." + TAIL),
    dict(name="a_spring_303", seed=303, prompt=TRIGGER +
         "a small six-tailed fire fox sitting on a pale winding path in a lush spring garden. Continue the path "
         "behind it into a bright, hazy clearing between leafy bushes, and extend upward into a luminous canopy of "
         "fresh green leaves with gentle sunbeams from the upper right. Below, continue the meadow into a foreground "
         "of clover, grass blades and softly blurred coral and white wildflowers. Warm cream light, sage and mint "
         "greens, delicate orange accents, floating pollen." + TAIL),
    dict(name="b_golden_202", seed=202, prompt=TRIGGER +
         "the same gentle storybook garden at golden hour. The fox sits on a pale path; behind it the path curves "
         "into a sunlit clearing. Above the leafy bushes, soft treetops open to a warm apricot and honey sky with "
         "thin clouds; low golden sunlight streams from the upper left, rim-lighting the leaves and the fox's fur. "
         "The foreground meadow glows amber, with clover, tall grass and tiny orange wildflowers. A few warm embers "
         "and pollen motes float in the air. Warm oranges and sage greens." + TAIL),
    dict(name="b_golden_303", seed=303, prompt=TRIGGER +
         "the same gentle storybook garden at golden hour. The fox sits on a pale path; behind it the path curves "
         "into a sunlit clearing. Above the leafy bushes, soft treetops open to a warm apricot and honey sky with "
         "thin clouds; low golden sunlight streams from the upper left, rim-lighting the leaves and the fox's fur. "
         "The foreground meadow glows amber, with clover, tall grass and tiny orange wildflowers. A few warm embers "
         "and pollen motes float in the air. Warm oranges and sage greens." + TAIL),
    dict(name="c_blossom_202", seed=202, prompt=TRIGGER +
         "a spring garden under blossoming cherry trees. Pale pink petals drift through the air and gather on the "
         "pale path and grass. Above the leafy bushes, a canopy of soft pink blossoms and delicate branches opens "
         "to a pale blue sky, with warm afternoon light filtering through. Continue the foreground into clover, "
         "small white flowers and drifting petals. Mint green and blush pink palette, warm cream light." + TAIL),
    dict(name="c_blossom_303", seed=303, prompt=TRIGGER +
         "a spring garden under blossoming cherry trees. Pale pink petals drift through the air and gather on the "
         "pale path and grass. Above the leafy bushes, a canopy of soft pink blossoms and delicate branches opens "
         "to a pale blue sky, with warm afternoon light filtering through. Continue the foreground into clover, "
         "small white flowers and drifting petals. Mint green and blush pink palette, warm cream light." + TAIL),
    dict(name="d_mist_202", seed=202, prompt=TRIGGER +
         "a quiet garden at dawn. A pale peach sky glows above layers of misty treetops; soft fog drifts between "
         "the bushes, dew beads on the grass, leaves are backlit, and gentle cool teal shadows contrast with warm "
         "pink highlights. The pale path fades into the mist behind the fox. Continue the foreground into wet "
         "clover, moss and tiny pale flowers. Dreamy, low-contrast, luminous." + TAIL),
    dict(name="d_mist_303", seed=303, prompt=TRIGGER +
         "a quiet garden at dawn. A pale peach sky glows above layers of misty treetops; soft fog drifts between "
         "the bushes, dew beads on the grass, leaves are backlit, and gentle cool teal shadows contrast with warm "
         "pink highlights. The pale path fades into the mist behind the fox. Continue the foreground into wet "
         "clover, moss and tiny pale flowers. Dreamy, low-contrast, luminous." + TAIL),
    dict(name="e_edge_202", seed=202, prompt=TRIGGER +
         "a garden opening onto a broad forest-edge clearing. Above the leafy bushes, distant treetops and rolling "
         "green hills recede under a soft blue sky with hazy white clouds; late-afternoon sun comes from the upper "
         "right. The pale path continues down through the foreground meadow, framed by tall grasses, clover and "
         "coral wildflowers. Airy, luminous, spacious composition with a clear sky opening above the fox." + TAIL),
    dict(name="e_edge_303", seed=303, prompt=TRIGGER +
         "a garden opening onto a broad forest-edge clearing. Above the leafy bushes, distant treetops and rolling "
         "green hills recede under a soft blue sky with hazy white clouds; late-afternoon sun comes from the upper "
         "right. The pale path continues down through the foreground meadow, framed by tall grasses, clover and "
         "coral wildflowers. Airy, luminous, spacious composition with a clear sky opening above the fox." + TAIL),
    dict(name="f_twilight_101", seed=101, prompt=TRIGGER +
         "the same garden at blue-hour twilight. A deep teal and soft violet sky above the treetops, with the last "
         "peach glow on the horizon; fireflies and warm embers glow among the bushes, and the pale path reflects a "
         "faint cool light. The fox's orange fur catches warm firelight. Continue the foreground into dark green "
         "grass, moss and tiny glowing flowers. Cinematic, painterly, soft, magical." + TAIL),
    dict(name="g_close_202", seed=202, prompt=TRIGGER +
         "a lush garden seen from a low, intimate angle. Large out-of-focus leaves and flowers frame the foreground "
         "bottom corners, the pale path continues behind the fox, and a soft canopy of leaves with warm light fills "
         "the top. Shallow depth of field with the fox in sharp focus, creamy foreground bokeh, gentle sunbeams, "
         "floating pollen, fresh green and coral palette." + TAIL),
]
