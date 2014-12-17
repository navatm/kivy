'''
Text Pango: Draw text with pango
'''
from math import ceil
import string
from kivy import Logger
from kivy.core.image import ImageData

__all__ = ('LabelPango',)

try:
    # import pango
    # import cairo
    # import pangocairo
    from gi.repository import Pango
    from gi.repository import PangoFT2
    from gi.repository import freetype2
except:
    raise

from kivy.core.text import LabelBase, TextInputBase
from kivy.core.text.text_layout import LayoutWord, LayoutLine

# font_map = pangocairo.cairo_font_map_get_default()
# families = font_map.list_families()

class LabelPango(LabelBase):
    
    def __init__(self, **kwargs):
        super(LabelPango, self).__init__(**kwargs)
        # temp_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
        # font_options = cairo.FontOptions()
        # font_options.set_antialias(cairo.ANTIALIAS_NONE)
        # font_options.set_hint_style(cairo.HINT_STYLE_FULL)
        # font_options.set_hint_metrics(cairo.HINT_METRICS_ON)
        self.fontmap = PangoFT2.FontMap.new()
        self.context = self.fontmap.create_context()
        # self.context = cairo.Context(temp_surface)
        # self.context.set_antialias(cairo.ANTIALIAS_NONE)
        # self.context.set_font_options(font_options)
        # self.pangocairo_context = pangocairo.CairoContext(self.context)
        # self.pangocairo_context.set_antialias(cairo.ANTIALIAS_NONE)
        # self.pangocairo_context.set_font_options(font_options)
        # del temp_surface

    def _get_font_id(self, options=None, debug=False):
        opt = options or self.options
        retu = ' '.join((opt['font_name'], 'bold' if opt['bold'] else '',
                         'italic' if opt['italic'] else '', str(opt['font_size']) + 'px'))
        if debug:
            print retu
        return retu
    
    def _get_font(self, options=None, debug=False):
        return Pango.FontDescription(self._get_font_id(options, debug))
    
    def get_extents(self, text):
        font = self._get_font()
        # surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 100, 100)
        # context = cairo.Context(surface)
        context = self.context
        # pangocairo_context = pangocairo.CairoContext(context)
        # pangocairo_context = self.pangocairo_context
        # pangocairo_context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        # layout = pangocairo_context.create_layout()
        layout = Pango.Layout(context)
        layout.set_font_description(font)
        layout.set_text(text)
        # pangocairo_context.update_layout(layout)
        extents = layout.get_pixel_extents()
        logical = extents[1]
        size = logical[2] - logical[0], logical[3] - logical[1]
        # print 'get_extents:', text, extents, size
        # ext = pangocairo_context.text_extents(text)
        # size = ext[2] + ext[4], ext[3] + ext[5]
        # print 'get_extents:', text, ext, size
        return size
    
    # def get_cached_extents(self):
    # 	pass

    def _render_real(self):
        lines = self._cached_lines
        if not lines:
            self._render_begin()
        else:
            self._render_lines(lines, self.options)

        data = self._render_end()
        assert data

        if data is not None and data.width > 1:
            self.texture.blit_data(data)
    
    def _render_begin(self):
        # self.render_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *self._size)
        # font_options = cairo.FontOptions()
        # font_options.set_antialias(cairo.ANTIALIAS_NONE)
        # font_options.set_hint_style(cairo.HINT_STYLE_FULL)
        # font_options.set_hint_metrics(cairo.HINT_METRICS_ON)
        # self.render_context = cairo.Context(self.render_surface)
        # self.render_context.set_antialias(cairo.ANTIALIAS_NONE)
        # self.render_context.set_font_options(font_options)
        # self.render_pangocairo_context = pangocairo.CairoContext(self.render_context)
        # self.render_pangocairo_context.set_antialias(cairo.ANTIALIAS_NONE)
        # self.render_pangocairo_context.set_font_options(font_options)
        pass

    def _render_lines(self, lines, options):
        self._render_begin()
        # context = self.render_context
        # pangocairo_context = self.render_pangocairo_context
        # twidth, theight = self._size
        
        line = lines[0]
        layout, lineoptions = line.words
        
        # context.translate(line.x, line.y)
        # print 'color:', lineoptions['color']
        # context.set_source_rgba(*lineoptions['color'])
        # pangocairo_context.update_layout(layout)
        # pangocairo_context.show_layout(layout)
        # context.translate(-line.x, -line.y)
        
        extent_ink, extent_logical = layout.get_pixel_extents()
        bitmap = freetype2.Bitmap
        
        
        # for layout, lineoptions, clip in lines:
        # 	y = 0
        # 	valign = lineoptions['valign'][0]
        # 	width, height = [s / pango.SCALE for s in layout.get_size()]
        # 	
        # 	if valign == 'm':
        # 		y = theight / 2 - height / 2 - clip / 2
        # 	elif valign == 'b':
        # 		y = theight - height - clip
        # 	
        # 	context.translate(0, y)
        # 	context.set_source_rgba(*lineoptions['color'])
        # 	pangocairo_context.update_layout(layout)
        # 	pangocairo_context.show_layout(layout)
        # 	context.translate(0, -y)

    # def _render_text(self, text, x, y):
    # 	context = self.render_context
    # 	# context.rectangle(0, 0, 320, 120)
    # 	# context.set_source_rgb(1, 1, 1)
    # 	# context.fill()
    # 	pangocairo_context = self.render_pangocairo_context
    # 	
    # 	context.translate(x, y)
    # 	# print 'translate:', x, y
    # 	
    # 	layout = pangocairo_context.create_layout()
    # 	layout.set_font_description(self._get_font())
    # 	
    # 	# print 'text:', text
    # 	layout.set_text(text)
    # 	
    # 	context.set_source_rgba(*self.options['color'])
    # 	pangocairo_context.update_layout(layout)
    # 	pangocairo_context.show_layout(layout)
    # 	
    # 	context.translate(-x, -y)
    
    def _render_end(self):
        w, h = self._size
        # print 'size:', w, h
        imdata = self.render_surface.get_data()
        # self.surface.write_to_png('text.png')
        # print 'imdata:', type(imdata), len(imdata)
        data = ImageData(w, h, 'rgba', imdata)
        
        del self.render_pangocairo_context
        del self.render_context
        del self.render_surface
        
        return data
    
    def get_cursor_pos(self, col):
        pass
    
    def layout_text_aligned(self, lines, options, text, uh, uw):
        w, h, clipped = self.layout_text(text, lines, (0, 0), (uw, uh),
                                         options, self.get_cached_extents(),
                                         True, True)
        return w, h
    
    def layout_text(self, text, lines, size, text_size, options, get_extents,
                    append_down, complete):
        xpad, ypad = options['padding_x'], options['padding_y']
        max_lines = int(options.get('max_lines', 0))
        font_size = options['font_size']
        line_height = options['line_height']
        halign = options['halign'][0]
        valign = options['valign'][0]
        strip = options['strip'] or halign == 'j'

        tlines = text.split('\n')
        if max_lines:
            tlines = tlines[:max_lines]
            complete = True
        
        if strip:
            if complete:
                tlines = [l.strip(string.whitespace) for l in tlines]
            else:
                tlines = [l.strip(string.whitespace) for l in tlines[:-1]] + tlines[-1:]

        text = '\n'.join(tlines)
        # font_options = cairo.FontOptions()
        # font_options.set_antialias(cairo.ANTIALIAS_NONE)
        # font_options.set_hint_style(cairo.HINT_STYLE_FULL)
        # font_options.set_hint_metrics(cairo.HINT_METRICS_ON)
        # self.context.set_font_options(font_options)
        # self.pangocairo_context.set_font_options(font_options)
        layout = self.pangocairo_context.create_layout()
        # line = [layout, options, 0]
        line = LayoutLine(xpad, ypad, words=[layout, options])
        lines.append(line)
        assert isinstance(layout, pango.Layout)

        text_width, text_height = text_size
        if text_width is not None:
            scaled_width = text_width * pango.SCALE
            # print text_width, pango.SCALE, scaled_width
            layout.set_width(int(ceil(scaled_width)))
        # if text_height is not None:
        # 	scaled_height = text_height * pango.SCALE
        # print text_height, pango.SCALE, scaled_height
        # layout.set_height(int(ceil(scaled_height)))

        # new_lines = text.split('\n')
        # n = len(new_lines)

        layout.set_font_description(self._get_font(options, True))
        layout.set_spacing(int(ceil((line_height - font_size) / 2 * pango.SCALE)))
        if halign == 'j':
            layout.set_justify(True)
        elif halign == 'l':
            layout.set_alignment(pango.ALIGN_LEFT)
        elif halign == 'r':
            layout.set_alignment(pango.ALIGN_RIGHT)
        else:
            layout.set_alignment(pango.ALIGN_CENTER)
        layout.set_text(text)

        # _l, _t, width, height = layout.get_pixel_extents()[0]
        width, height = [n / pango.SCALE for n in layout.get_size()]
        width += xpad * 2
        height += ypad * 2
        real_height = height if text_height is None else min(text_height, height)

        if text_height is not None:
            if valign == 'm':
                line.y = text_height / 2 - height / 2
            elif valign == 'b':
                line.y = text_height - height

        # exwidth, exheight = get_extents(text)
        # print text, width, height, height < exheight, text_size
        # line[2] = max(0, height - real_height)
        # if real_height < height:
        # 	print line[2]
        return width, real_height, real_height < height


class TextInputPango(TextInputBase):
    pass
