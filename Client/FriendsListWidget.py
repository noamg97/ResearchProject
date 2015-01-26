import Shared
from math import pi
import os
os.environ['LANG'] = 'en_US'
from gi.repository import Gtk, Gdk, GObject, GLib, GdkPixbuf
GObject.threads_init()


class FriendsListWidget(Gtk.EventBox):
    def __init__(self):
        Gtk.EventBox.__init__(self)
        self.selected_box = None
        
        self.brother_list = None
        
        con = Gtk.VBox(0, False)
        self.main_box = Gtk.VBox(5, True, name='FriendsList', vexpand=False)
        con.pack_start(self.main_box, False, False, 0)
        
        self.connect("button-press-event", self.friends_list_clear_selection)
        self.add(con)
        self.show_all()
        
    def append(self, name_to_show, show_indicator=True):
        frame = Gtk.Frame(vexpand=False)
        box = Gtk.HBox(False, 0, vexpand=False)
        frame.add(box)
        
        button = Gtk.Button(name_to_show, xalign=0, margin_left=15)
        button.connect('clicked', self.friends_list_selection_changed)
        box.pack_start(button, True, True, 0)
        
        if show_indicator:
            state_ind = Gtk.DrawingArea(name='offline', margin_right=15, width_request=15, height_request=15)
            state_ind.connect('draw', FriendsListWidget.draw_friend_state)

        
        box.pack_start(state_ind, False, False, 0)
        frame.show_all()
        
        self.main_box.pack_start(frame, False, False, 0)

    def friends_list_selection_changed(self, widget, data=None):
        user = widget.props.label
        
        if self.selected_box:
            self.selected_box.set_name("unselected_friend")
        self.selected_box = widget.get_parent().get_parent()
        self.selected_box.set_name("selected_friend")

        if not data:
            if not Shared.main_window.current_chat_window is Shared.main_window.chat_windows[user]:
                if Shared.main_window.current_chat_window:
                    Shared.main_window.current_chat_window.hide()
                Shared.main_window.chat_windows[user].show_all()
                Shared.main_window.current_chat_window = Shared.main_window.chat_windows[user]
                Shared.main_window.current_chat_window_username = user
            self.brother_list.select_by_username(user)

    def friends_list_clear_selection(self, widget, event, hide_current_chat=True):
        if self.selected_box:
            self.selected_box.set_name("unselected_friend")
            
        if hide_current_chat:
            if Shared.main_window.current_chat_window:
                Shared.main_window.current_chat_window.hide()
            Shared.main_window.current_chat_window = None
            Shared.main_window.current_chat_window_username = None
            self.brother_list.friends_list_clear_selection(None, None, False)
    
    def select_by_username(self, username):
        for frame in self.main_box.get_children():
            btn = frame.get_child().get_children()[0]
            if username == btn.props.label:
                self.friends_list_selection_changed(btn, True)
                return
        self.friends_list_clear_selection(None, None, False)
    
    @staticmethod
    def draw_friend_state(drawing_area, cr):
        state = drawing_area.get_name().lower()

        cr.arc(drawing_area.get_allocated_width()/2, drawing_area.get_allocated_height()/2, drawing_area.get_allocated_width()*0.4, 0.0, 2.0 * pi)
        cr.set_source_rgba(1,1,1,1)
        cr.set_line_width(2.5)
        cr.stroke()
        
        if state == 'offline': cr.set_source_rgba  (52/255.0,  49/255.0,   49/255.0,   1.0)
        elif state == 'online': cr.set_source_rgba (5/255.0,   198/255.0,  0,          1.0)
        elif state == 'afk': cr.set_source_rgba    (1,         172/255.0,  0,          1.0)
        elif state == 'busy': cr.set_source_rgba   (200/255.0, 0,          0,          1.0)
        else: cr.set_source_rgba(1, 1, 1,1)
        
        cr.arc(drawing_area.get_allocated_width()/2, drawing_area.get_allocated_height()/2, drawing_area.get_allocated_width()*0.4, 0.0, 2.0 * pi)
        cr.fill()

    def friend_state_changed(self, username, state):
        for box in [frame.get_children()[0] for frame in self.main_box.get_children()]:
            btn, state_area = box.get_children()
            if btn.props.label == username:
                state_area.set_name(state)
                state_area.queue_draw()
                break