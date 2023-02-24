from gi.repository import Adw, GLib, Gio, Gtk, Gdk

from os import path
from loguru import logger
from wand.display import display
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from conjure.window import Window
    from conjure.magic import Magic

from .dropped_image import DroppedImage
from .blob_image import BlobImage
from .command_panel import CommandPanel
from .display_image import DisplayImage
from .history_panel import HistoryPanel
from .save_dialog import SaveImageDialog


mimes = ['text/uri-list']

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/image_drop_page.ui')
class ImageDropPage(Adw.Bin):
    __gtype_name__ = 'ImageDropPage'

    overlay = Gtk.Template.Child(name="overlay")
    status = Gtk.Template.Child(name="status")
    open_image_button = Gtk.Template.Child(name="open_image_button")
    command_revealer = Gtk.Template.Child(name="command_revealer")
    command_panel = Gtk.Template.Child(name="command_panel")

    display_image = Gtk.Template.Child(name="display_image")

    save_toolbar = Gtk.Template.Child(name="save_toolbar")
    apply_button = Gtk.Template.Child(name="apply_button")
    save_button = Gtk.Template.Child(name="save_button")

    history_revealer = Gtk.Template.Child(name="history_revealer")
    history_panel = Gtk.Template.Child(name="history_panel")

    def __init__(self) -> None:
        super().__init__()
        self.window: Optional[Window] = None
        self.magic: Optional[Magic] = None
        self.setup_drop_target()
        self.file_verified = False

        self.apply_button.connect('clicked', lambda _button: self.on_apply())
        self.save_button.connect('clicked', lambda _button: self.on_save())
        self.history_panel.connect('clicked', lambda _panel, position: self.restore_from_history(position))


    def restore_from_history(self, position):
        if self.magic.update_main_image_from_index(position):
            self.reset_main_image_ui()
        else:
            self.window.add_error_toast(_("Could not restore from history."))

    def on_apply(self):
        if self.magic.current_image:
            self.magic.update_main_image_from_most_recent()
            #self.history_panel.add_child(self.magic.current_image)
            
            self.reset_main_image_ui()
        else:
            self.window.add_error_toast(_("No transformation to apply."))

    def on_save(self):
        dialog = SaveImageDialog(self.magic.current_image, self.window, self.magic)
        dialog.show() 

    def reset_main_image_ui(self):
        try:
            image_blob = self.magic.current_image.make_blob(format='rgb')
            size = self.magic.current_image.size
            self.load_image_ui(BlobImage(image_blob, size))
            self.save_toolbar.show()
        except Exception as e:
            self.save_toolbar.hide()
            logger.error(e)
            self.window.add_error_toast(_("Unable to load converted image."))

    def saturate(self, window, magic):
        self.command_panel.saturate(window, magic)
        self.history_panel.saturate(window, magic)
        self.window = window 
        self.magic = magic
        
    def setup_drop_target(self):
        formats = Gdk.ContentFormats.new(mimes)
        drop_target = Gtk.DropTargetAsync.new(formats=formats, actions=Gdk.DragAction.COPY)
        drop_target.connect('accept', self.on_drag_accept)
        drop_target.connect('drop', self.on_drag_drop)
        
        self.overlay.add_controller(drop_target)

    def on_drag_accept(self, drop_target, drop_value):
        self.file_verified = False
        formats = drop_value.get_formats()
        if contain_mime_types(formats):
            drop_value.read_value_async(Gio.File, GLib.PRIORITY_DEFAULT, None, self.verify_file_valid)
            return True
        return False

    def verify_file_valid(self, drop, task):
        result = drop.read_value_finish(task)
        if not result:
            return
        self.file_verified = path.exists(result.get_path())

    def on_drag_drop(self, drop_target, drop_value, *args):
        if not drop_value:
            self.window.add_error_toast(_("Unable to read drop."))
            drop_value.finish(0)
            return False
    
        if not self.file_verified:
            self.window.add_error_toast(_("Unable to verify file on drop, try with the file chooser in the upper left corner."), 4)
            drop_value.finish(0)
            return False

        drop_value.read_value_async(Gio.File, GLib.PRIORITY_DEFAULT, None, self.load_value_async)
        return True
        
    def load_value_async(self, drop, task):
        result = drop.read_value_finish(task)
        if not result:
            self.window.add_error_toast(_("Unable to read drop."))
            drop.finish(0)
            return
        
        uri = result.get_path()
        if self.load_image(uri):
            drop.finish(Gdk.DragAction.COPY)
            self.window.open_image_toast(uri)
        else:
            self.window.error_image_toast(uri)
            drop.finish(0)

    def load_image(self, uri):
        try:
            if self.magic.open(uri):
                self.load_image_ui(DroppedImage(uri))
                self.command_panel.reload()
                return True            
        except Exception as e:
            logger.error(e)
            self.load_image_ui(None)
        return False

    def load_image_ui(self, image):
        visible = image != None
        self.status.set_visible(not visible)
        self.command_revealer.set_reveal_child(visible)
        #self.info_revealer.set_reveal_child(visible)
        self.display_image.set_main(image)
        self.display_image.new_image_bin.set_child(None)
        self.history_panel.set_visible(visible and self.magic.visible_history())
        self.history_revealer.set_reveal_child(visible and self.magic.visible_history())
        self.history_panel.update_view()
            
    def load_transformed(self, image_blob, size):
        try:
            self.display_image.set_transformed(BlobImage(image_blob, size))
            self.save_toolbar.show()
        except Exception as e:
            self.save_toolbar.hide()
            logger.error(e)
            self.window.add_error_toast(_("Unable to load converted image."))
    


def contain_mime_types(formats):
    if formats is not None:
        return True in (formats.contain_mime_type(m) for m in mimes)
    return False