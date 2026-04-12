from PIL import Image, ImageDraw, ImageFont
import imageio
import numpy as np

width, height = 1080, 1920
bg_color = (58, 27, 51)  # aubergine
text_color = (230, 200, 160)  # sable

frames = []
fps = 12
duration = 4
total_frames = fps * duration

font = ImageFont.truetype("DejaVuSans-Bold.ttf", 90)

text = "Bientôt disponible"

for i in range(total_frames):
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    bbox = draw.textbbox((0,0), text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]

    scale = 0.95 + 0.05*(i/total_frames)
    new_w, new_h = int(tw*scale), int(th*scale)

    temp = Image.new("RGBA", (tw, th), (0,0,0,0))
    temp_draw = ImageDraw.Draw(temp)
    temp_draw.text((0,0), text, font=font, fill=text_color)
    temp = temp.resize((new_w, new_h))

    x = (width - new_w)//2
    y = (height - new_h)//2

    if i < total_frames*0.2:
        alpha = i/(total_frames*0.2)
    elif i > total_frames*0.8:
        alpha = (total_frames-i)/(total_frames*0.2)
    else:
        alpha = 1

    alpha_mask = temp.split()[3].point(lambda p: int(p*alpha))
    img.paste(temp, (x,y), alpha_mask)

    frames.append(np.array(img))

imageio.mimsave("bientot_disponible.mp4", frames, fps=fps)