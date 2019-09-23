from typing import List, Dict, Union, Tuple


class SVGObject:
    def __init__(self, **kwargs):
        self.parameters = {}
        for k, v in kwargs.items():
            if isinstance(k, str) and (isinstance(v, int) or isinstance(v, float) or isinstance(v, str)):
                self.parameters[k.replace('_', '-')] = v

    def finalize(self):
        return ''

    def get_prefix(self):
        return ''

    def get_suffix(self):
        return ''


class SVGClosedObject(SVGObject):
    def __init__(self, **kwargs):
        super(SVGClosedObject, self).__init__(**kwargs)

    def finalize(self):
        return f'{self.get_prefix()}{self.get_suffix()}'

    def get_suffix(self):
        temp = " ".join([f'{k}="{v}"' for k, v in self.parameters.items()])
        return f'{temp} />'


class SVGOpenObject(SVGObject):
    svg_objects: List[SVGObject] = []

    def __init__(self, **kwargs):
        super(SVGOpenObject, self).__init__(**kwargs)

    def add(self, svg_object: SVGObject):
        self.svg_objects.append(svg_object)

    def rem(self, svg_index: int):
        if len(self.svg_objects) >= svg_index:
            del self.svg_objects[svg_index]

    def finalize(self):
        return f'{self.get_prefix()}{"".join([svg_object.finalize() for svg_object in self.svg_objects])}{self.get_suffix()}'


class SVGGraphic(SVGOpenObject):
    def get_prefix(self):
        return '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">'

    def get_suffix(self):
        return '</svg>'

    def save(self, file):
        temp = "".join([svg_object.finalize() for svg_object in self.svg_objects])
        file.write(f'{self.get_prefix()}{temp}{self.get_suffix()}')
        file.flush()


class SVGCircle(SVGClosedObject):
    def __init__(self, cx: float, cy: float, r: float, **kwargs):
        kwargs['cx'] = cx
        kwargs['cy'] = cy
        kwargs['r'] = r
        super(SVGCircle, self).__init__(**kwargs)

    def get_prefix(self):
        return '<circle '


class SVGRect(SVGClosedObject):
    def __init__(self, pos: Tuple[float, float], dim: Tuple[float, float], **kwargs):
        kwargs['x'], kwargs['y'] = pos
        kwargs['width'], kwargs['height'] = dim
        super(SVGRect, self).__init__(**kwargs)

    def get_prefix(self):
        return '<rect '


class SVGPolygon(SVGClosedObject):
    def __init__(self, points: List[Tuple[float, float]], **kwargs):
        kwargs['points'] = " ".join([f"{x},{y}" for x, y in points])
        super(SVGPolygon, self).__init__(**kwargs)

    def get_prefix(self):
        return '<polygon '


class SVGLine(SVGClosedObject):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], **kwargs):
        kwargs['x1'], kwargs['y1'] = start
        kwargs['x2'], kwargs['y2'] = end
        super(SVGLine, self).__init__(**kwargs)

    def get_prefix(self):
        return '<line '


if __name__ == '__main__':
    graphic = SVGGraphic()
    
    graphic.add(SVGCircle(
        50, 50, 5, 
        stroke='red', stroke_width=2, fill='white'))
    graphic.add(SVGRect(
        (5, 5), (40, 10), 
        stroke='red', stroke_width=2, fill='white'))
    graphic.add(SVGPolygon(
        [(5, 5), (4, 1), (9, 2)], 
        fill='red', stroke='black', stroke_width=2))
    graphic.add(SVGLine(
        (0, 0), (50, 50), 
        stroke='blue', stroke_width=2))

    with open('nope.svg', 'w') as f:
        graphic.save(f)