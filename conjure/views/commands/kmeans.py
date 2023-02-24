from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/kmeans.ui')
class KMeans(Adw.Bin):
    __gtype_name__ = 'KMeans'

    colors_spin = Gtk.Template.Child('colors_spin')
    iterations_spin = Gtk.Template.Child('iterations_spin')
    tolerance_spin = Gtk.Template.Child('tolerance_spin')  

    colors_adj = Gtk.Template.Child('colors_adj')
    iterations_adj = Gtk.Template.Child('iterations_adj')
    tolerance_adj = Gtk.Template.Child('tolerance_adj')

    def __init__(self, job_callback, colors=None, iterations=None, tolerance=None) -> None:
        super().__init__()

        if colors:
            self.colors_adj.set_value(colors)

        if iterations:
            self.iterations_adj.set_value(iterations)

        if tolerance:
            self.tolerance_adj.set_value(tolerance)

        self.colors = int(self.colors_spin.get_value())
        self.iterations = int(self.iterations_spin.get_value())
        self.tolerance = self.tolerance_spin.get_value()

        self.colors_spin.connect('value-changed', self.on_spin_change)
        self.tolerance_spin.connect('value-changed', self.on_spin_change)
        self.iterations_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.colors, self.iterations, self.tolerance)
    
    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        match spin:
            case self.colors_spin:
                self.colors = int(value)
            case self.iterations_spin:
                self.iterations = int(value)
            case self.tolerance_spin:
                self.tolerance = float(value)  

        self.start_job(self.colors, self.iterations, self.tolerance)