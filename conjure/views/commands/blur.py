from gi.repository import Adw, Gtk

from loguru import logger

from .radius_sigma import RadiusSigma
from .radius_sigma_angle import RadiusSigmaAngle
from .radius_sigma_threshold import RadiusSigmaThreshold
from .angle import Angle

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/blur.ui')
class BlurCommands(Adw.Bin):
    __gtype_name__ = 'BlurCommands'

    blur_dropdown: Gtk.SpinButton = Gtk.Template.Child('blur_dropdown')
    parameters_bin: Gtk.SpinButton = Gtk.Template.Child('parameters_bin')

    def __init__(self, job_callback) -> None:
        super().__init__()
        self.blur_dropdown.connect('notify::selected', lambda dropdown, _value: self.on_command_change(dropdown.get_selected()))
        self.start_job = job_callback
        self.on_command_change(0)

    def on_command_change(self, selected_command):
        self.blur_command = selected_command
        logger.debug('on_command_change')
        parameters = None
        match selected_command:
            case 0: #NORMAL (radius, sigma)
                self.radius, self.sigma = 0.0, 3.0
                parameters = RadiusSigma(lambda r, s: self.start_job(0, (r, s)), 0.0, 3.0)

            case 1: #ADAPTIVE (radius, sigma)
                self.radius, self.sigma = 8.0, 4.0
                parameters = RadiusSigma(lambda r, s: self.start_job(1, (r, s)), 8.0, 4.0)
       
            case 2: #GAUSSIAN (radius, sigma)
                self.radius, self.sigma = 0.0, 3.0
                parameters = RadiusSigma(lambda r, s: self.start_job(2, (r, s)), 0.0, 3.0)
            case 3: #MOTION (radius, sigma, angle)
                self.radius, self.sigma, self.angle = 16.0, 8.0, 315
                parameters = RadiusSigmaAngle(lambda r, s, a: self.start_job(3, (r, s, a)), 16.0, 8.0, 315)

            case 4: #ROTATIONAL (angle)
                self.angle = 15
                parameters = Angle(lambda a: self.start_job(4, (a)), 15)

            case 5: #SELECTIVE (radius, sigma, threshold)
                self.radius, self.sigma, self.threshold = 8.0, 3.0, 0.25
                parameters = RadiusSigmaThreshold(lambda r, s, t: self.start_job(5, (r, s, t)), 8.0, 3.0, 0.25)
    
        self.parameters_bin.set_child(parameters)

