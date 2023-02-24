from gi.repository import Adw, Gtk, Gio
import os
from wand.image import Image
from loguru import logger
from .blob_image import BlobImage

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/save_dialog.ui')
class SaveImageDialog(Adw.MessageDialog):
    __gtype_name__ = 'SaveImageDialog'

    image_bin = Gtk.Template.Child(name="image_bin")

    def __init__(self, image: Image, window, magic) -> None:
        super().__init__()
        logger.debug('init')

        self.image = image
        self.window = window
        self.magic = magic

        self.set_transient_for(self.window)
        self.set_image()
        self.add_dialog()

    def set_image(self):
        try:
            image_blob = self.image.make_blob(format='rgb')
            size = self.image.size
            self.image_bin.set_child(BlobImage(image_blob, size))

        except Exception as e:
            logger.error(e)


    def add_dialog(self):
        try:
            self.save_dialog = Gtk.FileChooserNative.new(title=_("Save Image"), 
                                                            action=Gtk.FileChooserAction.SAVE, 
                                                            parent=self.window, 
                                                            accept_label=_("Save"))

            #folder = Gio.File.new_for_path(self.magic.folder)

            #self.save_dialog.set_current_folder(folder)

            name, ext = os.path.splitext(self.magic.file_name)

            self.save_dialog.set_current_name(f"{name}_transformed{ext}")
            self.save_dialog.connect("response", self.save_response)
        except Exception as e:
            logger.error(e)

    @Gtk.Template.Callback()
    def dialog_response(self, _dialog, response):
        logger.debug(response)
        logger.debug(response)
        if response == 'save':
            self.save_dialog.show()

    def save_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            try:
                new_uri = dialog.get_file().get_path()
                logger.debug(f"saving file to {new_uri}")
                if self.magic.save(new_uri):
                    self.window.add_success_toast(_("Saved!"), _(f"New image: {dialog.get_current_name()}"))
                else:
                    self.window.add_error_toast(_(f"Unable to save image {dialog.get_current_name()}."))
            except Exception as e:
                logger.error(e)
                self.window.add_error_toast(_(f"Unable to save image."))
            
