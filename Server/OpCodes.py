num_char = 2 #how many characters in an opcode


#____Unidentified Users:____#

#incoming
login = '00'
user_creation = '01'
sleeping_socket_connection = '02'

#outgoing
login_accepted = '99'
login_declined = '98'
user_created = '97'
user_creation_declined = '96'
sleeping_socket_accepted = '95'
sleeping_socket_declined = '94'




#____Logged In Users:____#

#incoming
user_state_changed = '00'
connect_to_friend = '01'
profile_data_changed = '02'
friend_request = '03'
friend_request_accepted = '04'
friend_request_declined = '05'

#outgoing
send_friend_connecting = '99'
send_state_changed = '98'
send_friend_request = '97'
send_friend_request_accepted = '96'
send_friend_request_declined = '95'