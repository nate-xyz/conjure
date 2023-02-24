from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/width_height_offset.ui')
class WidthHeightOffset(Adw.Bin):
    __gtype_name__ = 'WidthHeightOffset'

    width_spin: Gtk.SpinButton = Gtk.Template.Child('width_spin')
    height_spin: Gtk.SpinButton = Gtk.Template.Child('height_spin')
    offset_spin: Gtk.SpinButton = Gtk.Template.Child('offset_spin')

    def __init__(self, job_callback) -> None:
        super().__init__()
        
        self.width = int(self.width_spin.get_value())
        self.height = int(self.height_spin.get_value())
        self.offset = self.offset_spin.get_value()

        self.width_spin.connect('value-changed', self.on_spin_change)
        self.height_spin.connect('value-changed', self.on_spin_change)
        self.offset_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.width, self.height, self.offset)

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        match spin:
            case self.width_spin:
                self.width = int(value)
            case self.height_spin:
                self.height = int(value)
            case self.offset_spin:
                self.offset = float(value)
        

        self.start_job(self.width, self.height, self.offset)

