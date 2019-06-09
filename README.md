# noonpacific_automator

## To build:

Run:

First, you should generate the following config.yaml file

```
whitelabel: KEY_FOR_WHITELABEL 
buffer: KEY_FOR_BUFFER 
buffer_twitter: True|False Boolean on whether to publish to Twitter
```

To Deploy,

```
python setup.py sdist
docker build .
```

Go stupid! Go crazy!
