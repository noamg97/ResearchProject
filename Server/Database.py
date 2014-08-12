import sqlite3 as sql
import threading

class ThreadSafeDatabase:
    def __init__(self, database):
        self.db = database
        self.cursor = self.db.cursor()
        self.lock = threading.Lock()

    def execute(self, query, arguments=None, fetch=False, commit=False):
        self.lock.acquire()
        
        try:
            if not arguments:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, arguments)
            if fetch:
                result = self.cursor.fetchall()
        
        except Exception as exception: 
            raise exception
        
        finally:
            if commit: self.db.commit()
            self.lock.release()
        
        if fetch: return result

    def close(self):
        self.db.close()
            
            
            
class Database(ThreadSafeDatabase):
    def __init__(self, users_sockets):
        ThreadSafeDatabase.__init__(self, sql.connect('database.db', check_same_thread=False))
        self.users_sockets = users_sockets
        self.execute('CREATE TABLE IF NOT EXISTS users(' \
        'username TEXT, pass TEXT, state INTEGER, friends_list TEXT, profile_data TEXT, queued_messages TEXT, sent_friend_requests TEXT)')
        
    def insert_new_user(self, username, password):
        self.execute('INSERT INTO users VALUES(?,?,?,?,?,?,?)', (username, password, 1, '', '', '', ''), commit=True)
        
    def get_fields(self, username, *fields):
        if not len(fields):
            raise Exception('No Fields Given')
            
        return self.execute("SELECT " + ','.join(fields) + " FROM users WHERE username=?", (username,), True)

    def get_list_from_field(self, username, field):
        return [x for x in self.get_fields(username, field)[0][0].split(';') if x != '']
    
    def set_field(self, username, field, value):
        self.execute('UPDATE users SET ' + field + '=:val WHERE username=:usr', {'val':value, 'usr':username}, commit=True)
        
    def append_to_field(self, username, field, to_append):
        self.execute('UPDATE users SET :field=:field||:msg WHERE username=:usr', {'field':field ,'msg':message + ';', 'usr':username}, commit=True)
    
    def remove_from_field(self, username, field, to_remove):
        self.set_field(username, field, ';'.join(self.get_list_from_field(username, field).remove(to_remove)))

    def does_user_exist(self, username):
        ret = self.execute('SELECT username FROM users WHERE username=?', (username,), True)
        return bool(ret)
    
    def validate_password(self, username, password):
        ret = self.execute('SELECT username FROM users WHERE username=:usr and pass=:pss', {'usr':username, 'pss':password}, True)
        return bool(ret)
        
        




