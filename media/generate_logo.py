"""Generate the 512x512 ForeverTracking radar logo with Pillow."""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


SIZE = 512
SCALE = 3
S = SIZE * SCALE
C = S // 2


def point(x, y):
    return round(x * SCALE), round(y * SCALE)


def box(x0, y0, x1, y1):
    return (*point(x0, y0), *point(x1, y1))


def radar_point(radius, angle):
    radians = math.radians(angle)
    return point(
        C / SCALE + math.cos(radians) * radius,
        C / SCALE + math.sin(radians) * radius,
    )


def build():
    low = Image.new("RGBA", (256, 256))
    pixels = low.load()
    for y in range(256):
        for x in range(256):
            distance = min(1, math.hypot(x - 111, y - 101) / 220)
            pixels[x, y] = (
                round(33 - distance * 27),
                round(82 - distance * 66),
                round(119 - distance * 91),
                255,
            )

    background = low.resize((S, S), Image.Resampling.BICUBIC)
    rounded = Image.new("L", (S, S))
    ImageDraw.Draw(rounded).rounded_rectangle(
        (0, 0, S - 1, S - 1), radius=88 * SCALE, fill=255
    )
    background.putalpha(rounded)

    for bounds, color, blur in (
        (box(88, 61, 328, 301), (64, 127, 255, 80), 45),
        (box(283, 178, 443, 338), (165, 79, 255, 62), 30),
        (box(155, 157, 357, 359), (34, 247, 196, 55), 36),
    ):
        glow = Image.new("RGBA", (S, S))
        ImageDraw.Draw(glow).ellipse(bounds, fill=color)
        background = Image.alpha_composite(
            background, glow.filter(ImageFilter.GaussianBlur(blur * SCALE))
        )

    art = Image.new("RGBA", (S, S))
    draw = ImageDraw.Draw(art)

    draw.ellipse(box(63, 63, 449, 449), fill=(5, 14, 30, 220))
    draw.ellipse(box(71, 71, 441, 441), outline=(14, 39, 57, 255), width=18 * SCALE)
    draw.ellipse(box(77, 77, 435, 435), outline=(49, 215, 199, 255), width=7 * SCALE)
    draw.ellipse(box(87, 87, 425, 425), outline=(174, 255, 231, 180), width=2 * SCALE)
    draw.ellipse(box(118, 118, 394, 394), outline=(62, 173, 182, 185), width=4 * SCALE)
    draw.ellipse(box(160, 160, 352, 352), outline=(103, 224, 205, 190), width=5 * SCALE)

    for angle in range(0, 360, 15):
        major = angle % 45 == 0
        start_radius = 171 if major else 179
        end_radius = 193 if major else 189
        draw.line(
            [radar_point(start_radius, angle), radar_point(end_radius, angle)],
            fill=(222, 255, 242, 255) if major else (95, 201, 196, 230),
            width=(5 if major else 3) * SCALE,
        )

    sweep = Image.new("RGBA", (S, S))
    sweep_draw = ImageDraw.Draw(sweep)
    sector = [point(256, 256)] + [
        radar_point(141, angle) for angle in range(-104, -24, 2)
    ]
    sweep_draw.polygon(sector, fill=(43, 238, 194, 72))
    art = Image.alpha_composite(art, sweep)
    draw = ImageDraw.Draw(art)

    draw.arc(box(75, 75, 437, 437), 206, 299, fill=(147, 255, 226, 255), width=8 * SCALE)
    draw.arc(box(116, 116, 396, 396), 20, 117, fill=(121, 235, 216, 235), width=5 * SCALE)
    draw.arc(box(159, 159, 353, 353), 194, 280, fill=(185, 255, 230, 235), width=5 * SCALE)

    for first, last in (
        ((256, 98), (256, 184)),
        ((256, 328), (256, 414)),
        ((98, 256), (184, 256)),
        ((328, 256), (414, 256)),
    ):
        draw.line([point(*first), point(*last)], fill=(129, 211, 211, 175), width=3 * SCALE)

    sweep_line = Image.new("RGBA", (S, S))
    ImageDraw.Draw(sweep_line).line(
        [point(256, 256), radar_point(141, -52)],
        fill=(72, 255, 214, 255),
        width=8 * SCALE,
    )
    art = Image.alpha_composite(
        art, sweep_line.filter(ImageFilter.GaussianBlur(10 * SCALE))
    )
    draw = ImageDraw.Draw(art)
    draw.line(
        [point(256, 256), radar_point(141, -52)],
        fill=(154, 255, 226, 255),
        width=5 * SCALE,
    )

    target = radar_point(92, -52)
    target_glow = Image.new("RGBA", (S, S))
    target_draw = ImageDraw.Draw(target_glow)
    for radius, alpha in ((38, 35), (28, 75), (18, 150)):
        x, y = target
        target_draw.ellipse(
            (x - radius * SCALE, y - radius * SCALE,
             x + radius * SCALE, y + radius * SCALE),
            outline=(255, 176, 79, alpha),
            width=5 * SCALE,
        )
    art = Image.alpha_composite(
        art, target_glow.filter(ImageFilter.GaussianBlur(13 * SCALE))
    )
    draw = ImageDraw.Draw(art)
    draw.ellipse(
        (target[0] - 22 * SCALE, target[1] - 22 * SCALE,
         target[0] + 22 * SCALE, target[1] + 22 * SCALE),
        fill=(255, 184, 78, 255),
        outline=(255, 246, 207, 255),
        width=5 * SCALE,
    )
    draw.ellipse(
        (target[0] - 8 * SCALE, target[1] - 8 * SCALE,
         target[0] + 8 * SCALE, target[1] + 8 * SCALE),
        fill=(255, 255, 235, 255),
    )

    draw.ellipse(
        (C - 26 * SCALE, C - 26 * SCALE, C + 26 * SCALE, C + 26 * SCALE),
        fill=(14, 49, 62, 255),
        outline=(107, 255, 220, 255),
        width=7 * SCALE,
    )
    draw.ellipse(
        (C - 13 * SCALE, C - 13 * SCALE, C + 13 * SCALE, C + 13 * SCALE),
        fill=(230, 255, 243, 255),
    )

    background = Image.alpha_composite(background, art)
    return background.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


if __name__ == "__main__":
    destination = Path(__file__).with_name("logo.png")
    build().save(destination, optimize=True)
    print(destination)
