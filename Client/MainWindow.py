import UserInputParser
import Shared
import Paths
from Friend import StateCodes
import FriendsListWidget, ChatWidget
import os
import Queue
from datetime import datetime
from math import pi
os.environ['LANG'] = 'en_US'
from gi.repository import Gtk, Gdk, GObject, GLib, GdkPixbuf
GObject.threads_init()

main_win = None


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL, title="Whoosh - " + Shared.my_data.username)
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.destroy_event)
        self.set_default_size(850, 500)
        #self.set_decorated(False)
        
        self.calls = Queue.Queue()
        self.chat_windows = {}
        self.current_chat_window = None
        self.current_chat_window_username = None
        global main_win
        main_win = self
        
        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('StyleSheet.css')
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
        
        hpaned = Gtk.HPaned()
        self.add(hpaned)
        
        self.chat_side = Gtk.VBox()
        hpaned.pack2(self.chat_side, resize=True, shrink=False)
        
        left_side_frame = Gtk.Frame(name="left_side_frame")
        hpaned.pack1(left_side_frame, resize=False, shrink=False)
        left_side = Gtk.VBox(0, False)
        left_side_frame.add(left_side)
        
        state_store = Gtk.ListStore(str, GdkPixbuf.Pixbuf)
        for state in ['Online', 'AFK', 'Busy', 'Offline']:
            icn = GdkPixbuf.Pixbuf.new_from_file_at_size("images" + Paths.slash + "state_" + state.lower() + ".png", 14, 14)
            state_store.append([state, icn])

        state_box = Gtk.ComboBox.new_with_model(state_store)
        state_box.set_active(0)
        state_box.connect("changed", self.on_my_state_changed)
        
        renderer_text = Gtk.CellRendererText()
        state_box.pack_start(renderer_text, True)
        state_box.add_attribute(renderer_text, "text", 0)
        state_renderer = Gtk.CellRendererPixbuf()
        state_box.pack_start(state_renderer, False)
        state_box.add_attribute(state_renderer, "pixbuf", 1)

        
        username_and_state_box = Gtk.HBox(False, 0, name="username_and_state_box")
        username_and_state_box.pack_start(Gtk.Label(Shared.my_data.username), False, False, 10)
        username_and_state_box.pack_end(state_box, False, False, 10)
        left_side.pack_start(username_and_state_box, False, False, 10)
        
        
        notebook_frame = Gtk.Frame(name='notebook_frame', width_request=265, height_request=350)
        left_side.pack_start(notebook_frame, True, True, 0)
        
        notebook = Gtk.Notebook()
        notebook.set_scrollable(True)
        notebook.popup_disable()
        notebook_frame.add(notebook)
        
        self.contacts_list = FriendsListWidget()
        for f in Shared.friends_list:
            self.append_friend(f.username)
            
        

        
        friend_requests_container = Gtk.VBox(True, 4)
        friend_to_add_username_box = Gtk.VBox(False, 4)
        friend_requests_container.pack_start(friend_to_add_username_box, True, False, 0)
        username_lbl = Gtk.Label("\n\n\n\n\n\nFriend's Username:")
        friend_to_add_username_box.pack_start(username_lbl, False, False, 3)
        friend_to_add_username = Gtk.Entry()
        friend_to_add_username_box.pack_start(friend_to_add_username, False, False, 3)
        add_friend_btn = Gtk.Button("Send Friend Request")
        add_friend_btn.connect("clicked", self.send_friend_request, friend_to_add_username)
        friend_to_add_username_box.pack_start(add_friend_btn, False, False, 3)
        

        self.in_frequests_box = Gtk.VBox(True, 4)
        friend_requests_container.pack_start(self.in_frequests_box, True, False, 0)
        self.in_frequests_box.pack_start(Gtk.Label("New Friend Requests"), False, False, 4)

        
        
        self.active_chats = FriendsListWidget()
        
        self.active_chats.brother_list = self.contacts_list
        self.contacts_list.brother_list = self.active_chats
        
        
        notebook.append_page(self.active_chats, Gtk.Label('Active'))#Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size("images" + Paths.slash + "active_chats.png", 40, 40)))
        notebook.append_page(friend_requests_container, Gtk.Label('Friend Requests'))#Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size("images" + Paths.slash + "add_friend.png", 40, 40)))
        notebook.append_page(self.contacts_list, Gtk.Label('Contacts'))#Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size("images" + Paths.slash + "contacts.png", 40, 40)))

        
        self.show_all()
        self.load_chat_data()
        

        GObject.timeout_add(100, self.update)

    def draw_friend_state(self, drawing_area, cr):
        print 'got here'
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

        
    def update(self):
        while not self.calls.empty():
            items = self.calls.get()
            func = items[0]
            args = items[1:]
            func(*args)
        return True

        
    def send(self, widget, data=None):
        if data and data.keyval != 65293:
            return False
        if self.current_chat_window_username:
            if self.current_chat_window.textbuffer.get_char_count():
                start, end = self.current_chat_window.textbuffer.get_bounds()
                UserInputParser.send_message(   self.current_chat_window_username, 
                                                self.current_chat_window.textbuffer.get_text(start, end, True))
                self.current_chat_window.textbuffer.delete(start, end)
        return True
        
    def on_my_state_changed(self, statebox):
        tree_iter = statebox.get_active_iter()
        if tree_iter != None:
            model = statebox.get_model()
            state = model[tree_iter][0].lower()

            UserInputParser.state_changed(StateCodes.get_code_by_state(state))
    
    
    def load_chat_data(self):
        for friend in Shared.friends_list:
            self.chat_windows[friend.username].append_multiple(friend.data.chat_data)
            self.chat_windows[friend.username].hide()
            
            if any(friend.data.chat_data):
                self.active_chats.append(friend.username)
            
    def append_chat_message(self, username, msg):
        self.chat_windows[username].append(msg, self.chat_windows[username] is self.current_chat_window)
  
    def append_active_chat(self, chat_title):
        self.active_chats.append(chat_title)

    def append_friend(self, username):
        self.contacts_list.append(username)
        self.chat_windows[username] = ChatWidget([])
        self.chat_side.pack_start(self.chat_windows[username], True, True, 0)

    def friend_state_changed(self, username, state):
        self.contacts_list.friend_state_changed(username, state)
        self.active_chats.friend_state_changed(username, state)
    
    def send_friend_request(self, widget, data=None):
        name = data.get_text()
        if name:
            UserInputParser.send_friend_request(name)
    
    def append_frequest(self, username):
        self.in_frequests_box.pack_end(NewFriendRequestBox(username), False, False, 4)
    
    
    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False
        
    def destroy_event(self, widget, data=None):
        Gtk.main_quit()
        
    def main(self):
        Gtk.main()
        
        
class NewFriendRequestBox(Gtk.HBox):
    def __init__(self, username):
        Gtk.HBox.__init__(self, True, 5)
        name = Gtk.Label(username)
        acc = Gtk.Button('Accept')
        acc.connect('clicked', self.accept_click , username)
        dec = Gtk.Button('Decline')
        dec.connect('clicked', self.decline_click, username)
        self.pack_start(name, False, False, 4)
        self.pack_start(acc, False, False, 4)
        self.pack_start(dec, False, False, 4)
        self.show_all()
    
    def accept_click(self, widget, user):
        UserInputParser.accept_friend_request(user)
        self.destroy()
        
    def decline_click(self, widget, user):
        UserInputParser.decline_friend_request(user)
        self.destroy()
        
        
