'''
Text Pango: Draw text with pango
'''
from kivy.core.image import ImageData

__all__ = ('LabelPango',)

from kivy.core.text import LabelBase, TextInputBase

try:
    import pango
    import cairo
    import pangocairo
except:
    raise

font_map = pangocairo.cairo_font_map_get_default()
families = font_map.list_families()

print [f.get_name() for f in families]

class LabelPango(LabelBase):
    def _get_font_id(self):
        return ' '.join(('Droid Sans', 'bold' if self.options['bold'] else '',
                         'italic' if self.options['italic'] else '', str(self.options['font_size'])))
    
    def _get_font(self):
        return pango.FontDescription(self._get_font_id())
    
    def get_extents(self, text):
        font = self._get_font()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 100, 100)
        context = cairo.Context(surface)
        pangocairo_context = pangocairo.CairoContext(context)
        pangocairo_context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        layout = pangocairo_context.create_layout()
        layout.set_font_description(font)
        layout.set_text(text)
        pangocairo_context.update_layout(layout)
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
    
    def _render_begin(self):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *self._size)
        self.context = cairo.Context(self.surface)
        self.pangocairo_context = pangocairo.CairoContext(self.context)
        self.pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)


    def _render_text(self, text, x, y):
        context = self.context
        # context.rectangle(0, 0, 320, 120)
        # context.set_source_rgb(1, 1, 1)
        # context.fill()
        pangocairo_context = self.pangocairo_context
        
        context.translate(x, y)
        # print 'translate:', x, y
        
        layout = pangocairo_context.create_layout()
        layout.set_font_description(self._get_font())
        
        # print 'text:', text
        layout.set_text(text)
        
        context.set_source_rgba(*self.options['color'])
        pangocairo_context.update_layout(layout)
        pangocairo_context.show_layout(layout)
        
        context.translate(-x, -y)
    
    def _render_end(self):
        w, h = self._size
        # print 'size:', w, h
        imdata = self.surface.get_data()
        # self.surface.write_to_png('text.png')
        # print 'imdata:', type(imdata), len(imdata)
        data = ImageData(w, h, 'rgba', imdata)
        
        del self.pangocairo_context
        del self.context
        del self.surface
        
        return data
    
    def get_cursor_pos(self, col):
        pass


class TextInputPango(TextInputBase):
    pass
