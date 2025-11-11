#!/usr/bin/env python3
"""
Generate 30 beautiful placeholder images for the random image loader.
"""

from PIL import Image, ImageDraw, ImageFont
import colorsys
import os

def generate_image(number, total=30):
    """Generate a beautiful placeholder image with gradient and number."""
    width, height = 800, 600
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Generate a color based on the number (hue varies across the spectrum)
    hue = (number / total) % 1.0
    saturation = 0.7
    lightness = 0.9
    
    # Convert HSL to RGB for gradient start
    r1, g1, b1 = colorsys.hls_to_rgb(hue, lightness, saturation)
    r1, g1, b1 = int(r1 * 255), int(g1 * 255), int(b1 * 255)
    
    # Darker shade for gradient end
    r2, g2, b2 = colorsys.hls_to_rgb(hue, lightness - 0.2, saturation)
    r2, g2, b2 = int(r2 * 255), int(g2 * 255), int(b2 * 255)
    
    # Draw gradient
    for y in range(height):
        ratio = y / height
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add decorative circles
    circle_size = 150
    for i in range(3):
        x = width // 4 + (i * width // 4)
        y = height // 2
        size = circle_size - (i * 20)
        alpha = 0.3
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.ellipse(
            [x - size//2, y - size//2, x + size//2, y + size//2],
            fill=(255, 255, 255, int(255 * alpha))
        )
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Add number text
    try:
        # Try to use a nice font, fallback to default if not available
        font_size = 120
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
            except:
                font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    text = str(number)
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Draw text with shadow effect
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    # Shadow
    draw.text((text_x + 3, text_y + 3), text, font=font, fill=(0, 0, 0, 100))
    # Main text
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))
    
    return img

def main():
    """Generate 30 images."""
    print("Generating 30 images...")
    
    for i in range(1, 31):
        img = generate_image(i, 30)
        filename = f"{i}.jpg"
        img.save(filename, "JPEG", quality=90)
        print(f"Generated {filename}")
    
    print("\nDone! Generated 30 images (1.jpg through 30.jpg)")

if __name__ == "__main__":
    main()

