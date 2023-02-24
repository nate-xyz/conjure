from gi.repository import Adw, GLib, Gio, Gtk, GObject

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/crop.ui')
class CropCommand(Adw.Bin):
    __gtype_name__ = 'CropCommand'

    left_spin: Gtk.SpinButton = Gtk.Template.Child('left_spin')
    top_spin: Gtk.SpinButton = Gtk.Template.Child('top_spin')
    width_spin: Gtk.SpinButton = Gtk.Template.Child('width_spin')
    height_spin: Gtk.SpinButton = Gtk.Template.Child('height_spin')

    def __init__(self, job_callback, size) -> None:
        super().__init__()
        self.width, self.height = size
        
        self.left_crop, self.top_crop, self.width_crop, self.height_crop = 0, 0, self.width, self.height
        #new (value, lower, upper, step_increment, page_increment, page_size)
        self.left_adjustment = Gtk.Adjustment.new(0.0, 0.0, self.width, 1.0, 0, 0)
        self.left_spin.set_adjustment(self.left_adjustment)

        self.top_adjustment = Gtk.Adjustment.new(0.0, 0.0, self.height, 1.0, 0, 0)
        self.top_spin.set_adjustment(self.top_adjustment)

        self.width_adjustment = Gtk.Adjustment.new(self.width, 0.0, self.width, 1.0, 0, 0)
        self.width_spin.set_adjustment(self.width_adjustment)

        self.height_adjustment = Gtk.Adjustment.new(self.height, 0.0, self.height, 1.0, 0, 0)
        self.height_spin.set_adjustment(self.height_adjustment)

        self.left_spin.connect('value-changed', self.on_spin_change)
        self.top_spin.connect('value-changed', self.on_spin_change)
        self.width_spin.connect('value-changed', self.on_spin_change)
        self.height_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        match spin:
            case self.left_spin:
                self.left_crop = int(value)
            case self.top_spin:
                self.top_crop = int(value)
            case self.width_spin:
                self.width_crop = int(value)
            case self.height_spin:
                self.height_crop = int(value)
        
        if self.width_crop > 0 and self.height_crop > 0:
            self.start_job(self.left_crop, self.top_crop, self.width_crop, self.height_crop)
