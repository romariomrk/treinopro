# Generate simple SVG icons and convert to PNG using Python
import struct, zlib, base64

def create_png(size, bg_color, accent_color):
    """Create a simple PNG icon"""
    import struct, zlib
    
    def make_png(width, height, pixels):
        def chunk(name, data):
            c = struct.pack('>I', len(data)) + name + data
            return c + struct.pack('>I', zlib.crc32(c[4:]) & 0xffffffff)
        
        ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
        raw = b''
        for row in pixels:
            raw += b'\x00'
            for r, g, b in row:
                raw += bytes([r, g, b])
        
        idat = zlib.compress(raw)
        return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')
    
    # Create simple icon with background and "T" letter
    pixels = []
    for y in range(size):
        row = []
        for x in range(size):
            # Rounded background
            cx, cy = size//2, size//2
            r = size//2 - 2
            dist = ((x-cx)**2 + (y-cy)**2)**0.5
            if dist <= r:
                # Draw "T" shape in center
                center_x = size // 2
                bar_y = size // 3
                stem_x1 = center_x - size//12
                stem_x2 = center_x + size//12
                bar_x1 = center_x - size//4
                bar_x2 = center_x + size//4
                bar_h = size // 8
                
                in_bar = (bar_x1 <= x <= bar_x2 and bar_y <= y <= bar_y + bar_h)
                in_stem = (stem_x1 <= x <= stem_x2 and bar_y <= y <= size*2//3)
                
                if in_bar or in_stem:
                    row.append((220, 180, 255))  # light purple
                else:
                    row.append(bg_color)
            else:
                row.append((13, 13, 15))  # transparent-ish bg
        pixels.append(row)
    
    return make_png(size, size, pixels)

# Generate icons
for size, name in [(192, 'icon-192.png'), (512, 'icon-512.png')]:
    png_data = create_png(size, (30, 27, 46), (124, 58, 237))
    with open(f'/home/claude/treinopro/{name}', 'wb') as f:
        f.write(png_data)
    print(f'{name} criado ({size}x{size})')

