import UserInputParser
import Shared
import os
os.environ['LANG'] = 'en_US'
from gi.repository import Gtk, Gdk, GObject, GLib
GObject.threads_init()

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL, title="Whoosh - "+Shared.my_data.username)
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.destroy_event)
        self.set_default_size(850, 500)
        #self.set_decorated(False)
        
        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('StyleSheet.css')
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
        
        hpaned = Gtk.HPaned()
        self.add(hpaned)
        
        chat_side = Gtk.VPaned()
        chat_side.set_size_request(450, 350)
        hpaned.pack2(chat_side, resize=True, shrink=False)
        
        chat_scroller = Gtk.ScrolledWindow()
        chat_scroller.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        chat_scroller.set_shadow_type(Gtk.ShadowType.NONE)
        chat_side.pack1(chat_scroller, resize=True, shrink=False)
        
        self.chat = Gtk.TextView()
        self.chat.set_editable(False)
        self.chat.set_cursor_visible(False)
        chat_scroller.add(self.chat)
        
        lower_chat = Gtk.HBox(False, 0)
        chat_side.pack2(lower_chat, resize=False, shrink=False)

        self.textbox = Gtk.TextView()
        lower_chat.pack_start(self.textbox, True, True, 0)
        
        send_btn = Gtk.Button("Send", halign=0)
        send_btn.set_size_request(50,50)
        send_btn.connect("clicked", self.send, False)
        lower_chat.pack_start(send_btn, False, False, 0)
        
        notebook_frame = Gtk.Frame()
        notebook_frame.set_size_request(250,350)
        notebook_frame.set_name('notebook_frame')
        hpaned.pack1(notebook_frame, resize=False, shrink=False)
        notebook = Gtk.Notebook()
        notebook.set_scrollable(True)
        notebook.popup_disable()
        notebook_frame.add(notebook)
        
        
        self.friend_store = Gtk.ListStore(str)

        for f in Shared.friends_list:
            self.append_friend(f.data.username)
        
        flist_box = Gtk.VBox(False, 10)
        flist = Gtk.TreeView(self.friend_store)
        flist.set_name('flist')
        flist.set_headers_visible(False)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Friends", renderer, text=0)
        column.set_spacing(50)
        flist.append_column(column)
        selection = flist.get_selection()
        selection.connect("changed", self.friends_list_selection_changed)
        flist_box.pack_start(flist, False, False, 10)
        
        
        notebook.append_page(flist_box, Gtk.Label('3Heads'))
        
        
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
        
        #self.anim_counter = 0
        #self.anim_done = False
        #hpaned.set_position(0)
        #print 'pos2 ', hpaned.get_position()
        #hpaned.connect('notify::position', self.hpaned_move, flist_scroller.get_size_request()[0])
        #GLib.timeout_add(1000.0/60, self.animate_flist, hpaned, 1000, 1000.0/60,  flist_scroller.get_size_request()[0])
        
    def send(self, widget, data=None):
        print 'send'
     
    def send_friend_request(self, widget, data=None):
        name = data.get_text()
        if name:
            UserInputParser.send_friend_request(name)
    
    def append_frequest(self, username):
        self.in_frequests_box.pack_end(NewFriendRequestBox(username), False, False, 4)
    
    def append_friend(self, username):
        itr = self.friend_store.append([username])
        self.friend_store.set(itr, [0], [username])
    
    
    
    
    def friends_list_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print "You selected", model[treeiter][0]
            
    #def animate_flist(self, paned, total_time, interval, end_pos):
    #    self.anim_counter+=1
    #    paned.set_position(round(end_pos * (self.anim_counter * interval / total_time)))
    #    
    #    print 'pos ', paned.get_position()
    #    if self.anim_counter*interval >= total_time:
    #        self.anim_done = True
    #        return False
    #    return True

    #def hpaned_move(self, widget, what, data):
    #    if self.anim_done and widget.props.position <= int(data):
    #        print 'false'
    #        return False
    #    return True
        
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
        self.show()
        name.show()
        acc.show()
        dec.show()
    
    def accept_click(self, widget, user):
        UserInputParser.accept_friend_request(user)
        self.destroy()
        
    def decline_click(self, widget, user):
        UserInputParser.decline_friend_request(user)
        self.destroy()