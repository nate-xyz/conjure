from gi.repository import Gtk, Adw

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/fx.ui')
class FXExpression(Adw.Bin):
    __gtype_name__ = 'FXExpression'

    entry_row = Gtk.Template.Child('entry_row')

    def __init__(self, job_callback) -> None:
        super().__init__()

        self.entry_row.set_text("(hue > 0.9 || hue < 0.1) ? u : lightness")
        self.command = self.entry_row.get_text()

        self.entry_row.connect('changed', self.on_entry_change)

        self.start_job = job_callback
        self.start_job(self.command)

    def on_entry_change(self, row):
        self.command = row.get_text()
        self.start_job(self.command)
