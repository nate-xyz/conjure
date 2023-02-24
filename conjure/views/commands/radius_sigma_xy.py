from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/radius_sigma_xy.ui')
class RadiusSigmaXY(Adw.Bin):
    __gtype_name__ = 'RadiusSigmaXY'

    radius_spin = Gtk.Template.Child('radius_spin')
    sigma_spin = Gtk.Template.Child('sigma_spin')
    x_spin = Gtk.Template.Child('x_spin')  
    y_spin = Gtk.Template.Child('y_spin')  

    radius_adj = Gtk.Template.Child('radius_adj')
    sigma_adj = Gtk.Template.Child('sigma_adj')

    def __init__(self, job_callback, image_size, radius=None, sigma=None, x=None, y=None) -> None:
        super().__init__()

        if radius:
            self.radius_adj.set_value(radius)

        if sigma:
            self.sigma_adj.set_value(sigma)

        if x:
            self.x_adj.set_value(x)

        if y:
            self.y_adj.set_value(y)

        self.width, self.height = image_size

        #new (value, lower, upper, step_increment, page_increment, page_size)
        self.x_adjustment = Gtk.Adjustment.new(10, 0.0, self.width/2 - 1, 5.0, 0, 0)
        self.x_spin.set_adjustment(self.x_adjustment)

        self.y_adjustment = Gtk.Adjustment.new(10, 0.0, self.height/2 - 1, 5.0, 0, 0)
        self.y_spin.set_adjustment(self.y_adjustment)

        self.radius = self.radius_spin.get_value()
        self.sigma = self.sigma_spin.get_value()
        self.x = int(self.x_spin.get_value())
        self.y = int(self.y_spin.get_value())

        self.radius_spin.connect('value-changed', self.on_spin_change)
        self.sigma_spin.connect('value-changed', self.on_spin_change)
        self.x_spin.connect('value-changed', self.on_spin_change)
        self.y_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.radius, self.sigma, self.x, self.y)
    
    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        match spin:
            case self.radius_spin:
                self.radius = float(value)
            case self.sigma_spin:
                self.sigma = float(value)
            case self.x_spin:
                self.x = int(value)  
            case self.y_spin:
                self.y = int(value)  

        self.start_job(self.radius, self.sigma, self.x, self.y)