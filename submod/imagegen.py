def generate(tx, ty, points):
    out = ""
    for x in range(tx):
        for y in range(ty):
            loc = [x, y]
            if loc in points:
                out += f'<rect width="15" height="15" x="{(x * 20)}" y="{(y * 20)}" rx="3" ry="3" style="fill:green;" />'
            else:
                out += f'<rect width="15" height="15" x="{(x * 20)}" y="{(y * 20)}" rx="3" ry="3" style="fill:black;"/>'
    width = 10 * 20 
    height = 10 * 20
    svg_header = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="padding: 20px;">'
    return svg_header + out + "</svg>"

width = 10 * 20 
height = 10 * 20

svg_header = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="padding: 20px;">'
