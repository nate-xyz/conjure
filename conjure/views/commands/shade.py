from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/shade.ui')
class Shade(Adw.Bin):
    __gtype_name__ = 'Shade'

    gray_check = Gtk.Template.Child('gray_check')
    azimuth_spin = Gtk.Template.Child('azimuth_spin')  
    elevation_spin = Gtk.Template.Child('elevation_spin')

    azimuth_adj = Gtk.Template.Child('azimuth_adj')
    elevation_adj = Gtk.Template.Child('elevation_adj')

    def __init__(self, job_callback, gray=None, azimuth=None, elevation=None) -> None:
        super().__init__()

        if gray:
            self.gray_check.set_active(gray)

        if azimuth:
            self.azimuth_adj.set_value(azimuth)

        if elevation:
            self.elevation_adj.set_value(elevation)

        self.gray = self.gray_check.get_active()
        self.azimuth = self.azimuth_adj.get_value()
        self.elevation = self.elevation_adj.get_value()

        self.gray_check.connect('toggled', self.toggled)
        self.azimuth_spin.connect('value-changed', self.on_spin_change)
        self.elevation_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.gray, self.azimuth, self.elevation)
    
    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        match spin:
            case self.azimuth_spin:
                self.azimuth = float(value)
            case self.elevation_spin:
                self.elevation = float(value)  

        self.start_job(self.gray, self.azimuth, self.elevation)
    
    def toggled(self, check):
        self.gray = check.get_active()
        self.start_job(self.gray, self.azimuth, self.elevation)
