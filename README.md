# open-event-scraper

Google spreadsheet parsing for FOSSASIA 2016

## setup

```shell
pip install -r requirements.txt
./run.sh
```

## How deploy to heroku
Install heroku
```
$ sudo apt-get install heroku
```

Add heroku branch to git
```
$ heroku git:remote -a ots-2016
```

Deploy changes to server
```
$ git push heroku master
```

## License

[MIT](./LICENSE)


