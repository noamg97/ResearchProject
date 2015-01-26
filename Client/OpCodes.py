num_char = 2 #how many characters in an opcode

#____Blocking (New Connections):____#

#incoming
login = '00'
user_creation = '01'
sleeping_socket_connection = '02'
friends_list = '03'

#outgoing
login_accepted = '99'
login_declined = '98'
user_created = '97'
user_creation_declined = '96'
sleeping_socket_accepted = '95'
sleeping_socket_declined = '94'




#____Non-Blocking (Logged In Users):____#

#outgoing
my_state_changed = '00'
connect_to_peer = '01'
profile_data_changed = '02'
send_friend_request = '03'
accept_friend_request = '04'
decline_friend_request = '05'

#incoming
friend_connecting = '99'
friend_state_changed = '98'
friend_request = '97'
friend_request_accepted = '96'
friend_request_declined = '95'



@staticmethod
def get_action_by_opcode(opcode):
    for action, op in vars(OpCodes).iteritems():
        if str(op) == str(opcode):
            return str(action)
    return ''