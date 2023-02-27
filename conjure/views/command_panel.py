from gi.repository import Adw, Gtk

import sys
import threading
from loguru import logger

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from conjure.window import Window
    from conjure.magic import Magic

from .commands import ResizeCommand, RadiusSigma, CropCommand, BlurCommands, Radius, Shade, SharpenCommands, Factor, ColorAlpha, RadiusSigmaAngle, Threshold, Angle, AmountMethod, Polaroid, Noise, RadiusSigmaXY, Wave, ThresholdSoftness, Rotate, Statistic, KMeans, Posterize, Quantize, ThresholdCommands, FXExpression, OrderedDither

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/command_panel.ui')
class CommandPanel(Adw.Bin):
    __gtype_name__ = 'CommandPanel'

    command_dropdown = Gtk.Template.Child('command_dropdown')
    parameters_bin = Gtk.Template.Child('parameters_bin')

    def __init__(self) -> None:
        super().__init__()
        self.window: Optional[Window] = None
        self.magic: Optional[Magic] = None
        self.current_command: int = 0
        self.command_dropdown.connect('notify::selected', lambda dropdown, _value: self.on_command_change(dropdown.get_selected()))

        self.thread_id = None
        self.threads = []

    def saturate(self, window, magic):
        self.window = window 
        self.magic = magic

    def reload(self):
        self.on_command_change(self.current_command)

    def on_command_change(self, selected_command):
        logger.debug(f'on_command_change {selected_command}')
        parameters = None
        if self.magic.current_image:
            match selected_command:
                case 1: #RESIZE
                    parameters = ResizeCommand(lambda w, h: self.start_job(self.magic.resize, (w, h)), self.magic.current_image.size)         
                case 2: #CROP
                    parameters = CropCommand(lambda l, t, w, h: self.start_job(self.magic.crop, (l, t, w, h)), self.magic.current_image.size)
                case 3: #SEAM CARVING
                    parameters = ResizeCommand(lambda w, h: self.start_job(self.magic.resize, (w, h)), self.magic.current_image.size)
                case 4: #BLUR
                    parameters = BlurCommands(lambda j, a: self.blur_job(j, a))
                case 5: #DESPECKLE
                    self.start_job(self.magic.despeckle, None)
                case 6: # EDGE
                    parameters = Radius(lambda r: self.start_job(self.magic.edge, (r)))
                case 7: #EMBOSS
                    parameters = RadiusSigma(lambda r, s: self.start_job(self.magic.emboss, (r, s)), radius=3.0, sigma=1.5)               
                case 8: #KUWAHARA
                    parameters = RadiusSigma(lambda r, s: self.start_job(self.magic.kuwahara, (r, s)), radius=2.0, sigma=1.5)    
                case 9: #SHADE
                    parameters = Shade(lambda g, a, e: self.start_job(self.magic.shade, (g, a, e)))
                case 10: #SHARPEN
                    parameters = SharpenCommands(lambda j, a: self.sharpen_job(j, a))
                case 11: #SPREAD
                    parameters = Radius(lambda r: self.start_job(self.magic.spread, (r)), radius=8.0)
                case 12: #ADD NOISE
                    parameters = Noise(lambda t, a: self.start_job(self.magic.noise, (t, a)))
                case 13: #BLUESHIFT
                    parameters = Factor(lambda f: self.start_job(self.magic.blue_shift, (f)))
                case 14: #CHARCOAL
                    parameters = RadiusSigma(lambda r, s: self.start_job(self.magic.charcoal, (r, s)))
                case 15: #COLORIZE
                    parameters = ColorAlpha(lambda c, r, g, b: self.start_job(self.magic.colorize, (c, r, g, b)))
                case 16: #FX 
                    parameters = FXExpression(lambda command: self.start_job(self.magic.fx, (command)))
                case 17: #IMPLODE
                    parameters = AmountMethod(lambda m, a: self.start_job(self.magic.implode, (m, a)))
                case 18: #POLAROID
                    parameters = Polaroid(lambda a, c, f, m: self.start_job(self.magic.polaroid, (a, c, f, m)))
                case 19: #SEPIA_TONE
                    parameters = Threshold(lambda t: self.start_job(self.magic.sepia_tone, (t)))
                case 20: #SKETCH
                    parameters = RadiusSigmaAngle(lambda r, s, a: self.start_job(self.magic.sketch, (r, s, a)), 0.5, 0.0, 98.0)
                case 21: #SOLARIZE
                    parameters = Threshold(lambda t: self.start_job(self.magic.solarize, (t)), 0.5)
                # case 22: #STEREOGRAM
                #     self.start_job(self.magic.stereogram, None)
                case 22: #SWIRL
                    parameters = Angle(lambda a: self.start_job(self.magic.swirl, (a)), 90)
                case 23: #TINT
                    parameters = ColorAlpha(lambda c, r, g, b: self.start_job(self.magic.tint, (c, r, g, b)), red=102, green=153, blue=204)
                case 24: #VIGNETTE
                    parameters = RadiusSigmaXY(lambda r, s, x, y: self.start_job(self.magic.vignette, (r, s, x, y)), self.magic.current_image.size)
                case 25: #WAVE
                    parameters = Wave(lambda a, l, m: self.start_job(self.magic.wave, (a, l, m)))
                case 26: #WAVELET DESNOISE
                    parameters = ThresholdSoftness(lambda t, s: self.start_job(self.magic.wavelet_denoise, (t, s)))
                case 27: #ENHANCE
                    self.start_job(self.magic.enhance, None)
                case 28: #FLIP
                    self.start_job(self.magic.flip, None)
                case 29: #FLOP
                    self.start_job(self.magic.flop, None)
                case 30: #ROTATE
                    parameters = Rotate(lambda a, c: self.start_job(self.magic.rotate, (a, c)))
                case 31: #STATISTIC
                    parameters = Statistic(lambda m, w, h: self.start_job(self.magic.statistic, (m, w, h)))
                case 32: #KMEANS
                    parameters = KMeans(lambda c, i, t: self.start_job(self.magic.kmeans, (c, i, t)))
                case 33: #POSTERIZE
                    parameters = Posterize(lambda l, d: self.start_job(self.magic.posterize, (l, d)))
                case 34: #QUANTIZE
                    parameters = Quantize(lambda nc, ct, td, d, me: self.start_job(self.magic.quantize, (nc, ct, td, d, me)))
                case 35: #ORDERED DITHER
                    parameters = OrderedDither(lambda m: self.start_job(self.magic.ordered_dither, (m)))
                case 36: #THRESHOLD COMMANDS
                    parameters = ThresholdCommands(lambda j, a: self.threshold_job(j, a))

            self.current_command = selected_command
            self.parameters_bin.set_child(parameters)
        else:
            self.window.add_error_toast(_("Unable select command, no image loaded."))

    def blur_job(self, blur_command, args):
        match blur_command:
            case 0: #normal
                job = self.magic.blur
            case 1: #adaptive
                job = self.magic.blur_adaptive
            case 2: #gaussian
                job = self.magic.blur_gaussian
            case 3: #motion
                job = self.magic.blur_motion
            case 4: #rotational
                job = self.magic.blur_rotational
            case 5: #selective
                job = self.magic.blur_selective
        self.start_job(job, args)

    def sharpen_job(self, blur_command, args):
        match blur_command:
            case 0: #normal
                job = self.magic.sharpen
            case 1: #adaptive
                job = self.magic.sharpen_adaptive
            case 2: #unsharp mask
                job = self.magic.sharpen_unsharp_mask

        self.start_job(job, args)

    def threshold_job(self, command, args):
        match command:
            case 0: #adaptive
                job = self.magic.adaptive_threshold
            case 1: #auto
                job = self.magic.auto_threshold
            case 2: #black
                job = self.magic.black_threshold
            case 3: #color
                job = self.magic.color_threshold
            # case 4: #ordered
            #     job = self.magic.ordered_dither
            case 4:
                job = self.magic.random_threshold
            case 5:
                job = self.magic.range_threshold
            case 6:
                job = self.magic.white_threshold

        self.start_job(job, args)

    def start_job(self, job, args):
        logger.debug('start_job')
        if self.magic.current_image != None:

            for t in self.threads:
                t.kill()

            self.threads = []

            try:                
                thread = KillableThread(
                    target=job,
                    args=(
                        self.job_done,
                        args,
                    ))

                thread.daemon = True 
                thread.start()
                self.thread_id = thread.ident
                self.threads.append(thread)

                self.window.image_drop_page.display_image.start_job()
                

            except Exception as e:
                logger.error(e)
                self.window.add_error_toast(_("Unable to start conversion."))
                
        else:
            self.window.add_error_toast(_("Unable to start conversion, no image loaded."))

    def job_done(self, img_blob, size, thread_id):
        logger.debug('job_done')
    
        if self.thread_id != thread_id:
            logger.debug(f"wrong process id {self.thread_id} != {thread_id}")
            return;

        if img_blob != None:
            self.window.image_drop_page.load_transformed(img_blob, size)
        else:
            self.window.add_error_toast(_("Unable to complete conversion."))
            self.window.image_drop_page.display_image.stop_job()
        


class KillableThread(threading.Thread): 
  def __init__(self, *args, **keywords): 
    threading.Thread.__init__(self, *args, **keywords) 
    self.killed = False
  
  def start(self): 
    self.__run_backup = self.run 
    self.run = self.__run       
    threading.Thread.start(self) 
  
  def __run(self): 
    sys.settrace(self.globaltrace) 
    self.__run_backup() 
    self.run = self.__run_backup 
  
  def globaltrace(self, frame, event, arg): 
    if event == 'call': 
      return self.localtrace 
    else: 
      return None
  
  def localtrace(self, frame, event, arg): 
    if self.killed: 
      if event == 'line': 
        raise SystemExit() 
    return self.localtrace 
  
  def kill(self): 
    logger.debug(f"killing {threading.get_ident()}")
    self.killed = True
