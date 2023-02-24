from gi.repository import Adw, Gtk

from loguru import logger

from wand.font import Font

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/polaroid.ui')
class Polaroid(Adw.Bin):
    __gtype_name__ = 'Polaroid'

    caption_row = Gtk.Template.Child('caption_row')
    font_row = Gtk.Template.Child('font_row')
    dropdown = Gtk.Template.Child('dropdown')
    angle_spin = Gtk.Template.Child('angle_spin')
    angle_adj = Gtk.Template.Child('angle_adj')

    def __init__(self, job_callback, amount=None) -> None:
        super().__init__()

        if amount != None:
            self.angle_adj.set_value(amount)


        self.method = self.dropdown.get_selected()
        self.angle = self.angle_spin.get_value()
        self.font = None 
        self.caption = None

        self.caption_row.connect('changed', self.on_caption_change)
        self.font_row.connect('changed', self.on_font_change)
        self.angle_spin.connect('value-changed', self.on_spin_change)
        self.dropdown.connect('notify::selected', lambda dropdown, _value: self.on_method_change(dropdown.get_selected()))

        self.start_job = job_callback
        self.on_method_change(0)

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        self.angle = float(value)
        self.start_job(self.angle, self.font, self.caption, self.method)
            
    def on_method_change(self, selected_method):
        self.method = selected_method
        self.start_job(self.angle, self.font, self.caption, self.method)

    def on_caption_change(self, row):
        self.caption = row.get_text()
        self.start_job(self.angle, self.font, self.caption, self.method)
    
    def on_font_change(self, row):
        value = row.get_text()

        try:
            _font = Font(value)
        except Exception as e:
            logger.error(e)
            return

        self.font = value
        self.start_job(self.angle, self.font, self.caption, self.method)