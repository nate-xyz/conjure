from gi.repository import Adw, Gtk

from loguru import logger

@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/quantize.ui')
class Quantize(Adw.Bin):
    __gtype_name__ = 'Quantize'

    dither_dropdown = Gtk.Template.Child('dither_dropdown')
    colorspace_dropdown = Gtk.Template.Child('colorspace_dropdown')

    levels_spin = Gtk.Template.Child('levels_spin')
    levels_adj = Gtk.Template.Child('levels_adj')

    tree_depth_spin = Gtk.Template.Child('tree_depth_spin')
    tree_depth_adj = Gtk.Template.Child('tree_depth_adj')

    #error_check = Gtk.Template.Child('error_check')

    def __init__(self, job_callback, levels=None, tree_depth=None) -> None:
        super().__init__()

        if levels != None:
            self.levels_adj.set_value(levels)
        
        if tree_depth != None:
            self.tree_depth_adj.set_value(tree_depth)

        self.dither_dropdown.set_selected(2)
        self.colorspace_dropdown.set_selected(13)

        self.levels = int(self.levels_spin.get_value())
        self.colorspace = self.colorspace_dropdown.get_selected()
        self.tree_depth = int(self.tree_depth_spin.get_value())
        self.dither = self.dither_dropdown.get_selected()

        #self.error = self.error_check.get_active()
        self.error = False

        self.levels_spin.connect('value-changed', self.on_spin_change)
        self.tree_depth_spin.connect('value-changed', self.on_spin_change)
        self.colorspace_dropdown.connect('notify::selected', lambda dropdown, _value: self.on_dropdown_change(dropdown))
        self.dither_dropdown.connect('notify::selected', lambda dropdown, _value: self.on_dropdown_change(dropdown))
        #self.error_check.connect('toggled', self.toggled)

        self.start_job = job_callback
        self.start_job(self.levels, self.colorspace, self.tree_depth, self.dither, self.error)

    def on_spin_change(self, spin):
        value = spin.get_value()
        logger.debug(value)

        match spin:
            case self.levels_spin:
                self.levels = int(value)
            case self.tree_depth_spin:
                self.tree_depth = int(value)

        self.start_job(self.levels, self.colorspace, self.tree_depth, self.dither, self.error)
            
    def on_dropdown_change(self, dropdown):
        value = dropdown.get_selected()

        match dropdown:
            case self.colorspace_dropdown:
                self.colorspace = int(value)
            case self.dither_dropdown:
                self.dither = int(value)

        self.start_job(self.levels, self.colorspace, self.tree_depth, self.dither, self.error)

    # def toggled(self, check):
    #     self.error = check.get_active()
    #     self.start_job(self.levels, self.colorspace, self.tree_depth, self.dither, self.error)
