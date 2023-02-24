from gi.repository import Adw, Gtk

from loguru import logger

from .radius_sigma import RadiusSigma
from .radius_sigma_amount_threshold import RadiusSigmaAmountThreshold

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/sharpen.ui')
class SharpenCommands(Adw.Bin):
    __gtype_name__ = 'SharpenCommands'

    sharpen_dropdown: Gtk.SpinButton = Gtk.Template.Child('sharpen_dropdown')
    parameters_bin: Gtk.SpinButton = Gtk.Template.Child('parameters_bin')

    def __init__(self, job_callback) -> None:
        super().__init__()
        self.sharpen_dropdown.connect('notify::selected', lambda dropdown, _value: self.on_command_change(dropdown.get_selected()))
        self.start_job = job_callback
        self.on_command_change(0)

    def on_command_change(self, selected_command):
        logger.debug('on_command_change: sharpen')
        parameters = None
        match selected_command:
            case 0: #NORMAL (radius, sigma)
                parameters = RadiusSigma(lambda r, s: self.start_job(0, (r, s)), 8.0, 4.0)

            case 1: #ADAPTIVE (radius, sigma)
                parameters = RadiusSigma(lambda r, s: self.start_job(1, (r, s)), 8.0, 4.0)
       
            case 2: #UNSHARP MASK (radius, sigma)
                parameters = RadiusSigmaAmountThreshold(lambda r, s, a, t: self.start_job(2, (r, s, a, t)), 10.0, 4.0, 1.0, 0.0)

        self.parameters_bin.set_child(parameters)

