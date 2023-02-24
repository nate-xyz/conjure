from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/threshold_softness.ui')
class ThresholdSoftness(Adw.Bin):
    __gtype_name__ = 'ThresholdSoftness'

    threshold_spin = Gtk.Template.Child('threshold_spin')
    softness_spin = Gtk.Template.Child('softness_spin')

    threshold_adj = Gtk.Template.Child('threshold_adj')
    softness_adj = Gtk.Template.Child('softness_adj')
    
    def __init__(self, job_callback, threshold=None, softness=None) -> None:
        super().__init__()

        if threshold != None:
            self.threshold_adj.set_value(threshold)

        if softness != None:
            self.softness_adj.set_value(softness)


        self.threshold = self.threshold_spin.get_value()
        self.softness = self.softness_spin.get_value()

        self.threshold_spin.connect('value-changed', self.on_spin_change)
        self.softness_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.threshold, self.softness)
    

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        match spin:
            case self.threshold_spin:
                self.threshold = float(value)
            case self.softness_spin:
                self.softness = float(value)
        
        self.start_job(self.threshold, self.softness)
            
