import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# Auth0 Config
AUTH0_DOMAIN = 'shrutikumar.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Auth Header


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:

        raise AuthError({
            'code': 'invalid_header',
            'description': 'Permissions not included.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Required permission not included in permissions.'
        }, 401)
    return True


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    # get public key from authorization system

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
   
    jwks = json.loads(jsonurl.read())
    
    # get header data from token
    unverified_header = jwt.get_unverified_header(token)
    
    # choose rsa key
    rsa_key = {}
    
    # validate token header contains kid
    if 'kid' not in unverified_header:
        print("1")
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)
     
    for key in jwks['keys']:
        print("2")
        # if kid match, build rsa key
        if key['kid'] == unverified_header['kid']:
            
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }   
    print(rsa_key)    
    if rsa_key!=None:
        try:
            # validate the token
            print("try")
            payload = jwt.decode(token,
                                 rsa_key,
                                 algorithms=ALGORITHMS,
                                 audience=API_AUDIENCE,
                                 issuer='https://' + AUTH0_DOMAIN + '/')
            print("decode")
            return payload
        # catch common errors
        except jwt.ExpiredSignatureError:
            print("Expired")
            raise AuthError(
                {
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)

        except jwt.JWTClaimsError:
            print("auth")
            raise AuthError(
                {
                    'code':'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
        except Exception:
            
            raise AuthError(
                {
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 401)
               
    raise AuthError(
        {
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
               
                token = get_token_auth_header()
                print(token)
                payload = verify_decode_jwt(token)
                print(payload)
                check_permissions(permission, payload)
                
                
                return f(payload, *args, **kwargs)
            except AuthError as e:
                abort(e.status_code)
        return wrapper
    return requires_auth_decorator
    #https://shrutikumar.auth0.com/authorize?audience=capstone&response_type=token&client_id=d0ApqMdCWYHIECvnZUfXDX3yhictl6Rj&redirect_uri=http://127.0.0.1:5000
    #https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
