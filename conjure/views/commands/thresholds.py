from gi.repository import Adw, Gtk

from loguru import logger

from .width_height_offset import WidthHeightOffset
from .auto_threshold import AutoThreshold
from .color_threshold import ColorThreshold
from .color_threshold_start_stop import ColorThresholdStartStop
# from .ordered_dither import OrderedDither
from .low_high import LowHigh
from .low_high_white_black import LowHighWhiteBlack

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/thresholds.ui')
class ThresholdCommands(Adw.Bin):
    __gtype_name__ = 'ThresholdCommands'

    sharpen_dropdown: Gtk.SpinButton = Gtk.Template.Child('sharpen_dropdown')
    parameters_bin: Gtk.SpinButton = Gtk.Template.Child('parameters_bin')

    def __init__(self, job_callback) -> None:
        super().__init__()
        self.sharpen_dropdown.connect('notify::selected', lambda dropdown, _value: self.on_command_change(dropdown.get_selected()))
        self.start_job = job_callback
        self.on_command_change(0)


    def on_command_change(self, selected_command):
        logger.debug(f'on_command_change: threshold {selected_command}')
        parameters = None
        match selected_command:
            case 0: #ADAPTIVE (radius, sigma)
                parameters = WidthHeightOffset(lambda w, h, o: self.start_job(selected_command, (w, h, o)))
            case 1: 
                parameters = AutoThreshold(lambda m: self.start_job(selected_command, (m)))
            case 2: #black
                parameters = ColorThreshold(lambda c: self.start_job(selected_command, (c)))
            case 3: #color
                parameters = ColorThresholdStartStop(lambda start, stop: self.start_job(selected_command, (start, stop)))
            # case 4: #ordered dither
            #     parameters = OrderedDither(lambda m: self.start_job(selected_command, (m)))
            case 4: #random threshold
                parameters = LowHigh(lambda l, h: self.start_job(selected_command, (l, h)))
            case 5: #range threshold
                parameters = LowHighWhiteBlack(lambda lb, lw, hw, hb: self.start_job(selected_command, (lb, lw, hw, hb)))
            case 6: #white threshold
                parameters = ColorThreshold(lambda c: self.start_job(selected_command, (c)))
        
        self.parameters_bin.set_child(parameters)

