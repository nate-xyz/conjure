from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/factor.ui')
class Factor(Adw.Bin):
    __gtype_name__ = 'Factor'

    factor_spin = Gtk.Template.Child('factor_spin')
    factor_adj = Gtk.Template.Child('factor_adj')
    
    def __init__(self, job_callback, factor=None) -> None:
        super().__init__()

        if factor != None:
            self.factor_adj.set_value(factor)

        self.factor = self.factor_spin.get_value()

        self.factor_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.factor)
    

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        self.factor = float(value)
        self.start_job(self.factor)
            
