from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/low_high_white_black.ui')
class LowHighWhiteBlack(Adw.Bin):
    __gtype_name__ = 'LowHighWhiteBlack'

    low_black_spin: Gtk.SpinButton = Gtk.Template.Child('low_black_spin')
    low_white_spin: Gtk.SpinButton = Gtk.Template.Child('low_white_spin')
    high_white_spin: Gtk.SpinButton = Gtk.Template.Child('high_white_spin')
    high_black_spin: Gtk.SpinButton = Gtk.Template.Child('high_black_spin')

    def __init__(self, job_callback) -> None:
        super().__init__()
        
        self.low_black = float(self.low_black_spin.get_value())
        self.low_white = float(self.low_white_spin.get_value())
        self.high_white = float(self.high_white_spin.get_value())
        self.high_black = float(self.high_black_spin.get_value())

        self.low_black_spin.connect('value-changed', self.on_spin_change)
        self.low_white_spin.connect('value-changed', self.on_spin_change)
        self.high_white_spin.connect('value-changed', self.on_spin_change)
        self.high_black_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.low_black, self.low_white, self.high_white, self.high_black)

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        match spin:
            case self.low_black_spin:
                self.low_black = float(value)
            case self.low_white_spin:
                self.low_white = float(value)
            case self.high_white_spin:
                self.high_white = float(value)
            case self.high_black_spin:
                self.high_black = float(value)

        self.start_job(self.low_black, self.low_white, self.high_white, self.high_black)


