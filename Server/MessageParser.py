from OpCodes import *

db = None
users_sockets = []

def init(_db, _users_sockets):
    global db, users_sockets
    db = _db
    users_sockets = _users_sockets
    
    
    #TODO: validate all the variables that are received from user
    
    
def parse(msg, username):
    if msg[:num_char] == user_state_changed:
        parse_user_state_changed(msg[num_char:], username)
        
    elif msg[:num_char] == connect_to_friend:
        parse_user_connecting_to_friend(msg[num_char:], username)
        
    elif msg[:num_char] == profile_data_changed:
        parse_user_profile_data_changed(msg[num_char:], username)
        
    elif msg[:num_char] == friend_request:
        parse_friend_request(msg[num_char:], username)
        
    elif msg[:num_char] == friend_request_accepted:
        parse_friend_request_accepted(msg[num_char:], username)
        
    elif msg[:num_char] == friend_request_declined:
        parse_friend_request_declined(msg[num_char:], username)
        
        
        
        
def parse_user_state_changed(data, username):
    global db, users_sockets
    print 'user ' + str(username) + ' is now ' + str(data)
    
    state = int(data)
    db.set_field(username, 'state', state)
    try: users_sockets[username].state = state
    except KeyError: pass
    
    frd_list = db.get_list_from_field(username, 'friends_list')
    for friend in frd_list:
        try:
            users_sockets[friend].send(send_state_changed + str(username) + ',' + str(state))
        except KeyError: pass
        
        
def parse_user_connecting_to_friend(data, username):
    global db, users_sockets
    friend_username = data.strip()
    print 'user ' + username + ' starts connecting to ' + friend_username
    
    frd_list = db.get_list_from_field(username, 'friends_list')
    if friend_username in frd_list:
        if int(db.get_fields(friend_username, 'state')[0][0]) != 0:
            if any(users_sockets[username].sleeping_sockets) and any(users_sockets[friend_username].sleeping_sockets):
                usr_ip, usr_port = users_sockets[username].use_sleeping()
                frnd_ip, frnd_port = users_sockets[friend_username].use_sleeping()
                
                users_sockets[username].send(send_friend_connecting + friend_username + ',' + frnd_ip + ',' + str(frnd_port))
                users_sockets[friend_username].send(send_friend_connecting + username + ',' + usr_ip + ',' + str(usr_port))                
            else: print 'either ' + username + ' or ' + friend_username + " don't have a connected sleeping socket"
        else: print friend_username + ' is offline'
    else: print friend_username + ' not on ' + username + "'s friends list."
    
    
def parse_user_profile_data_changed(data, username):
    pass
    
    
def parse_friend_request(data, username):
    global db, users_sockets
    friend_username = data.strip()
    print 'user ' + username + ' sent a friend request to user ' + friend_username
    
    if db.does_user_exist(friend_username):
        frd_list = db.get_list_from_field(username, 'friends_list')
        if friend_username not in frd_list:
            db.append_to_field(username, 'sent_friend_requests', friend_username)
            if int(db.get_fields(friend_username, 'state')[0][0]) != 0:
                users_sockets[friend_username].send(send_friend_request + username)
            else:
                db.append_to_field(friend_username, 'queued_messages', send_friend_request + username)
        else: print friend_username + ' already in ' + username + "'s friends list"
    else: print friend_username + ' does not exist'
    
    
def parse_friend_request_accepted(data, username):
    global db, users_sockets
    friend_username = data.strip()
    print 'user ' + username + ' accepted a friend request from user ' + friend_username
    
    if username in db.get_list_from_field(friend_username, 'sent_friend_requests'):
        db.append_to_field(username, 'friends_list', friend_username)
        db.append_to_field(friend_username, 'friends_list', username)
        
        db.remove_from_field(friend_username, 'sent_friend_requests', username)
        
        users_sockets[username].send(send_state_changed + str(friend_username) + ',' + str(users_sockets[friend_username].state))
        
        if int(db.get_fields(friend_username, 'state')[0][0]) != 0:
            users_sockets[friend_username].send(send_friend_request_accepted + username)
            if username in users_sockets and friend_username in users_sockets:
                users_sockets[friend_username].send(send_state_changed + str(username) + ',' + str(users_sockets[username].state))
        else:
            db.append_to_field(friend_username, 'queued_messages', send_friend_request_accepted + username)
        
        
def parse_friend_request_declined(data, username):
    global db, users_sockets
    friend_username = data.strip()
    print 'user ' + username + ' declined a friend request from user ' + friend_username
    
    if username in db.get_list_from_field(friend_username, 'sent_friend_requests'):
        db.remove_from_field(friend_username, 'sent_friend_requests', username)
        
        if int(db.get_fields(friend_username, 'state')[0][0]) != 0:
            users_sockets[friend_username].send(send_friend_request_declined + username)
        else:
            db.append_to_field(friend_username, 'queued_messages', send_friend_request_declined + username)