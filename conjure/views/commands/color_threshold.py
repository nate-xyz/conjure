from gi.repository import Gtk, Adw

from wand.color import Color

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/color_threshold.ui')
class ColorThreshold(Adw.Bin):
    __gtype_name__ = 'ColorThreshold'

    color_entry_row = Gtk.Template.Child('color_entry_row')

    def __init__(self, job_callback) -> None:
        super().__init__()

        self.color = '#930'
        self.color_entry_row.set_text(self.color)

        self.color_entry_row.connect('changed', self.on_entry_change)

        self.start_job = job_callback
        self.start_job(self.color)
    
    def on_entry_change(self, row):
        value = row.get_text()

        try:
            _color = Color(value)
        except Exception as e:
            logger.error(e)
            return

        self.color = value
        self.start_job(self.color)
