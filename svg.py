"""
Scalable Vector Graphics (SVG) is an XML-based vector image format.
This file help to render image in svg format.
"""

__all__ = ["to_svg"]

def hex_str(value: int) -> str:
    """convert hex value to string"""
    return '0' + hex(value)[2:] if value < 16 else hex(value)[2:]

def rgb2hex(rgb: tuple) -> str:
    """convert rgb color to hex color"""
    return '#' + hex_str(rgb[0]) + hex_str(rgb[1]) + hex_str(rgb[2])

def to_svg(size, points, colors, average_color, file_path) -> None:
    """generate svg path given polygon contour"""
    height, width = size[0], size[1]
    svg_content = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0.0 0.0 {w} {h}" \
    height="{h}px" width="{w}px">\n'.format(w = width, h = height)]
    path_template = '<path fill="{}" stroke-opacity="0" d="{}"></path>\n'
    svg_content.append(path_template.format(rgb2hex(average_color), \
        f"M0 0 L0 {height} L{width} {height} L{width} 0 Z"))
    for i, sps in enumerate(points):
        hex_color = rgb2hex((int(colors[i][0]), int(colors[i][1]), int(colors[i][2])))
        path = f"M{sps[0][0]} {sps[0][1]}"
        for each_point in sps[1:]:
            path += f" L{each_point[0]} {each_point[1]}"
        svg_content.append(path_template.format(hex_color, path))
    svg_content.append("</svg>")
    with open(file_path, 'w', encoding='UTF-8') as write_handle:
        write_handle.writelines(svg_content)
