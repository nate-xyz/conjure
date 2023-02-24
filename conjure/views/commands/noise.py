from gi.repository import Adw, Gtk

from loguru import logger

from wand.font import Font

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/noise.ui')
class Noise(Adw.Bin):
    __gtype_name__ = 'Noise'

    dropdown: Gtk.DropDown = Gtk.Template.Child('dropdown')
    attenuate_spin = Gtk.Template.Child('attenuate_spin')
    attenuate_adj = Gtk.Template.Child('attenuate_adj')

    def __init__(self, job_callback, type=None, attenuate=None) -> None:
        super().__init__()

        if attenuate != None:
            self.attenuate_adj.set_value(attenuate)

        if type != None:
            self.dropdown.set_selected(type)
        else:
            self.dropdown.set_selected(5)

        self.type = self.dropdown.get_selected()
        self.angle = self.attenuate_spin.get_value()

        self.attenuate_spin.connect('value-changed', self.on_spin_change)
        self.dropdown.connect('notify::selected', lambda dropdown, _value: self.on_type_change(dropdown.get_selected()))

        self.start_job = job_callback
        self.on_type_change(self.type)

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        self.angle = float(value)
        self.start_job(self.type, self.angle)
            
    def on_type_change(self, selected_type):
        self.type = selected_type
        self.start_job(self.type, self.angle)