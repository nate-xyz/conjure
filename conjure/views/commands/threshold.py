from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/threshold.ui')
class Threshold(Adw.Bin):
    __gtype_name__ = 'Threshold'

    threshold_spin = Gtk.Template.Child('threshold_spin')
    threshold_adj = Gtk.Template.Child('threshold_adj')
    
    def __init__(self, job_callback, threshold=None) -> None:
        super().__init__()

        if threshold != None:
            self.threshold_adj.set_value(threshold)

        self.threshold = self.threshold_spin.get_value()

        self.threshold_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.threshold)
    

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        self.threshold = float(value)
        self.start_job(self.threshold)
            
