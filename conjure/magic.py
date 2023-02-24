from gi.repository import GLib

from wand.image import Image, Font
from wand.display import display
import time
import os
from threading import get_ident
from loguru import logger

#MANAGE IMAGE RESOURCES & MAKE CALLS TO WAND LIBRARY
class Magic():
    def __init__(self) -> None:
        self.current_image = None 
        self.most_recent_image = None
        self.most_recent_transformation = ""
        self.image_history = [] 
        self.folder = None 
        self.file_name = None

    def open(self, uri) -> bool:
        try:
            self.uri = uri
            self.current_image = Image(filename=uri)
            self.reset_all()
            self.image_history.append((self.current_image, 'original image'))

            logger.debug(f"original folder: {os.path.dirname(uri)}")
            
            self.folder = os.path.dirname(uri)

            logger.debug(f"original filename {os.path.basename(uri)}")
            self.file_name = os.path.basename(uri)

            return True
        except Exception as e:
            logger.error(e)
            return False


    def save(self, uri) -> bool:
        try:
            with self.current_image.clone() as img:
                img.save(filename=uri)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def reset_all(self):
        self.most_recent_image = None
        self.image_history = [] 

    def visible_history(self) -> bool:
        return len(self.image_history) > 1

    def update_main_image_from_most_recent(self):
        self.current_image = self.most_recent_image
        self.image_history.append((self.most_recent_image, self.most_recent_transformation))
        logger.debug('updated main image from most recent')

    def update_main_image_from_index(self, index) -> bool:
        if index >= len(self.image_history) or index < 0:
            logger.error(f'tried to update main index from incorrect index {index}')
            return False
        self.most_recent_image = self.image_history[index][0]
        self.current_image = self.most_recent_image
        logger.debug(f'updated main image from index {index}')
        return True

    def resize(self, callback, args):
        logger.debug(f'resize {get_ident()}')
        time.sleep(0.25)
        width, height = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:

                img.resize(width, height)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"resize({width}x{height})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())

        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())


    def crop(self, callback, args):
        logger.debug(f'crop {get_ident()}')
        time.sleep(0.25)
        logger.debug(self.uri)
        logger.debug(args)
        left, top, width, height = args
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                print(left)
                img.crop(left, top, width=width, height=height)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"crop(left: {left}, top: {top}, {width}x{height})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())

        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())


    def seam_carving(self, callback, args):
        logger.debug(f'seam_carving {get_ident()}')
        time.sleep(0.25)
        width, height = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:

                img.liquid_rescale(width, height)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"seam_carving({width}x{height})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())

        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())


    def blur(self, callback, args):
        logger.debug(f'blur {get_ident()}')
        time.sleep(0.25)
        radius, sigma = args
        logger.debug(f"{radius} {sigma}")
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.blur(radius=radius, sigma=sigma)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"blur(radius={radius}, sigma={sigma})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def blur_adaptive(self, callback, args):
        logger.debug(f'blur_adaptive {get_ident()}')
        time.sleep(0.25)
        radius, sigma = args
        logger.debug(f"{radius} {sigma}")
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.adaptive_blur(radius=radius, sigma=sigma)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"adaptive_blur(radius={radius}, sigma={sigma})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def blur_gaussian(self, callback, args):
        logger.debug(f'blur_gaussian {get_ident()}')
        time.sleep(0.25)
        radius, sigma = args
        logger.debug(f"{radius} {sigma}")
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.gaussian_blur(radius=radius, sigma=sigma)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"gaussian_blur(radius={radius}, sigma={sigma})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def blur_motion(self, callback, args):
        logger.debug(f'blur_motion {get_ident()}')
        time.sleep(0.25)
        radius, sigma, angle = args
        logger.debug(f"{radius} {sigma}")
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.motion_blur(radius=radius, sigma=sigma)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"motion_blur(radius={radius}, sigma={sigma})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def blur_rotational(self, callback, args):
        logger.debug(f'blur_rotational {get_ident()}')
        time.sleep(0.25)
        angle = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.rotational_blur(angle=angle)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"rotational_blur(angle={angle})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def blur_selective(self, callback, args):
        logger.debug(f'blur_selective {get_ident()}')
        time.sleep(0.25)
        radius, sigma, threshold = args
        logger.debug(f"{radius} {sigma}")
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.selective_blur(radius=radius, sigma=sigma, threshold=threshold * img.quantum_range)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"selective_blur(radius={radius}, sigma={sigma}, threshold={threshold})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def despeckle(self, callback, _args):
        logger.debug(f'despeckle {get_ident()}')
        time.sleep(0.25)
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.despeckle()
                self.most_recent_image = img.clone()
                self.most_recent_transformation = "despeckle"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def edge(self, callback, args):
        logger.debug(f'edge {get_ident()}')
        time.sleep(0.25)
        radius = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.edge(radius=radius)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"edge(radius=radius{radius})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def emboss(self, callback, args):
        logger.debug(f'emboss {get_ident()}')
        time.sleep(0.25)
        radius, sigma = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.emboss(radius=radius, sigma=sigma)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"emboss(radius={radius}, sigma={sigma})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def kuwahara(self, callback, args):
        logger.debug(f'kuwahara {get_ident()}')
        time.sleep(0.25)
        radius, sigma = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.kuwahara(radius=radius, sigma=sigma)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"kuwahara(radius={radius}, sigma={sigma})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())
    
    def shade(self, callback, args):
        logger.debug(f'shade {get_ident()}')
        time.sleep(0.25)
        gray, azimuth, elevation = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.shade(gray=gray, azimuth=azimuth, elevation=elevation)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"shade(gray={gray}, azimuth={azimuth}, elevation={elevation})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def sharpen(self, callback, args):
        logger.debug(f'sharpen {get_ident()}')
        time.sleep(0.25)
        radius, sigma = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.sharpen(radius=radius, sigma=sigma)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"sharpen(radius={radius}, sigma={sigma})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def sharpen_adaptive(self, callback, args):
        logger.debug(f'adaptive_sharpen {get_ident()}')
        time.sleep(0.25)
        radius, sigma = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.adaptive_sharpen(radius=radius, sigma=sigma)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"adaptive_sharpen(radius={radius}, sigma={sigma})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def sharpen_unsharp_mask(self, callback, args):
        logger.debug(f'unsharp_mask {get_ident()}')
        time.sleep(0.25)
        radius, sigma, amount, threshold = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.unsharp_mask(radius=radius, sigma=sigma, amount=amount, threshold=threshold)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"unsharp_mask(radius={radius}, sigma={sigma}, amount={amount}, threshold={threshold})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def spread(self, callback, args):
        logger.debug(f'spread {get_ident()}')
        time.sleep(0.25)
        radius = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.spread(radius=radius)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"spread(radius={radius})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def noise(self, callback, args):
        logger.debug(f'noise {get_ident()}')
        time.sleep(0.25)
        t, attenuate = args
        type_map = {
            0: 'undefined',
            1: 'uniform',
            2: 'gaussian',
            3: 'multiplicative_gaussian',
            4: 'impulse',
            5: 'laplacian',
            6: 'poisson',
            7: 'random'
        }
        noise_type = type_map[t]
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.noise(noise_type=noise_type, attenuate=attenuate)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"noise(noise_type={noise_type}, attenuate={attenuate})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def blue_shift(self, callback, args):
        logger.debug(f'blue_shift {get_ident()}')
        time.sleep(0.25)
        factor = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.blue_shift(factor=factor)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"blue_shift(factor={factor})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def charcoal(self, callback, args):
        logger.debug(f'charcoal {get_ident()}')
        time.sleep(0.25)
        radius, sigma = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.charcoal(radius=radius, sigma=sigma)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"charcoal(radius={radius}, sigma={sigma})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())

        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())



    def colorize(self, callback, args):
        logger.debug(f'colorize {get_ident()}')
        time.sleep(0.25)
        color, r, g, b = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        alpha = f"rgb({r},{g},{b}"
        try:
            with self.current_image.clone() as img:
                img.colorize(color=color, alpha=alpha)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"colorize(color={color}, alpha={alpha})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def implode(self, callback, args):
        logger.debug(f'implode {get_ident()}')
        time.sleep(0.25)
        m, amount = args
        method_map = {
            0: 'undefined',
            1: 'average',
            2: 'average9',
            3: 'average16',
            4: 'background',
            5: 'bilinear',
            6: 'blend',
            7: 'catrom',
            8: 'integer',
            9: 'mesh',
            10: 'nearest',
            11: 'spline'
        }
        method = method_map[m]

        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.implode(amount=amount, method=method)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"implode(amount={amount}, method={method})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def polaroid(self, callback, args):
        logger.debug(f'polaroid {get_ident()}')
        time.sleep(0.25)
        angle, f, caption, m = args
        method_map = {
            0: 'undefined',
            1: 'average',
            2: 'average9',
            3: 'average16',
            4: 'background',
            5: 'bilinear',
            6: 'blend',
            7: 'catrom',
            8: 'integer',
            9: 'mesh',
            10: 'nearest',
            11: 'spline'
        }
        method = method_map[m]
        font = None
        if f:
            try:
                font=Font(f)
            except:
                font=None

        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                
                img.polaroid(angle=angle, caption=caption, font=font, method=method)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"polaroid(angle={angle}, caption={caption}, font={font}, method={method})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def sepia_tone(self, callback, args):
        logger.debug(f'sepia_tone {get_ident()}')
        time.sleep(0.25)
        threshold = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.sepia_tone(threshold=threshold)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"sepia_tone(threshold={threshold})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def sketch(self, callback, args):
        logger.debug(f'sketch {get_ident()}')
        time.sleep(0.25)
        radius, sigma, angle = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.sketch(radius=radius, sigma=sigma, angle=angle)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"sketch(radius={radius}, sigma={sigma}, angle={angle})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def solarize(self, callback, args):
        logger.debug(f'solarize {get_ident()}')
        time.sleep(0.25)
        threshold = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.solarize(threshold=threshold*img.quantum_range)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"solarize(threshold={threshold*img.quantum_range})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    # def stereogram(self, callback, _args):
    #     logger.debug(f'stereogram {get_ident()}')
    #     time.sleep(0.25)
    #     logger.debug(self.uri)
    #     if self.current_image == None:
    #         logger.debug('current none')
    #     try:
    #         with self.current_image.clone() as left_eye:
    #             with self.current_image.clone() as right_eye:
    #                 with Image.stereogram(left=left_eye, right=right_eye) as img:
    #                     self.most_recent_image = img.clone()
    #                     self.most_recent_transformation = f""
    #                     GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
    #     except Exception as e:
    #         logger.error(e)
    #         GLib.idle_add(callback, None, None, get_ident())

    def swirl(self, callback, args):
        logger.debug(f'swirl {get_ident()}')
        time.sleep(0.25)
        angle = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.swirl(degree=angle)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"swirl(degree={angle})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def tint(self, callback, args):
        logger.debug(f'tint {get_ident()}')
        time.sleep(0.25)
        color, r, g, b = args
        alpha = f"rgb({r},{g},{b}"
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.tint(color=color, alpha=alpha)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"tint(color={color}, alpha={alpha})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def vignette(self, callback, args):
        logger.debug(f'vignette {get_ident()}')
        time.sleep(0.25)
        r, s, x, y = args
        logger.debug(f'vignette {r}, {s}, {x}, {y}')
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.vignette(radius=r, sigma=s, x=x, y=y)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"vignette(radius={r}, sigma={s}, x={x}, y={y})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def wave(self, callback, args):
        logger.debug(f'wave {get_ident()}')
        time.sleep(0.25)
        amplitude, wave_length, m = args
        method_map = {
            0: 'undefined',
            1: 'average',
            2: 'average9',
            3: 'average16',
            4: 'background',
            5: 'bilinear',
            6: 'blend',
            7: 'catrom',
            8: 'integer',
            9: 'mesh',
            10: 'nearest',
            11: 'spline'
        }
        method = method_map[m]

        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                
                img.wave(amplitude=img.height/amplitude, wave_length=img.width/wave_length, method=method)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"wave(amplitude={img.height/amplitude}, wave_length={img.width/wave_length}, method={method})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def wavelet_denoise(self, callback, args):
        logger.debug(f'wavelet_denoise {get_ident()}')
        time.sleep(0.25)
        t, s = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.wavelet_denoise(threshold=t*img.quantum_range, softness=s)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"wavelet_denoise(threshold={t*img.quantum_range}, softness={s})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def enhance(self, callback, _args):
        logger.debug(f'enhance {get_ident()}')
        time.sleep(0.25)
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.enhance()
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"enhance"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def flip(self, callback, _args):
        logger.debug(f'flip {get_ident()}')
        time.sleep(0.25)
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.flip()
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"flip"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def flop(self, callback, _args):
        logger.debug(f'flop {get_ident()}')
        time.sleep(0.25)
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.flop()
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"flop"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def rotate(self, callback, args):
        logger.debug(f'rotate {get_ident()}')
        time.sleep(0.25)
        angle, color= args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.rotate(degree=angle, background=color)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"rotate"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def statistic(self, callback, args):
        logger.debug(f'statistic {get_ident()}')
        time.sleep(0.25)
        m, width, height  = args
        method_map = {
            0: 'gradient',
            1: 'maximum',
            2: 'mean',
            3: 'median',
            4: 'minimum',
            5: 'mode',
            6: 'nonpeak',
            7: 'root_mean_square',
            8: 'standard_deviation'
        }
        method = method_map[m]

        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.statistic(stat=method, width=width, height=height)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"statistic(stat={method}, width={width}, height={height})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def kmeans(self, callback, args):
        logger.debug(f'rotate {get_ident()}')
        time.sleep(0.25)
        c, i, t= args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.kmeans(number_colors=c, max_iterations=i, tolerance=t)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"kmeans(number_colors={c}, max_iterations={i}, tolerance={t})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def posterize(self, callback, args):
        logger.debug(f'posterize {get_ident()}')
        time.sleep(0.25)
        levels, d  = args
        dither_map = {
            0: 'undefined',
            1: 'no',
            2: 'riemersma',
            3: 'floyd_steinberg'
        }
        dither = dither_map[d]

        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.posterize(levels=levels, dither=dither)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"posterize(levels={levels}, dither={dither})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def quantize(self, callback, args):
        logger.debug(f'quantize {get_ident()}')
        time.sleep(0.25)
        c, t, tree, d, m  = args

        if type(d) != bool:
            dither_map = {
                0: 'undefined',
                1: 'no',
                2: 'riemersma',
                3: 'floyd_steinberg'
            }
            dither = dither_map[d]
        else:
            dither = d

        colorspace_map = {
            0: 'undefined',
            1: 'rgb',
            2: 'gray',
            3: 'transparent',
            4: 'ohta',
            5: 'lab',
            6: 'xyz',
            7: 'ycbcr',
            8: 'ycc',
            9: 'yiq',
            10: 'ypbpr',
            11: 'yuv',
            12: 'cmyk',
            13: 'srgb',
            14: 'hsb',
            15: 'hsl',
            16: 'hwb',
            17: 'rec601ycbcr',
            18: 'rec709ycbcr',
            19: 'log',
            20: 'cmy',
            21: 'luv',
            22: 'hcl',
            23: 'lch',
            24: 'lms',
            25: 'lchab',
            26: 'lchuv',
            27: 'scrgb',
            28: 'hsi',
            29: 'hsv',
            30: 'hclp',
            31: 'xyy',
            32: 'ydbdr'
        }
        colorspace_type = colorspace_map[t]

        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.quantize(number_colors=c, colorspace_type=colorspace_type, treedepth=tree, dither=dither, measure_error=m)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"quantize(number_colors={c}, colorspace_type={colorspace_type}, treedepth={tree}, dither={dither}, measure_error={m})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())


    def adaptive_threshold(self, callback, args):
        logger.debug(f'adaptive_threshold {get_ident()}')
        time.sleep(0.25)
        w, h, o= args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.adaptive_threshold(width=w, height=h, offset=o * img.quantum_range)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"daptive_threshold(width={w}, height={h}, offset={o * img.quantum_range})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def auto_threshold(self, callback, args):
        logger.debug(f'auto_threshold {get_ident()}')
        time.sleep(0.25)
        m = args 
        method_map = {
            0: 'undefined',
            1: 'kapur',
            2: 'otsu',
            3: 'triangle'
        }
        method = method_map[m]
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.auto_threshold(method=method)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"auto_threshold(method={method})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def black_threshold(self, callback, args):
        logger.debug(f'black_threshold {get_ident()}')
        time.sleep(0.25)
        c = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.black_threshold(threshold=c)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"black_threshold(threshold={c})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def color_threshold(self, callback, args):
        logger.debug(f'color_threshold {get_ident()}')
        time.sleep(0.25)
        start, stop = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.color_threshold(start=start, stop=stop)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"color_threshold(start={start}, stop={stop})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def ordered_dither(self, callback, args):
        logger.debug(f'ordered_dither {get_ident()}')
        time.sleep(0.25)
        m = args
        dither_map = {
            0: 'threshold',
            1: 'checks',
            2: 'o2x2',
            3: 'o3x3',
            4: 'o4x4',
            5: 'o8x8',
            6: 'h4x4a',
            7: 'h6x6a',
            8: 'h8x8a',
            9: 'h4x4o',
            10: 'h6x6o',
            11: 'h8x8o',
            12: 'h16x16o',
            13: 'c5x5b',
            14: 'c5x5w',
            15: 'c6x6b',
            16: 'c6x6w',
            17: 'c7x7b',
            18: 'c7x7w',
        }
        dither = dither_map[m]
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.ordered_dither(threshold_map=dither)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"ordered_dither(threshold_map={dither})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def random_threshold(self, callback, args):
        logger.debug(f'random_threshold {get_ident()}')
        time.sleep(0.25)
        l, h = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.random_threshold(low=l, high=h)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"random_threshold(low={l}, high={h})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def range_threshold(self, callback, args):
        logger.debug(f'range_threshold {get_ident()}')
        time.sleep(0.25)
        lb, lw, hw, hb= args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.range_threshold(low_black=lb, low_white=lw, high_white=hw, high_black=hb)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"range_threshold(low_black={lb}, low_white={lw}, high_white={hw}, high_black={hb})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def white_threshold(self, callback, args):
        logger.debug(f'white_threshold {get_ident()}')
        time.sleep(0.25)
        c = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.white_threshold(threshold=c)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"white_threshold(threshold={c})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())

    def fx(self, callback, args):
        logger.debug(f'fx {get_ident()}')
        time.sleep(0.25)
        c = args
        logger.debug(self.uri)
        if self.current_image == None:
            logger.debug('current none')
        try:
            with self.current_image.clone() as img:
                img.fx(expression=c)
                self.most_recent_image = img.clone()
                self.most_recent_transformation = f"fx(expression={c})"
                GLib.idle_add(callback, img.make_blob(format='rgb'), img.size, get_ident())
        
        except Exception as e:
            logger.error(e)
            GLib.idle_add(callback, None, None, get_ident())