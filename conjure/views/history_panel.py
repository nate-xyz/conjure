from gi.repository import Adw, Gio, Gtk, GObject, GdkPixbuf

from loguru import logger

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from conjure.window import Window
    from conjure.magic import Magic

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/history_panel.ui')
class HistoryPanel(Adw.Bin):
    __gtype_name__ = 'HistoryPanel'


    __gsignals__ = {
        'clicked': (GObject.SignalFlags.RUN_FIRST, None, (int, )),
    }

    flow_box = Gtk.Template.Child('flow_box')
    scrolled_window = Gtk.Template.Child('scrolled_window')

    def __init__(self) -> None:
        super().__init__()
        self.window: Optional[Window] = None
        self.magic: Optional[Magic] = None

        self.list_store = Gio.ListStore(item_type=ImageType)
        self.flow_box.bind_model(self.list_store, self.flowbox_factory)

        self.children = []

    def saturate(self, window, magic):
        self.window = window 
        self.magic = magic

    def update_view(self):
        self.list_store.remove_all()
        for i, img in enumerate(self.magic.image_history):
            self.list_store.append(ImageType(img, i))

        self.flow_box.set_min_children_per_line(len(self.list_store))
        self.flow_box.set_max_children_per_line(len(self.list_store))

    def flowbox_factory(self, image_type):
        card = ImageCard(image_type)
        card.button.connect('clicked', lambda _button: self.emit('clicked', card.position))
        return card

class ImageType(GObject.GObject):
    __gtype_name__ = 'ImageType'

    def __init__(self, image, position: int) -> None:
        super().__init__()
        self.image, self.msg = image
        self.position = position

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/image_card.ui')
class ImageCard(Gtk.FlowBoxChild):
    __gtype_name__ = 'ImageCard'

    button = Gtk.Template.Child('button')
    color_bin = Gtk.Template.Child('color_bin')


    def __init__(self, image_type: ImageType) -> None:
        super().__init__()
        self.image = image_type.image
        self.position = image_type.position
        self.button.set_tooltip_text(image_type.msg)
        ctrl = Gtk.EventControllerMotion()
        ctrl.connect("enter", lambda _controller, _x, _y: self.button.show())
        ctrl.connect("leave", lambda _controller: self.button.hide())
        self.add_controller(ctrl)

        self.load_image()

    def load_image(self):
        self.color_bin.set_child(BlobImageScale(self.image.make_blob(format='rgb'), self.image.size))

class BlobImageScale(Adw.Bin):
    __gtype_name__ = 'BlobImageScale'

    def __init__(self, blob, size) -> None:
        super().__init__()
        self.size = 110
        self.set_halign(Gtk.Align.FILL)
        self.set_valign(Gtk.Align.FILL)
        self.load_image(blob, size)

    def load_image(self, blob, size):
        try:
            width, height = size
            pixbuf = GdkPixbuf.Pixbuf.new_from_data(blob, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3)   

            if width > height:
                height = (self.size / width) * height 
                width = self.size 
            else:
                width = (self.size / height) * width 
                height = self.size       

            scaled_pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)

            self.picture = Gtk.Picture.new_for_pixbuf(scaled_pixbuf)
            self.set_child(self.picture)
        except Exception as e:
            logger.error(e)
            return 
        





    
