from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/angle.ui')
class Angle(Adw.Bin):
    __gtype_name__ = 'Angle'

    angle_spin = Gtk.Template.Child('angle_spin')
    angle_adj = Gtk.Template.Child('angle_adj')
    
    def __init__(self, job_callback,  angle=None) -> None:
        super().__init__()

        if angle != None:
            self.angle_adj.set_value(angle)

        self.angle = self.angle_spin.get_value()

        self.angle_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.angle)
    

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        self.angle = float(value) 
                 
        self.start_job(self.angle)