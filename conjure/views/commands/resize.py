from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/resize.ui')
class ResizeCommand(Adw.Bin):
    __gtype_name__ = 'ResizeCommand'

    width_row: Gtk.SpinButton = Gtk.Template.Child('width_row')
    height_row: Gtk.SpinButton = Gtk.Template.Child('height_row')

    def __init__(self, job_callback, size) -> None:
        super().__init__()
        self.width, self.height = size

        self.width_row.set_input_purpose(Gtk.InputPurpose.DIGITS)
        self.height_row.set_input_purpose(Gtk.InputPurpose.DIGITS)

        self.width_row.set_text(str(self.width))
        self.height_row.set_text(str(self.height))

        self.width_row.connect('changed', self.on_entry_change)
        self.height_row.connect('changed', self.on_entry_change)

        self.start_job = job_callback

    def on_entry_change(self, row):
        value = row.get_text()

        try:
            number = int(value)
        except Exception as e:
            logger.error(e)
            return

        if row == self.width_row:
            self.width = number            
        else:
            self.height = number

        self.start_job(self.width, self.height)