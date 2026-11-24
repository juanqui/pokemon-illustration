TRIGGER = ("Outpaint the image: replace the solid gray areas with a seamless continuation of the scene, "
           "keeping the existing picture unchanged.\nScene: ")
TAIL = (" Soft pastel palette, smooth 3D storybook shading, gentle depth of field, cohesive single illustration, "
        "no text, no border, no watermark, no sticker, no other characters.")
JOBS = [
    dict(name="k_blossom_stream_202", seed=202, prompt=TRIGGER +
         "a spring garden beside a clear shallow stream under blossoming cherry trees. The fox sits at the water's "
         "edge on a mossy bank; pale pink petals drift on the water and gather on the grass. Continue the foreground "
         "into the stream: smooth pebbles under clear water, gentle ripples and soft reflections, ferns and clover "
         "along the bank. Above, a canopy of soft pink cherry blossoms and delicate branches opens to a pale blue "
         "sky, with warm afternoon light filtering through. Mint green and blush pink palette, warm cream light." + TAIL),
    dict(name="k_blossom_stream_303", seed=303, prompt=TRIGGER +
         "a spring garden beside a clear shallow stream under blossoming cherry trees. The fox sits at the water's "
         "edge on a mossy bank; pale pink petals drift on the water and gather on the grass. Continue the foreground "
         "into the stream: smooth pebbles under clear water, gentle ripples and soft reflections, ferns and clover "
         "along the bank. Above, a canopy of soft pink cherry blossoms and delicate branches opens to a pale blue "
         "sky, with warm afternoon light filtering through. Mint green and blush pink palette, warm cream light." + TAIL),
    dict(name="l_golden_stream_202", seed=202, prompt=TRIGGER +
         "the same garden at golden hour, beside a clear shallow stream. The fox sits at the water's edge; low golden "
         "sunlight from the upper left rim-lights its fur. The foreground continues into the stream with smooth "
         "pebbles, warm amber reflections and gentle ripples; mossy banks, clover and tall grass line the water. "
         "Above, soft treetops open to an apricot and honey sky with thin clouds; a few warm embers and pollen motes "
         "drift in the air. Warm oranges and sage greens." + TAIL),
    dict(name="l_golden_stream_303", seed=303, prompt=TRIGGER +
         "the same garden at golden hour, beside a clear shallow stream. The fox sits at the water's edge; low golden "
         "sunlight from the upper left rim-lights its fur. The foreground continues into the stream with smooth "
         "pebbles, warm amber reflections and gentle ripples; mossy banks, clover and tall grass line the water. "
         "Above, soft treetops open to an apricot and honey sky with thin clouds; a few warm embers and pollen motes "
         "drift in the air. Warm oranges and sage greens." + TAIL),
]
