from gi.repository import Gtk, Adw

from wand.color import Color

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/rotate.ui')
class Rotate(Adw.Bin):
    __gtype_name__ = 'Rotate'

    color_entry_row = Gtk.Template.Child('color_entry_row')
    angle_spin = Gtk.Template.Child('angle_spin')
    angle_adj = Gtk.Template.Child('angle_adj')


    def __init__(self, job_callback, angle=None) -> None:
        super().__init__()

        if angle:
            self.angle_adj.set_value(angle)



        # self.color_entry_row.set_text(self.color)
        self.color = None
        self.angle = self.angle_spin.get_value()


        self.color_entry_row.connect('changed', self.on_entry_change)
        self.angle_spin.connect('value-changed', self.on_spin_change)

        self.start_job = job_callback
        self.start_job(self.angle, self.color)
    
    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)
        self.angle = value
        self.start_job(self.angle, self.color)

    def on_entry_change(self, row):
        value = row.get_text()

        try:
            _color = Color(value)
        except Exception as e:
            logger.error(e)
            return

        self.color = value
        self.start_job(self.angle, self.color)
