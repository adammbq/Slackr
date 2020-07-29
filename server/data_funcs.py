'''
this file contains all the functions that interact with the data
such as get_data and functions that pickle and unpickle the data.
It also contains the data structure itself.
'''
import pickle
import os

DATA = {
    'users': [], # [{uid, email, password, firstname, lastname, handle, tokens, perm_id}]
    'channels': [], # [{channel_id, channel_name, owners, members, message_ids}]
    'valid_reset': {}, # {code: email}
    'messages' : [] #[{channel_id, message_id, u_id, reacts, time_created, is_pinned, message}]
}

def get_data():
    '''
    get_data checks
    if there is no pickle file, create one
    otherwise, use the data from that file
    '''
    if os.path.exists('server/data.p'):
        # keep trying to get the data from data.p
        # it sometimes is writing at the same time as trying to read
        # so during that time just wait
        while True:
            try:
                return pickle.load(open('server/data.p', 'rb'))
            except Exception:
                pass
    else:
        return DATA

def pickle_data(data):
    '''
    pickle_data stores the data on the server to
    a local directory
    '''
    with open('server/data.p', 'wb') as f_ile:
        pickle.dump(data, f_ile)

def clear_data():
    '''
    clear_data removed the pickled files so to simplfy
    the testing process
    '''
    with open('server/data.p', 'wb') as f_ile:
        pickle.dump(DATA, f_ile)

# coverage run --branch --include=message_funcs.py -m pytest message_react_test.py
