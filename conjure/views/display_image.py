from gi.repository import Adw, GLib, Gio, Gtk, Gdk

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/display_image.ui')
class DisplayImage(Adw.Bin):
    __gtype_name__ = 'DisplayImage'

    image_bin = Gtk.Template.Child(name="image_bin")
    new_image_bin = Gtk.Template.Child(name="new_image_bin")
    spinner = Gtk.Template.Child(name="spinner")
    overlay = Gtk.Template.Child(name="overlay")
    overlay_box = Gtk.Template.Child(name="overlay_box")

    def __init__(self) -> None:
        super().__init__()
        
    def set_main(self, image_widget):        
        self.new_image_bin.hide()
        self.stop_job()
        self.image_bin.set_child(image_widget)

    def set_transformed(self, image_widget):
        if image_widget:
            self.new_image_bin.show()
        else:
            self.new_image_bin.hide()
        self.new_image_bin.set_child(image_widget)
        self.stop_job()

    def start_job(self):
        self.overlay_box.show()
        self.spinner.show()
        self.spinner.start()

    def stop_job(self):
        self.overlay_box.hide()
        self.spinner.stop()
        self.spinner.hide()