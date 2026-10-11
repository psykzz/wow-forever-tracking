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
    return point(C / SCALE + math.cos(radians) * radius, C / SCALE + math.sin(radians) * radius)


def build():
    low = Image.new("RGBA", (256, 256))
    pixels = low.load()
    for y in range(256):
        for x in range(256):
            distance = min(1, math.hypot(x - 128, y - 128) / 190)
            pixels[x, y] = (
                round(25 - distance * 13),
                round(42 - distance * 18),
                round(58 - distance * 19),
                255,
            )

    background = low.resize((S, S), Image.Resampling.BICUBIC)
    rounded = Image.new("L", (S, S))
    ImageDraw.Draw(rounded).rounded_rectangle(
        (0, 0, S - 1, S - 1), radius=84 * SCALE, fill=255
    )
    background.putalpha(rounded)

    glow = Image.new("RGBA", (S, S))
    ImageDraw.Draw(glow).ellipse(box(145, 140, 367, 362), fill=(44, 211, 186, 64))
    background = Image.alpha_composite(
        background, glow.filter(ImageFilter.GaussianBlur(32 * SCALE))
    )

    art = Image.new("RGBA", (S, S))
    draw = ImageDraw.Draw(art)

    draw.ellipse(box(70, 70, 442, 442), outline=(5, 17, 27, 200), width=18 * SCALE)
    draw.ellipse(box(76, 76, 436, 436), outline=(61, 198, 184, 210), width=5 * SCALE)
    draw.ellipse(box(116, 116, 396, 396), outline=(55, 148, 158, 150), width=3 * SCALE)
    draw.ellipse(box(157, 157, 355, 355), outline=(90, 208, 194, 180), width=4 * SCALE)

    for angle in range(0, 360, 15):
        major = angle % 45 == 0
        start_radius = 174 if major else 180
        end_radius = 193
        draw.line(
            [radar_point(start_radius, angle), radar_point(end_radius, angle)],
            fill=(149, 232, 221, 230) if major else (91, 171, 174, 190),
            width=(4 if major else 2) * SCALE,
        )

    sweep = Image.new("RGBA", (S, S))
    sweep_draw = ImageDraw.Draw(sweep)
    sector = [point(256, 256)] + [radar_point(137, angle) for angle in range(-76, -14, 2)]
    sweep_draw.polygon(sector, fill=(39, 218, 176, 54))
    art = Image.alpha_composite(art, sweep)
    draw = ImageDraw.Draw(art)

    draw.arc(box(119, 119, 393, 393), 206, 304, fill=(114, 247, 211, 245), width=5 * SCALE)
    draw.line([point(256, 256), radar_point(137, -45)], fill=(130, 255, 220, 245), width=5 * SCALE)

    draw.line([point(256, 100), point(256, 185)], fill=(139, 215, 209, 190), width=3 * SCALE)
    draw.line([point(256, 327), point(256, 412)], fill=(139, 215, 209, 190), width=3 * SCALE)
    draw.line([point(100, 256), point(185, 256)], fill=(139, 215, 209, 190), width=3 * SCALE)
    draw.line([point(327, 256), point(412, 256)], fill=(139, 215, 209, 190), width=3 * SCALE)

    target = radar_point(91, -45)
    target_glow = Image.new("RGBA", (S, S))
    ImageDraw.Draw(target_glow).ellipse(
        (target[0] - 20 * SCALE, target[1] - 20 * SCALE,
         target[0] + 20 * SCALE, target[1] + 20 * SCALE),
        fill=(255, 190, 86, 170),
    )
    art = Image.alpha_composite(art, target_glow.filter(ImageFilter.GaussianBlur(12 * SCALE)))
    draw = ImageDraw.Draw(art)
    draw.ellipse(
        (target[0] - 13 * SCALE, target[1] - 13 * SCALE,
         target[0] + 13 * SCALE, target[1] + 13 * SCALE),
        fill=(255, 207, 115, 255),
        outline=(255, 244, 204, 255),
        width=3 * SCALE,
    )
    draw.ellipse(
        (C - 17 * SCALE, C - 17 * SCALE, C + 17 * SCALE, C + 17 * SCALE),
        fill=(229, 255, 243, 255),
        outline=(57, 186, 166, 255),
        width=5 * SCALE,
    )

    background = Image.alpha_composite(background, art)
    return background.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


if __name__ == "__main__":
    destination = Path(__file__).with_name("logo.png")
    build().save(destination, optimize=True)
    print(destination)
