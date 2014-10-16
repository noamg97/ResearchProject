os.environ['LANG'] = 'en_US'
from gi.repository import Gtk, Gdk, GObject, GLib, GdkPixbuf
GObject.threads_init()


class ChatWidget(Gtk.VPaned):
    def __init__(self, friend_chat_data):
        Gtk.VPaned.__init__(self, width_request=450, height_request=350)
        
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
        
        send_btn = Gtk.Button("Send", halign=0, width_request=50, height_request=50)
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