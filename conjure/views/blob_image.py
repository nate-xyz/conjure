from gi.repository import Adw, Gtk, GdkPixbuf

from loguru import logger

class BlobImage(Adw.Bin):
    __gtype_name__ = 'BlobImage'

    def __init__(self, blob, size) -> None:
        super().__init__()
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.load_image(blob, size)

    def load_image(self, blob, size):
        try:
            width, height = size
            pixbuf = GdkPixbuf.Pixbuf.new_from_data(blob, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3)
            self.picture = Gtk.Picture.new_for_pixbuf(pixbuf)
            self.set_child(self.picture)
        except Exception as e:
            logger.error(e)
            return 
        

    