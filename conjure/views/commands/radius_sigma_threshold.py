from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/radius_sigma_threshold.ui')
class RadiusSigmaThreshold(Adw.Bin):
    __gtype_name__ = 'RadiusSigmaThreshold'

    radius_spin = Gtk.Template.Child('radius_spin')
    sigma_spin = Gtk.Template.Child('sigma_spin')
    threshold_spin = Gtk.Template.Child('threshold_spin')  

    radius_adj = Gtk.Template.Child('radius_adj')
    sigma_adj = Gtk.Template.Child('sigma_adj')
    threshold_adj = Gtk.Template.Child('threshold_adj')

    def __init__(self, job_callback, radius=None, sigma=None, threshold=None) -> None:
        super().__init__()

        if radius:
            self.radius_adj.set_value(radius)

        if sigma:
            self.sigma_adj.set_value(sigma)

        if threshold:
            self.threshold_adj.set_value(threshold)

        self.radius = self.radius_spin.get_value()
        self.sigma = self.sigma_spin.get_value()
        self.threshold = self.threshold_spin.get_value()

        self.radius_spin.connect('value-changed', self.on_spin_change)
        self.threshold_spin.connect('value-changed', self.on_spin_change)
        self.sigma_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.radius, self.sigma, self.threshold)
    
    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        match spin:
            case self.radius_spin:
                self.radius = int(value)
            case self.sigma_spin:
                self.sigma = int(value)
            case self.threshold_spin:
                self.threshold = int(value)  

        self.start_job(self.radius, self.sigma, self.threshold)