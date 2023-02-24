from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/low_high.ui')
class LowHigh(Adw.Bin):
    __gtype_name__ = 'LowHigh'

    low_spin: Gtk.SpinButton = Gtk.Template.Child('low_spin')
    high_spin: Gtk.SpinButton = Gtk.Template.Child('high_spin')

    def __init__(self, job_callback) -> None:
        super().__init__()
        
        self.low = float(self.low_spin.get_value())
        self.high = float(self.high_spin.get_value())

        self.low_spin.connect('value-changed', self.on_spin_change)
        self.high_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.low, self.high)

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        match spin:
            case self.low_spin:
                self.low = float(value)
            case self.high_spin:
                self.high = float(value)
    
        self.start_job(self.low, self.high)

