from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/radius.ui')
class Radius(Adw.Bin):
    __gtype_name__ = 'Radius'

    radius_spin = Gtk.Template.Child('radius_spin')
    radius_adj = Gtk.Template.Child('radius_adj')
    
    def __init__(self, job_callback, radius=None) -> None:
        super().__init__()

        if radius != None:
            self.radius_adj.set_value(radius)

        self.radius = self.radius_spin.get_value()

        self.radius_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.radius)
    

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        self.radius = float(value)
        self.start_job(self.radius)
            
