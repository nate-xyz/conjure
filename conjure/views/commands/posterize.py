from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/posterize.ui')
class Posterize(Adw.Bin):
    __gtype_name__ = 'Posterize'

    dropdown = Gtk.Template.Child('dropdown')

    levels_spin = Gtk.Template.Child('levels_spin')
    levels_adj = Gtk.Template.Child('levels_adj')

    def __init__(self, job_callback, levels=None) -> None:
        super().__init__()

        if levels != None:
            self.levels_adj.set_value(levels)

        self.dropdown.set_selected(3)

        self.method = self.dropdown.get_selected()
        self.levels = int(self.levels_spin.get_value())

        self.levels_spin.connect('value-changed', self.on_spin_change)
        self.dropdown.connect('notify::selected', lambda dropdown, _value: self.on_method_change(dropdown.get_selected()))

        self.start_job = job_callback
        self.start_job(self.levels, self.method)

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        self.levels = int(value)
        self.start_job(self.levels, self.method)
            
    def on_method_change(self, selected_method):
        self.method = selected_method
        self.start_job(self.levels, self.method)