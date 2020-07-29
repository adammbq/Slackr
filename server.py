'''Flask server'''
import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message

'''Add the server file'''
#sys.path.append('./server')
from server.auth_funcs import register, login, logout, request_reset, reset_reset, permission_change
from server.channel_funcs import (create_channel, list_user_channels, list_all_user_channels,
                           invite_user, join_channel, leave_channel, addowner_channel,
                           details_channel, removeowner_channel, get_messages)
from server.message_funcs import (send_message, remove_message, edit_message,
                           pin_message, unpin_message, react_message, unreact_message,
                           message_search, send_later)
from server.user_profile_funcs import get_user_profile, set_user_email, set_user_name, set_user_handle, get_all_users, upload_photo
from server.standup_funcs import start_standup, active_standup, send_standup

def default_handler(err):
    '''
    Called as the default error handler
    '''
    response = err.get_response()  # catch the exception
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

# Set up app
APP = Flask(__name__, static_url_path='/frontend/prebundle/images')
CORS(APP)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
APP.register_error_handler(Exception, default_handler)

# Add the mail server settings
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='macrosoft1531@gmail.com',
    MAIL_PASSWORD="comp1531"
)


@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })

#Admin/Auth
@APP.route('/admin/userpermission/change', methods=['POST'])
def admin_userpermission_change():
    """ Change user permission """
    token = request.form.get('token')
    u_id = int(request.form.get('u_id'))
    permission_id = int(request.form.get('permission_id'))
    return dumps(permission_change(token, u_id, permission_id))

@APP.route('/auth/login', methods=['POST'])
def auth_login():
    """ Login user """
    email = request.form.get('email')
    password = request.form.get('password')
    return dumps(login(email, password))

@APP.route('/auth/logout', methods=['POST'])
def auth_logout():
    """ Logout user """
    token = request.form.get('token')
    return dumps(logout(token))

@APP.route('/auth/register', methods=['POST'])
def auth_register():
    """ Register user """
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return dumps(register(email, password, name_first, name_last))

@APP.route('/auth/passwordreset/request', methods=['POST'])
def auth_request_reset():
    """ Request reset for password """
    email = request.form.get('email')
    code = request_reset(email)
    mail = Mail(APP)
    try:
        msg = Message("Send Mail Test!",
                      sender="macrosoft1531@gmail.com",
                      recipients=[email])
        msg.body = f"Hello! {code} is your code!!"
        mail.send(msg)
        return dumps(request_reset(email))
    except Exception as e:
        return str(e)

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def auth_reset_reset():
    """ Reset password for user """
    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')
    return dumps(reset_reset(reset_code, new_password))

#Channel
@APP.route('/channels/create', methods=['POST'])
def channels_create():
    """ Create a channel """
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    dump = create_channel(token, name, is_public)
    return dumps(dump)

@APP.route('/channels/list', methods=['GET'])
def channels_list():
    """ List channel user is part of """
    token = request.args.get('token')
    dump = list_user_channels(token)
    return dumps(dump)

@APP.route('/channels/listall', methods=['GET'])
def channels_list_all():
    """ List all channels user is part of """
    token = request.args.get('token')
    dump = list_all_user_channels(token)
    return dumps(dump)

@APP.route('/channel/invite', methods=['POST'])
def channels_invite():
    """ Invite user to channel """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return dumps(invite_user(token, channel_id, u_id))

@APP.route('/channel/join', methods=['POST'])
def channel_join():
    """ Join a channel """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    return dumps(join_channel(token, channel_id))

@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    """ Leave a channel """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    return dumps(leave_channel(token, channel_id))

@APP.route('/channel/details', methods=['GET'])
def channel_details():
    """ Get the details of a channel"""
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    dump = details_channel(token, channel_id)
    return dumps(dump)

@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    """ Remove an owner of a channel """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return dumps(removeowner_channel(token, channel_id, u_id))

