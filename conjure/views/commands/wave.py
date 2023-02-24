from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/wave.ui')
class Wave(Adw.Bin):
    __gtype_name__ = 'Wave'

    dropdown = Gtk.Template.Child('dropdown')

    amplitude_spin = Gtk.Template.Child('amplitude_spin')
    amplitude_adj = Gtk.Template.Child('amplitude_adj')

    length_spin = Gtk.Template.Child('length_spin')
    length_adj = Gtk.Template.Child('length_adj')

    def __init__(self, job_callback, amplitude=None, length=None) -> None:
        super().__init__()

        if amplitude != None:
            self.amplitude_adj.set_value(amplitude)
        if length != None:
            self.length_adj.set_value(length)

        self.method = self.dropdown.get_selected()
        self.amplitude = self.amplitude_spin.get_value()
        self.wave_length = self.length_spin.get_value()


        self.amplitude_spin.connect('value-changed', self.on_spin_change)
        self.length_spin.connect('value-changed', self.on_spin_change)
        self.dropdown.connect('notify::selected', lambda dropdown, _value: self.on_method_change(dropdown.get_selected()))

        self.start_job = job_callback
        self.on_method_change(0)

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)

        match spin:
            case self.amplitude_spin:
                self.amplitude = float(value)
            case self.length_spin:
                self.wave_length = float(value)

        self.start_job(self.amplitude, self.wave_length, self.method)
            
    def on_method_change(self, selected_method):
        self.method = selected_method
        self.start_job(self.amplitude, self.wave_length, self.method)