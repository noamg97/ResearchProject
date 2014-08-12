import Shared
from MyData import MyData
from gi.repository import Gtk, Gdk, GObject
GObject.threads_init()

class LoginWindow(Gtk.Window):
    def __init__(self):
        succeeded = MyData.load_login_data()
        if succeeded:
            self.login(None, True)
            
        else:
            Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL, title="Login")
            self.connect("delete_event", self.delete_event)
            self.connect("destroy", self.destroy)
            self.set_border_width(10)
            
            self.vbox = Gtk.VBox(False, 0)
            self.add(self.vbox)
            
            
            self.username_box = Gtk.HBox(False, 0)
            self.vbox.pack_start(self.username_box, False, False, 0)
            self.username_tbox = Gtk.Entry()
            self.username_box.pack_start(self.username_tbox, True, True, 0)
            self.username_lbl = Gtk.Label("Username: ")
            self.username_box.pack_start(self.username_lbl, False, False, 0)
            
            self.username_lbl.show()
            self.username_tbox.show()
            self.username_box.show()
            
            self.pass_box = Gtk.HBox(False, 0)
            self.vbox.pack_start(self.pass_box, False, False, 10)
            self.pass_tbox = Gtk.Entry()
            self.pass_tbox.set_visibility(False)
            self.pass_box.pack_start(self.pass_tbox, True, True, 0)
            self.pass_lbl = Gtk.Label("Password:  ")
            self.pass_box.pack_start(self.pass_lbl, False, False, 0)
            
            self.pass_lbl.show()
            self.pass_tbox.show()
            self.pass_box.show()
            
            self.login_btn = Gtk.Button("Login")
            self.login_btn.connect("clicked", self.login, False)
            self.vbox.pack_start(self.login_btn, False, False, 5)
            
            self.create_btn = Gtk.Button("Create")
            self.create_btn.connect("clicked", self.create, None)
            self.vbox.pack_start(self.create_btn, False, False, 0)
            
            self.vbox.show()
            self.login_btn.show()
            self.create_btn.show()
            self.show()
        
    def login(self, widget, data=None): #data for [is_from_saved_data]
        if not data:
            #TODO: add user input validations.
            Shared.my_data = MyData(self.username_tbox.get_text(), self.pass_tbox.get_text(), 1) #TODO: load state even if login details aren't available
        
        if Shared.server.send_login_request():
            self.destroy()
        else:
            #show some label saying login declined
            pass
            
    def create(self, widget, data=None):
        #TODO: add user input validations
        
        Shared.my_data = MyData(self.username_tbox.get_text(), self.pass_tbox.get_text(), 1)
        
        if Shared.server.send_create_user_request():
            self.destroy()
        else:
            #show some label saying user creation declined
            pass
        
    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False
        
    def destroy(self, widget, data=None):
        #destructor
        Gtk.main_quit()
        
    def main(self):
        Gtk.main()