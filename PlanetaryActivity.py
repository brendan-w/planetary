


# Sugar Imports
from sugar3.activity.activity import Activity
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ActivityButton


# Gtk Import
from gi.repository import Gtk
from gettext import gettext as _

import Planetary


class PlanetaryActivity(Activity):
    def __init__(self, sugar_handle):
        Activity.__init__(self, sugar_handle)

        
        # Create a Toolbar
        toolbar = Gtk.Toolbar()

        # Add toolbar to Sugar Activity Toolbar Space
        self.set_toolbar_box(toolbar)

        # Add Activity Button
        toolbar.insert(ActivityButton(self), -1)

        # Create & Add Separator
        separator = Gtk.SeparatorToolItem(draw=False)
        separator.set_expand(True)
        toolbar.insert(separator, -1)

        # Add Stop Button
        toolbar.insert(StopButton(self), -1)

        

        # Create Container
        grid = Gtk.Grid()

        # Add grid to Sugar Activity GtkWindow
        self.set_canvas(grid)

        # Create & Add Label
        label = Gtk.Label(label=_("Name: "))
        grid.attach(label, 0, 0, 1, 1)

        # Add Output Label
        output = Gtk.Label()
        grid.attach(output, 1, 1, 1, 1)

        # Create & Add Text Entry
        entry = Gtk.Entry()
        grid.attach(entry, 0, 1, 1, 1)

        # Empty output on keypress in entry
        entry.connect('key-release-event', self.emptyout, output)

        # Add a button
        button = Gtk.Button(label=_("Greet!"))
        grid.attach(button, 0, 2, 1, 1)

        # Tell the button to run a class method
        button.connect('clicked', self.greeter, entry, output)

        # Show all components (otherwise none will be displayed)
        self.show_all()

    def greeter(self, button, entry, output):
        if len(entry.get_text()) > 0:
            output.set_text("Hello " + entry.get_text() + "!")
        else:
            output.set_text("Please entry your name.")

    def emptyout(self, entry, event, output):
        output.set_text("")

        
    def read_file(self, file_path):
        pass

    def write_file(self, file_path):
        pass
