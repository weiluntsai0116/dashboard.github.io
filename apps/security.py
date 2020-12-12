import os

login_page_url = "http://user-service-dash.eba-y82cxuwr.us-east-2.elasticbeanstalk.com/"

jwt_secret = os.environ['JWT_SECRET']
jwt_algo = os.environ['JWT_ALGO']
jwt_exp_delta_sec = float(os.environ['JWT_EXP'])

fernet_secret = os.environ['TOKEN_SECRET'].encode('utf-8')