@APP.route('/channel/addowner', methods=['POST'])
def channels_addowner():
    """ Add an owner of a channel """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return dumps(addowner_channel(token, channel_id, u_id))

@APP.route('/channel/messages', methods=['GET'])
def channel_messages():
    """ Get the messages from the channel """
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    dump = get_messages(token, channel_id, start)
    return dumps(dump)

@APP.route('/message/react', methods=['POST'])
def message_react():
    """ React to a message within a channel """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    return dumps(react_message(token, message_id, react_id))

@APP.route('/message/unreact', methods=['POST'])
def message_unreact():
    """ Unreact to a message within a channel """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    return dumps(unreact_message(token, message_id, react_id))

@APP.route('/message/send', methods=['POST'])
def message_send():
    """ Send a message to a channel """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message_str = request.form.get('message')
    dump = send_message(token, channel_id, message_str)
    return dumps(dump)

@APP.route('/message/pin', methods=['POST'])
def message_pin():
    """ Pin a message to the channel """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    return dumps(pin_message(token, message_id))

@APP.route('/message/unpin', methods=['POST'])
def message_unpin():
    """ Unpin a message from a channel """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    return dumps(unpin_message(token, message_id))

@APP.route('/message/remove', methods=['DELETE'])
def message_remove():
    """ Remove a message from a channel """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    return dumps(remove_message(token, message_id))

@APP.route('/message/edit', methods=['POST', 'PUT'])
def message_edit():
    """ Edit a message from a channel """
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    message_str = request.form.get('message')
    return dumps(edit_message(token, message_id, message_str))

#User
@APP.route('/user/profile', methods=['GET'])
def user_profile():
    """ Get the user profile """
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    dump = get_user_profile(token, u_id)
    return dumps(dump)

@APP.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname():
    """ Set a user's name """
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return dumps(set_user_name(token, name_first, name_last))

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_profile_setemail():
    """ Set a user's email """
    token = request.form.get('token')
    email = request.form.get('email')
    return dumps(set_user_email(token, email))

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():
    """ Set a user's handle """
    token = request.form.get('token')
    handle_str = request.form.get('handle_str')
    return dumps(set_user_handle(token, handle_str))

@APP.route('/users/all', methods=['GET'])
def users_all():
    """ Get all the users """
    token = request.args.get('token')
    return dumps(get_all_users(token))

@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def user_uploadphoto():
    """ Upload photo """
    token = request.form.get('token')
    img_url = request.form.get('img_url')
    x_start = int(request.form.get('x_start'))
    y_start = int(request.form.get('y_start'))
    x_end = int(request.form.get('x_end'))
    y_end = int(request.form.get('y_end'))
    
    return dumps(upload_photo(token, img_url, x_start, y_start, x_end, y_end))
    
@APP.route("/images/<filename>", methods=["GET"])
def send_js(filename):
	return send_from_directory('', filename)
	

# No caching at all for API endpoints.
@APP.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

#Search
@APP.route('/search', methods=['GET'])
def search():
    """ Search for a particular string within a channel """
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(message_search(token, query_str))

@APP.route('/message/sendlater', methods=['POST'])
def message_sendlater():
    """ Send a message at a specified time """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message_str = request.form.get('message')
    time_sent = float(request.form.get('time_sent'))

    return dumps(send_later(token, channel_id, message_str, time_sent))

#Standup
@APP.route('/standup/start', methods=['POST'])
def standup_start():
    """ Start a standup """
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    length = int(request.form.get('length'))
    return dumps(start_standup(token, channel_id, length))

@APP.route('/standup/active', methods=['GET'])
def standup_active():
    """ check whether standup on channel is active """
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(active_standup(token, channel_id))

@APP.route('/standup/send', methods=['POST'])
def standup_send():
    """ Send a message while a standup is active"""
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message_str = request.form.get('message')
    return dumps(send_standup(token, channel_id, message_str))




if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
