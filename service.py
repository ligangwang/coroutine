from datastore import save_in_messages

def on_msg_recv(msg):
    
    save_in_messages('ENFN', [msg])