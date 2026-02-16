from PIL import Image
import sys

def to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def clamp(v):
    return max(0, min(255, int(v)))

def darker(rgb, factor=0.8):
    return tuple(clamp(c * factor) for c in rgb)

def lighter(rgb, factor=1.2):
    return tuple(clamp(c * factor) for c in rgb)

def main(path):
    img = Image.open(path).convert('RGBA')
    # Composite against white if alpha present
    if img.mode == 'RGBA':
        bg = Image.new('RGBA', img.size, (255,255,255,255))
        bg.paste(img, mask=img.split()[3])
        img = bg.convert('RGB')
    else:
        img = img.convert('RGB')

    # Resize to 1x1 to get average color
    avg = img.resize((1,1), resample=Image.BILINEAR).getpixel((0,0))
    dark = darker(avg, 0.78)
    light = lighter(avg, 1.12)

    print(to_hex(avg))
    print(to_hex(dark))
    print(to_hex(light))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python get_logo_colors.py path/to/logo.png')
        sys.exit(1)
    main(sys.argv[1])
