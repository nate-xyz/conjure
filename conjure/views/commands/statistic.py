from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/statistic.ui')
class Statistic(Adw.Bin):
    __gtype_name__ = 'Statistic'

    dropdown = Gtk.Template.Child('dropdown')

    width_spin = Gtk.Template.Child('width_spin')
    width_adj = Gtk.Template.Child('width_adj')

    height_spin = Gtk.Template.Child('height_spin')
    height_adj = Gtk.Template.Child('height_adj')

    def __init__(self, job_callback, width=None, height=None) -> None:
        super().__init__()

        if width != None:
            self.width_adj.set_value(width)
        if height != None:
            self.height_adj.set_value(height)

        self.dropdown.set_selected(3)

        self.method = self.dropdown.get_selected()
        self.width = int(self.width_spin.get_value())
        self.height = int(self.height_spin.get_value())

        self.width_spin.connect('value-changed', self.on_spin_change)
        self.height_spin.connect('value-changed', self.on_spin_change)
        self.dropdown.connect('notify::selected', lambda dropdown, _value: self.on_method_change(dropdown.get_selected()))

        self.start_job = job_callback
        self.on_method_change(self.method)

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)

        match spin:
            case self.width_spin:
                self.width = int(value)
            case self.height_spin:
                self.height = int(value)

        self.start_job(self.method, self.width, self.height)
            
    def on_method_change(self, selected_method):
        self.method = selected_method
        self.start_job(self.method, self.width, self.height)