import os

UPLOAD_FOLDER = 'static/images/uploads/'
ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])

homer_gif_path = 'static/images/homer.gif'
client_id = os.environ['IMGUR_CLIENT_ID']
consumer_secret = os.environ['IMGUR_CONSUMER_SECRET']
