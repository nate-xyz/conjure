# window.py
#
# Copyright 2023 nate-xyz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio

import os
import html

from conjure.views import ImageDropPage
from .util import SUCCESS_GREEN, ERROR_RED, image_mime_types


@Gtk.Template(resource_path='/io/github/nate_xyz/Conjure/window.ui')
class Window(Adw.ApplicationWindow):
    __gtype_name__ = 'Window'

    toast_overlay = Gtk.Template.Child('toast_overlay')
    open_image_button = Gtk.Template.Child('open_image_button')
    image_drop_page = Gtk.Template.Child('image_drop_page')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = kwargs['application']
        self.magic = app.magic
        self.add_dialog()
        help_overlay = Gtk.Builder\
            .new_from_resource('/io/github/nate_xyz/Conjure/help-overlay.ui')\
            .get_object('help_overlay')
        self.set_help_overlay(help_overlay)
        self.setup_actions(app)
        self.saturate()

# SETUP

    def add_dialog(self):
        self.open_image_dialog = Gtk.FileChooserNative.new(title=_("Select an Image File"), 
                                                        parent=self, 
                                                        action=Gtk.FileChooserAction.OPEN, 
                                                        accept_label=_("Open Image"))

        f = Gtk.FileFilter()
        f.set_name(_("Image files"))
        for m in image_mime_types:
            f.add_mime_type(m)

        self.open_image_dialog.connect("response", self.open_response)
        self.open_image_dialog.add_filter(f)
        self.open_image_button.connect("clicked", lambda _button: self.open_image_dialog.show())
        self.image_drop_page.open_image_button.connect("clicked", lambda _button: self.open_image_dialog.show())

    def open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            image_uri = dialog.get_file().get_path()
            if self.image_drop_page.load_image(image_uri):
                self.open_image_toast(image_uri)
            else:
                self.error_image_toast(image_uri)

    def setup_actions(self, app):
        app.set_accels_for_action("win.show-help-overlay", ['<Primary>question'])
        self.create_action(app, 'image-open', self.open_image_dialog.show, ['<Primary>o'])

    def saturate(self):
        self.image_drop_page.saturate(self, self.magic)

# TOAST MESSAGES

    def add_toast(self, title: str, timeout: int = 1):
        toast = Adw.Toast.new(html.escape(title))
        toast.set_timeout(timeout)
        self.toast_overlay.add_toast(toast)

    def add_toast_markup(self, title: str, timeout: int = 1):
        toast = Adw.Toast.new(title)
        toast.set_timeout(timeout)
        self.toast_overlay.add_toast(toast)

    def add_success_toast(self, verb: str, msg: str, timeout: int = 1):
        toast = Adw.Toast.new(f"<span foreground={SUCCESS_GREEN}>{verb}</span> {html.escape(msg)}")
        toast.set_timeout(timeout)
        self.toast_overlay.add_toast(toast)

    def add_error_toast(self, error: str, timeout: int = 1):
        # Translators: Only replace "Error!"
        toast = Adw.Toast.new(_(f"<span foreground={ERROR_RED}>Error!</span> {html.escape(error)}"))
        toast.set_timeout(timeout)
        self.toast_overlay.add_toast(toast)

    def open_image_toast(self, uri):
        base_name = html.escape(os.path.basename(uri))
        self.add_success_toast(_("Opened image:"), base_name)

    def error_image_toast(self, uri):
        base_name = os.path.basename(uri)
        # Translators: Do not replace {}
        self.add_error_toast(_("Could not open image: {}").format(base_name), 3)

    def create_action(self, app, name, callback=None, shortcuts=None):
        """Add a window action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        if callback != None:
            action.connect("activate", lambda _widget, _parameter: callback())
        self.add_action(action)
        if shortcuts:
            app.set_accels_for_action(f"win.{name}", shortcuts)