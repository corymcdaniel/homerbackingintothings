# Homer Backing Into Things

![](http://www.homerbackingintothings.com/static/images/homer.gif)

This is a gif generator that replaces the green bushes of the `homer backing into bushes` gif with whatever image is uploaded, then uploads the image to imgur.com.

## To Install:

Make sure you have `libjpeg` installed:
```
$ brew install libjpeg
```

Register an application at Imgur: 
```
https://api.imgur.com/oauth2/addclient
```
  
Then clone this repo:
```
$ git clone https://github.com/rodneykeeling/homerbackingintothings
```

Install Python dependencies
```
$ sudo pip install -r requirements.txt
```

Set a few environmental variables:

```
$ export IMGUR_CLIENT_ID='my_imgur_client_id'
$ export IMGUR_CONSUMER_SECRET='my_imgur_secret'
```

Run the app!
```
$ python app.py
```

## Contributing

Fork it    
Create your feature branch (`git checkout -b my-new-feature`)    
Commit your changes (`git commit -am 'Add some feature'`)    
Push to the branch (`git push origin my-new-feature`)    
Create new Pull Request    
???    
Profit    
