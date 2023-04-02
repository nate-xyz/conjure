# app.py
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

from gi.repository import Gio, Gtk, Adw

from loguru import logger

from conjure.window import Window
from .magic import Magic

class App(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.nate_xyz.Conjure',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        self.setup_actions()
        self.magic = Magic()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = Window(application=self)
        win.present()

    def setup_actions(self):
        self.create_action('quit', self.quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        
    def on_about_action(self):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Conjure',
                                application_icon='io.github.nate_xyz.Conjure',
                                developer_name='nate-xyz',
                                version='0.1.2',
                                developers=['nate-xyz'],
                                copyright='© 2023 nate-xyz',
                                license_type=Gtk.License.GPL_3_0_ONLY,
                                website='https://github.com/nate-xyz/conjure',
                                issue_url='https://github.com/nate-xyz/conjure/issues',
        )

        # Translator credits. Replace "translator-credits" with your name/username, and optionally an email or URL. 
        # One name per line, please do not remove previous names.
        about.set_translator_credits(_("translator-credits"))

        # Translators: just translate "Powered by"
        ack =  _("Powered by ImageMagick")+""
        about.add_acknowledgement_section(
            ack,
            [
                "Wand https://github.com/emcconville/wand",
                "ImageMagick https://imagemagick.org/index.php",
            ]
        )

        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        logger.debug('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", lambda _widget, _parameter: callback())
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

