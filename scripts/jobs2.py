"""Second sweep: more narrative full-art scenes."""
TRIGGER = ("Outpaint the image: replace the solid gray areas with a seamless continuation of the scene, "
           "keeping the existing picture unchanged.\nScene: ")
TAIL = (" Soft pastel palette, smooth 3D storybook shading, gentle depth of field, cohesive single illustration, "
        "no text, no border, no watermark, no sticker, no other characters.")

JOBS = [
    dict(name="h_stream_202", seed=202, prompt=TRIGGER +
         "a small six-tailed fire fox sitting beside a clear shallow stream in a sunlit forest glade. The pale path "
         "curves behind it into the trees. Continue the foreground into the stream: smooth pebbles under clear water, "
         "gentle ripples and soft reflections, mossy banks, ferns and watercress at the water's edge, tiny white "
         "flowers. Above, a luminous canopy of fresh green leaves with dappled sunbeams. Warm cream light, sage and "
         "mint greens, delicate orange accents." + TAIL),
    dict(name="h_stream_303", seed=303, prompt=TRIGGER +
         "a small six-tailed fire fox sitting beside a clear shallow stream in a sunlit forest glade. The pale path "
         "curves behind it into the trees. Continue the foreground into the stream: smooth pebbles under clear water, "
         "gentle ripples and soft reflections, mossy banks, ferns and watercress at the water's edge, tiny white "
         "flowers. Above, a luminous canopy of fresh green leaves with dappled sunbeams. Warm cream light, sage and "
         "mint greens, delicate orange accents." + TAIL),
    dict(name="i_bluebell_202", seed=202, prompt=TRIGGER +
         "a magical bluebell wood in spring. Drifts of blue-violet bluebells carpet the foreground under slender "
         "birch trees; ferns, mossy roots and fallen branches frame the edges, and the pale path winds back into a "
         "hazy sunlit clearing. Above, a high canopy of young green leaves with soft sunbeams and a few drifting "
         "petals. Cool blue-violet accents against warm sage green and cream light." + TAIL),
    dict(name="i_bluebell_303", seed=303, prompt=TRIGGER +
         "a magical bluebell wood in spring. Drifts of blue-violet bluebells carpet the foreground under slender "
         "birch trees; ferns, mossy roots and fallen branches frame the edges, and the pale path winds back into a "
         "hazy sunlit clearing. Above, a high canopy of young green leaves with soft sunbeams and a few drifting "
         "petals. Cool blue-violet accents against warm sage green and cream light." + TAIL),
    dict(name="j_late_202", seed=202, prompt=TRIGGER +
         "a late-summer meadow at the edge of an oak wood. Tall golden grasses and ripe seed heads fill the "
         "foreground, with late poppies and cornflowers; the pale path leads back between sun-warmed bushes. Above, "
         "a canopy of deep green leaves with a few yellowing edges opens to a soft blue sky and hazy clouds. Warm "
         "honey light, long soft shadows, gentle breeze." + TAIL),
    dict(name="j_late_303", seed=303, prompt=TRIGGER +
         "a late-summer meadow at the edge of an oak wood. Tall golden grasses and ripe seed heads fill the "
         "foreground, with late poppies and cornflowers; the pale path leads back between sun-warmed bushes. Above, "
         "a canopy of deep green leaves with a few yellowing edges opens to a soft blue sky and hazy clouds. Warm "
         "honey light, long soft shadows, gentle breeze." + TAIL),
]
