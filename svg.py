# Scalable Vector Graphics (SVG) is an XML-based vector image format.
# This file help to render image in svg format.

def hex_str(value: int) -> str:
    return '0' + hex(value)[2:] if value < 16 else hex(value)[2:]

def rgb2hex(rgb: tuple) -> str:
    return '#' + hex_str(rgb[0]) + hex_str(rgb[1]) + hex_str(rgb[2])

def to_svg(height, width, ps, cs, average_color, file_path) -> None:
    svg_content = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0.0 0.0 {} {}" \
    height="{}px" width="{}px">\n'.format(width, height, height, width)]
    path_template = '<path fill="{}" stroke-opacity="0" d="{}"></path>\n'
    svg_content.append(path_template.format(rgb2hex(average_color), "M0 0 L0 {} L{} {} L{} 0 Z".format(height, width, height, width)))
    for i in range(len(ps)):
        sps = ps[i]
        hex_color = rgb2hex((int(cs[i][0]), int(cs[i][1]), int(cs[i][2])))
        path = "M{} {}".format(sps[0][0], sps[0][1])
        for each_point in sps[1:]:
            path += " L{} {}".format(each_point[0], each_point[1])
        svg_content.append(path_template.format(hex_color, path))
    svg_content.append("</svg>")
    with open(file_path, 'w') as ww:
        ww.writelines(svg_content)

