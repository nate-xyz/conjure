from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/auto_threshold.ui')
class AutoThreshold(Adw.Bin):
    __gtype_name__ = 'AutoThreshold'

    dropdown = Gtk.Template.Child('dropdown')

    def __init__(self, job_callback) -> None:
        super().__init__()

        self.dropdown.set_selected(1)
        self.threshold_method = self.dropdown.get_selected()

        self.dropdown.connect('notify::selected', lambda dropdown, _value: self.on_dropdown_change(dropdown))

        self.start_job = job_callback
        self.start_job(self.threshold_method)

    def on_dropdown_change(self, dropdown):
        value = dropdown.get_selected()
        self.threshold_method = int(value)
        self.start_job(self.threshold_method)