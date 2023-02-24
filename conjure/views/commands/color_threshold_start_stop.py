from gi.repository import Gtk, Adw

from wand.color import Color

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/color_threshold_start_stop.ui')
class ColorThresholdStartStop(Adw.Bin):
    __gtype_name__ = 'ColorThresholdStartStop'

    start_color_entry_row = Gtk.Template.Child('start_color_entry_row')
    stop_color_entry_row = Gtk.Template.Child('stop_color_entry_row')

    def __init__(self, job_callback) -> None:
        super().__init__()

        self.start_color = '#333'
        self.start_color_entry_row.set_text(self.start_color)

        self.stop_color = '#cdc'
        self.stop_color_entry_row.set_text(self.stop_color)

        self.start_color_entry_row.connect('changed', self.on_entry_change)
        self.stop_color_entry_row.connect('changed', self.on_entry_change)

        self.start_job = job_callback
        self.start_job(self.start_color, self.stop_color)
    
    def on_entry_change(self, row):
        value = row.get_text()

        try:
            _color = Color(value)
        except Exception as e:
            logger.error(e)
            return

        match row:
            case self.start_color_entry_row:
                self.start_color = value 
            case self.stop_color_entry_row:
                self.stop_color - value

        self.color = value
        self.start_job(self.start_color, self.stop_color)
