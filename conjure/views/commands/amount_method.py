from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/amount_method.ui')
class AmountMethod(Adw.Bin):
    __gtype_name__ = 'AmountMethod'

    dropdown = Gtk.Template.Child('dropdown')
    amount_spin = Gtk.Template.Child('amount_spin')
    amount_adj = Gtk.Template.Child('amount_adj')

    def __init__(self, job_callback, amount=None) -> None:
        super().__init__()

        if amount != None:
            self.amount_adj.set_value(amount)


        self.method = self.dropdown.get_selected()
        self.amount = self.amount_spin.get_value()

        self.amount_spin.connect('value-changed', self.on_spin_change)
        self.dropdown.connect('notify::selected', lambda dropdown, _value: self.on_method_change(dropdown.get_selected()))

        self.start_job = job_callback
        #self.start_job(self.method, self.amount)
        self.on_method_change(0)

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        self.amount = float(value)
        self.start_job(self.method, self.amount)
            
    def on_method_change(self, selected_method):
        self.method = selected_method
        self.start_job(self.method, self.amount)
