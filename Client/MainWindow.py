import UserInputParser
import Shared
import os
import Queue
from datetime import datetime
from math import pi
os.environ['LANG'] = 'en_US'
from gi.repository import Gtk, Gdk, GObject, GLib
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
        
        
        notebook_frame = Gtk.Frame(name='notebook_frame')
        notebook_frame.set_size_request(250,350)
        hpaned.pack1(notebook_frame, resize=False, shrink=False)
        notebook = Gtk.Notebook()
        notebook.set_scrollable(True)
        notebook.popup_disable()
        notebook_frame.add(notebook)
        
        self.flist = FriendsListWidget()
        for f in Shared.friends_list:
            self.append_friend(f.data.username)
            
        notebook.append_page(self.flist, Gtk.Label('3Heads'))
        

        
        friend_requests_container = Gtk.VBox(True, 4)
        notebook.append_page(friend_requests_container, Gtk.Label('Head+'))
        
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


        self.show_all()
        self.load_chat_data()
        

        GObject.timeout_add(100, self.update)

        
        
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
            friend = Shared.get_friend_by_username(self.current_chat_window_username)
            if friend:
                if self.current_chat_window.textbuffer.get_char_count():
                    start, end = self.current_chat_window.textbuffer.get_bounds()
                    friend.message(self.current_chat_window.textbuffer.get_text(start, end, True))
                    self.current_chat_window.textbuffer.delete(start, end)
        return True
        
    def load_chat_data(self):
        for friend in Shared.friends_list:
            self.chat_windows[friend.data.username].append_multiple(friend.data.chat_data)
            self.chat_windows[friend.data.username].hide()
            
    def append_chat_message(self, username, msg):
        self.chat_windows[username].append(msg, self.chat_windows[username] is self.current_chat_window)
  
    def append_friend(self, username):
        self.flist.append(username)
        self.chat_windows[username] = ChatWidget([])
        self.chat_side.pack_start(self.chat_windows[username], True, True, 0)

    def friend_state_changed(self, username, state):
        self.flist.friend_state_changed(username, state)
    
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
        
        
class ChatWidget(Gtk.VPaned):
    def __init__(self, friend_chat_data):
        Gtk.VPaned.__init__(self)
        self.set_size_request(450, 350)
        
        self.chat_scroller = Gtk.ScrolledWindow()
        self.chat_scroller.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.chat_scroller.set_shadow_type(Gtk.ShadowType.NONE)
        self.pack1(self.chat_scroller, resize=True, shrink=False)
        
        chat = Gtk.VBox(False, 0)
        self.chat_scroller.add(chat)
        
        lower_chat = Gtk.HBox(False, 0)
        self.pack2(lower_chat, resize=False, shrink=False)

        textview = Gtk.TextView()
        textview.connect("key-press-event", self.key_event)
        self.textbuffer = textview.get_buffer()
        lower_chat.pack_start(textview, True, True, 0)
        
        send_btn = Gtk.Button("Send", halign=0)
        send_btn.set_size_request(50,50)
        send_btn.connect("clicked", main_win.send)
        lower_chat.pack_start(send_btn, False, False, 0)
        
        
        chat_frame = Gtk.Frame(name='chat_widget_frame')
        self.chat_widget = Gtk.Grid()
        self.chat_widget.set_row_spacing(5)
        self.chat_widget.set_column_spacing(50)
        chat_frame.add(self.chat_widget)
        
        for msg in friend_chat_data:
            self.append(msg)
        
        
        chat.add(chat_frame)
    
    def append(self, message, show=False):
        author_lbl = Gtk.Label(str(message.author), halign=Gtk.Align.START, selectable=True)
        time_lbl = Gtk.Label(datetime.strftime(message.time, '%H:%M'), halign=Gtk.Align.START, selectable=True)
        content_lbl = Gtk.Label(str(message.content), halign=Gtk.Align.START, selectable=True, hexpand=True, wrap=True, wrap_mode=2)

        if show:
            author_lbl.show()
            time_lbl.show()
            content_lbl.show()
        
        self.chat_widget.attach_next_to(author_lbl, None, Gtk.PositionType.BOTTOM, 1, 1)
        self.chat_widget.attach_next_to(content_lbl, author_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.chat_widget.attach_next_to(time_lbl, content_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        
    def append_multiple(self, message_list):
        for msg in message_list:
            self.append(msg)
    
    def key_event(self, widget, ev, data=None):
        if ev.keyval == 65293:
            main_win.send(None)
            return True
        return False
        
        
class FriendsListWidget(Gtk.EventBox):
    def __init__(self):
        Gtk.EventBox.__init__(self)
        self.selected_box = None
        
        con = Gtk.VBox(0, False)
        self.main_box = Gtk.VBox(5, True, name='FriendsList', vexpand=False)
        con.pack_start(self.main_box, False, False, 0)
        
        self.connect("button-press-event", self.friends_list_clear_selection)
        self.add(con)
        self.show_all()
        
    def append(self, username):
        frame = Gtk.Frame(vexpand=False)
        box = Gtk.HBox(False, 0, vexpand=False)
        frame.add(box)
        
        button = Gtk.Button(username, xalign=0, margin_left=15)
        button.connect('clicked', self.friends_list_selection_changed)
        box.pack_start(button, True, True, 0)
        
        state_ind = Gtk.DrawingArea(name='offline', margin_right=15)
        state_ind.set_size_request(15, 15)
        state_ind.connect('draw', self.draw_friend_state)

        
        box.pack_start(state_ind, False, False, 0)
        frame.show_all()
        
        self.main_box.pack_start(frame, False, False, 0)
    

    def friends_list_selection_changed(self, widget, data=None):
        user = widget.props.label
        
        if self.selected_box:
            self.selected_box.set_name("unselected_friend")
        self.selected_box = widget.get_parent().get_parent()
        self.selected_box.set_name("selected_friend")
            
        if not main_win.current_chat_window is main_win.chat_windows[user]:
            if main_win.current_chat_window:
                main_win.current_chat_window.hide()
            main_win.chat_windows[user].show_all()
            main_win.current_chat_window = main_win.chat_windows[user]
            main_win.current_chat_window_username = user

    def friends_list_clear_selection(self, widget, event, data=None):
        if self.selected_box:
            self.selected_box.set_name("unselected_friend")
            
        if main_win.current_chat_window:
            main_win.current_chat_window.hide()
        main_win.current_chat_window = None
        main_win.current_chat_window_username = None

    def draw_friend_state(self, drawing_area, cr):
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
        print 1
        for box in self.main_box.get_children()[0].get_children():
            print 2
            btn, state_area = box.get_children()
            if btn.props.label == username:
                print 3
                state_area.set_name(state)
                state_area.queue_draw()
                break