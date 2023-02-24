from gi.repository import Gtk, Adw

from wand.color import Color

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/color_alpha.ui')
class ColorAlpha(Adw.Bin):
    __gtype_name__ = 'ColorAlpha'

    color_entry_row = Gtk.Template.Child('color_entry_row')

    red_spin = Gtk.Template.Child('red_spin')
    green_spin = Gtk.Template.Child('green_spin')
    blue_spin = Gtk.Template.Child('blue_spin')  

    red_adj = Gtk.Template.Child('red_adj')
    green_adj = Gtk.Template.Child('green_adj')
    blue_adj = Gtk.Template.Child('blue_adj')

    def __init__(self, job_callback, red=None, green=None, blue=None) -> None:
        super().__init__()

        if red:
            self.red_adj.set_value(red)

        if green:
            self.green_adj.set_value(green)

        if blue:
            self.blue_adj.set_value(blue)


        self.color = 'yellow'
        self.color_entry_row.set_text(self.color)

        self.red = self.red_spin.get_value()
        self.green = self.green_spin.get_value()
        self.blue = self.blue_spin.get_value()

        self.color_entry_row.connect('changed', self.on_entry_change)
        self.red_spin.connect('value-changed', self.on_spin_change)
        self.green_spin.connect('value-changed', self.on_spin_change)
        self.blue_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.color, self.red, self.green, self.blue)
    
    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        match spin:
            case self.red_spin:
                self.red = float(value)
            
            case self.green_spin:
                self.green = float(value)
            
            case self.blue_spin:
                self.blue = float(value)  

        self.start_job(self.color, self.red, self.green, self.blue)


    def on_entry_change(self, row):
        value = row.get_text()

        try:
            _color = Color(value)
        except Exception as e:
            logger.error(e)
            return

        self.color = value
        self.start_job(self.color, self.red, self.green, self.blue)
