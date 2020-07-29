''' import needed modules '''
from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    '''
    Raises AccessError per documentation
    '''
    code = 400
    message = 'No message specified'

class ValueError(HTTPException):
    '''
    Raises ValueError per documentation
    '''
    code = 400
    message = 'No message specified'
