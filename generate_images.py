#!/usr/bin/env python3
"""
Generate 30 complex beautiful images for the random image loader.
"""

from PIL import Image, ImageDraw, ImageFont
import colorsys
import math
import random

def generate_image(number, total=30):
    """Generate a complex beautiful image with multiple elements."""
    width, height = 800, 600
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Generate a color scheme based on the number
    base_hue = (number / total) % 1.0
    saturation = 0.7 + (number % 3) * 0.1  # Vary saturation
    lightness = 0.85 + (number % 2) * 0.1   # Vary lightness
    
    # Primary color (for gradient start)
    r1, g1, b1 = colorsys.hls_to_rgb(base_hue, lightness, saturation)
    r1, g1, b1 = int(r1 * 255), int(g1 * 255), int(b1 * 255)
    
    # Secondary color (complementary, for gradient end)
    comp_hue = (base_hue + 0.5) % 1.0
    r2, g2, b2 = colorsys.hls_to_rgb(comp_hue, lightness - 0.15, saturation * 0.8)
    r2, g2, b2 = int(r2 * 255), int(g2 * 255), int(b2 * 255)
    
    # Draw diagonal gradient
    for y in range(height):
        for x in range(width):
            # Diagonal gradient
            ratio = (x + y) / (width + height)
            r = int(r1 * (1 - ratio) + r2 * ratio)
            g = int(g1 * (1 - ratio) + g2 * ratio)
            b = int(b1 * (1 - ratio) + b2 * ratio)
            draw.point((x, y), fill=(r, g, b))
    
    # Add geometric shapes - circles
    num_circles = 5 + (number % 4)
    for i in range(num_circles):
        circle_x = random.randint(0, width)
        circle_y = random.randint(0, height)
        circle_size = random.randint(80, 200)
        
        # Create overlay for circle
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Vary circle colors
        circle_hue = (base_hue + i * 0.1) % 1.0
        cr, cg, cb = colorsys.hls_to_rgb(circle_hue, 0.6, 0.5)
        cr, cg, cb = int(cr * 255), int(cg * 255), int(cb * 255)
        alpha = 80 + (i % 3) * 40
        
        overlay_draw.ellipse(
            [circle_x - circle_size//2, circle_y - circle_size//2,
             circle_x + circle_size//2, circle_y + circle_size//2],
            fill=(cr, cg, cb, alpha)
        )
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Add geometric shapes - polygons (triangles)
    num_triangles = 3 + (number % 3)
    for i in range(num_triangles):
        # Random triangle points
        points = [
            (random.randint(0, width), random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height))
        ]
        
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        tri_hue = (base_hue + i * 0.15) % 1.0
        tr, tg, tb = colorsys.hls_to_rgb(tri_hue, 0.7, 0.6)
        tr, tg, tb = int(tr * 255), int(tg * 255), int(tb * 255)
        alpha = 100 + (i % 2) * 60
        
        overlay_draw.polygon(points, fill=(tr, tg, tb, alpha))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Add decorative lines/curves
    num_lines = 4 + (number % 3)
    for i in range(num_lines):
        start_x = random.randint(0, width)
        start_y = random.randint(0, height)
        end_x = random.randint(0, width)
        end_y = random.randint(0, height)
        
        line_hue = (base_hue + i * 0.2) % 1.0
        lr, lg, lb = colorsys.hls_to_rgb(line_hue, 0.5, 0.8)
        lr, lg, lb = int(lr * 255), int(lg * 255), int(lb * 255)
        
        # Draw curved line
        for t in range(0, 100):
            t_ratio = t / 100.0
            # Bezier-like curve
            x = int(start_x + (end_x - start_x) * t_ratio + 
                   math.sin(t_ratio * math.pi * 2) * 30)
            y = int(start_y + (end_y - start_y) * t_ratio + 
                   math.cos(t_ratio * math.pi * 2) * 30)
            if 0 <= x < width and 0 <= y < height:
                draw.ellipse([x-2, y-2, x+2, y+2], fill=(lr, lg, lb))
    
    # Add pattern overlay (grid or dots)
    pattern_type = number % 3
    if pattern_type == 0:  # Dots pattern
        dot_spacing = 40
        dot_size = 3
        for x in range(0, width, dot_spacing):
            for y in range(0, height, dot_spacing):
                if (x + y) % (dot_spacing * 2) == 0:
                    dot_r, dot_g, dot_b = colorsys.hls_to_rgb(base_hue, 0.9, 0.3)
                    dot_r, dot_g, dot_b = int(dot_r * 255), int(dot_g * 255), int(dot_b * 255)
                    draw.ellipse([x-dot_size, y-dot_size, x+dot_size, y+dot_size], 
                               fill=(dot_r, dot_g, dot_b))
    elif pattern_type == 1:  # Grid pattern
        grid_spacing = 50
        grid_r, grid_g, grid_b = colorsys.hls_to_rgb(base_hue, 0.8, 0.4)
        grid_r, grid_g, grid_b = int(grid_r * 255), int(grid_g * 255), int(grid_b * 255)
        for x in range(0, width, grid_spacing):
            draw.line([(x, 0), (x, height)], fill=(grid_r, grid_g, grid_b), width=1)
        for y in range(0, height, grid_spacing):
            draw.line([(0, y), (width, y)], fill=(grid_r, grid_g, grid_b), width=1)
    
    # Add number text with enhanced styling
    try:
        font_size = 140
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
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    # Draw text with multiple shadow layers for depth
    shadow_offset = 5
    for offset in range(shadow_offset, 0, -1):
        alpha = 50 // offset
        draw.text((text_x + offset, text_y + offset), text, font=font, 
                 fill=(0, 0, 0, alpha))
    
    # Main text with gradient effect (simulated with multiple colors)
    text_hue = (base_hue + 0.3) % 1.0
    tr, tg, tb = colorsys.hls_to_rgb(text_hue, 0.95, 0.9)
    tr, tg, tb = int(tr * 255), int(tg * 255), int(tb * 255)
    draw.text((text_x, text_y), text, font=font, fill=(tr, tg, tb))
    
    # Add border/frame effect
    border_width = 8
    border_r, border_g, border_b = colorsys.hls_to_rgb(base_hue, 0.3, 0.6)
    border_r, border_g, border_b = int(border_r * 255), int(border_g * 255), int(border_b * 255)
    draw.rectangle([0, 0, width-1, height-1], outline=(border_r, border_g, border_b), width=border_width)
    
    return img

def main():
    """Generate 30 images."""
    print("Generating 30 complex images...")
    
    # Set random seed for reproducibility per image number
    for i in range(1, 31):
        random.seed(i * 42)  # Consistent randomness per image
        img = generate_image(i, 30)
        filename = f"{i}.jpg"
        img.save(filename, "JPEG", quality=95)
        print(f"Generated {filename}")
    
    print("\nDone! Generated 30 complex images (1.jpg through 30.jpg)")

if __name__ == "__main__":
    main()
