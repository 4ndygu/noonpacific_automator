# noonpacific_automator

## To build:

Run:

First, you should generate the following config.yaml file

```
whitelabel: KEY_FOR_WHITELABEL 
buffer: KEY_FOR_BUFFER 
buffer_twitter: True|False Boolean on whether to publish to Twitter
mailchimp: KEY_FOR_MAILCHIMP
mailchimp_audience: Mailchimp Audience to Deliver to
```

To Deploy,

```
python setup.py sdist
docker build .
```

Run the docker container or deploy it on the infrastructure of your choice to set this up. The cron file assumes that the local timezone of the server runtime is the same as your local one, so please edit (preferably the cron schedule) accordingly.

Go stupid! Go crazy!
