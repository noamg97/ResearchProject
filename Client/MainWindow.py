import UserInputParser
from gi.repository import Gtk, Gdk, GObject
GObject.threads_init()


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL, title="Whoosh")
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.destroy)
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
        chat_side.set_name('chat_side')
        hpaned.pack1(chat_side, resize=True, shrink=False)
        
        chat_scroller = Gtk.ScrolledWindow()
        chat_scroller.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        chat_scroller.set_shadow_type(Gtk.ShadowType.NONE)
        chat_side.pack1(chat_scroller, resize=True, shrink=False)
        
        self.chat = Gtk.TextView()
        self.chat.set_editable(False)
        self.chat.set_cursor_visible(False)
        chat_scroller.add(self.chat)
        
        lower_chat = Gtk.HBox(False, 0)
        lower_chat.set_name('lower_chat')
        chat_side.pack2(lower_chat, resize=False, shrink=False)

        
        send_btn = Gtk.Button("Send", halign=0)
        send_btn.set_name('send_btn')
        send_btn.set_size_request(50,50)
        send_btn.connect("clicked", self.send, False)
        lower_chat.pack_start(send_btn, False, False, 0)
        
        self.textbox = Gtk.TextView()
        lower_chat.pack_start(self.textbox, True, True, 0)

        flist_scroller = Gtk.ScrolledWindow()
        flist_scroller.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        flist_scroller.set_shadow_type(Gtk.ShadowType.NONE)
        flist_scroller.set_size_request(200, 350)
        vp = Gtk.Viewport()
        vp.set_shadow_type(Gtk.ShadowType.NONE)
        hpaned.pack2(flist_scroller, resize=True, shrink=False)
        
        flist = Gtk.TreeView()
        flist.set_name('flist')
        selection = flist.get_selection()
        selection.connect("changed", self.friends_list_selection_changed)
        vp.add(flist)
        flist_scroller.add(vp)
        
        self.show_all()
        
    def send(self, widget, data=None):
        print 'send'
    
    def friends_list_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print "You selected", model[treeiter][0]
        
    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False
        
    def destroy(self, widget, data=None):
        Gtk.main_quit()
        
    def main(self):
        Gtk.main()