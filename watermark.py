from PIL import Image, ImageEnhance

def add_watermark(image_path, output_path, watermark_image_path, opacity=0.4):
    base_image = Image.open(image_path).convert("RGBA")
    watermark = Image.open(watermark_image_path).convert("RGBA")
    
    # scale the watermark to 5 pictures in a line - picture width
    target_width = base_image.width // 5
    aspect_ratio = watermark.width / watermark.height
    target_height = int(target_width / aspect_ratio)
    watermark = watermark.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # rotate the watermark by 45 and add transparency code. The opacy can be controled at the first line of the code. Now its 0.4
    watermark = watermark.rotate(45, expand=True)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    
    # creater the watermark as a tile
    watermark_tile = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
    
    # fill the image wit the watermark
    for x in range(0, base_image.size[0], watermark.width):
        for y in range(0, base_image.size[1], watermark.height):
            watermark_tile.paste(watermark, (x, y), watermark)
    
    # combine the original picture and watermark
    final_image = Image.alpha_composite(base_image, watermark_tile)
    
    # save the result
    final_image.convert("RGB").save(output_path, "JPEG")

