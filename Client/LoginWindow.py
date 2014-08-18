import Shared
from MyData import MyData
import os
os.environ['LANG'] = 'en_US'
from gi.repository import Gtk, Gdk, GObject
GObject.threads_init()

class LoginWindow(Gtk.Window):
    def __init__(self):
        self._continue = False
        succeeded = MyData.load_login_data()
        if succeeded:
            self.login(None, True)
            
        else:
            Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL, title="Login")
            self.connect("delete_event", self.delete_event)
            self.connect("destroy", self.destroy_event)
            self.set_border_width(10)
            
            self.connect("key_press_event", self.key_event)
            
            screen = Gdk.Screen.get_default()
            css_provider = Gtk.CssProvider()
            css_provider.load_from_path('StyleSheet.css')
            context = Gtk.StyleContext()
            context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

            
            self.vbox = Gtk.VBox(False, 0)
            self.add(self.vbox)
            
            self.username_box = Gtk.HBox(False, 0)
            self.vbox.pack_start(self.username_box, False, False, 0)
            self.username_lbl = Gtk.Label("Username: ")
            self.username_box.pack_start(self.username_lbl, False, False, 0)
            self.username_tbox = Gtk.Entry()
            self.username_box.pack_start(self.username_tbox, True, True, 0)
            
            
            self.pass_box = Gtk.HBox(False, 0)
            self.vbox.pack_start(self.pass_box, False, False, 10)
            self.pass_lbl = Gtk.Label("Password:  ")
            self.pass_box.pack_start(self.pass_lbl, False, False, 0)
            self.pass_tbox = Gtk.Entry()
            self.pass_tbox.set_visibility(False)
            self.pass_box.pack_start(self.pass_tbox, True, True, 0)
            
            
            self.login_btn = Gtk.Button("Login")
            self.login_btn.connect("clicked", self.login, False)
            self.vbox.pack_start(self.login_btn, False, False, 5)
            
            self.create_btn = Gtk.Button("Create")
            self.create_btn.connect("clicked", self.create, None)
            self.vbox.pack_start(self.create_btn, False, False, 0)
            
            self.show_all()
        
    def login(self, widget, is_from_saved_data):
        if is_from_saved_data:
            username = Shared.my_data.username
            password = Shared.my_data.password
            state = Shared.my_data.state
        else:
            username = self.username_tbox.get_text()
            password = self.pass_tbox.get_text()
            state = 1
            
        #TODO: add user input validations.
        if not username or not password: return
        
        
        if Shared.server.send_login_request(username, password, state):
            if not is_from_saved_data:
                Shared.my_data = MyData(username, password, 1)
            self._continue = True
            self.destroy()
        else:
            #show some label saying login declined
            pass
            
    def create(self, widget, data=None):
        username = self.username_tbox.get_text()
        password = self.pass_tbox.get_text()
        #TODO: add user input validations.
        
        if Shared.server.send_create_user_request(username, password):
            Shared.my_data = MyData(username, password, 1)
            self._continue = True
            self.destroy()
        else:
            #show some label saying login declined
            pass
        
    def key_event(self, widget, ev, data=None):
        if ev.keyval == 65293: #apparently enter
            print 'enter pressed'
            self.login(widget, False)
    
    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False
        
    def destroy_event(self, widget, data=None):
        #destructor
        Gtk.main_quit()
        
    def main(self):
        Gtk.main()
        return self._continue