def generate(tx, ty, points):
    out = ""
    for x in range(tx):
        for y in range(ty):
            loc = [x, y]
            if loc in points:
                out += f'<rect width="15" height="15" x="{(x * 20)}" y="{(y * 20)}" rx="3" ry="3" style="fill:lime;" />'
            else:
                out += f'<rect width="15" height="15" x="{(x * 20)}" y="{(y * 20)}" rx="3" ry="3" style="fill:black;"/>'
    width = tx * 20 - 5
    height = ty * 20 - 5
    svg_header = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    return svg_header + out + "</svg>"
