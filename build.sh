# thanks to https://gist.github.com/domenic/ec8b0fc8ab45f39403dd
#!/bin/sh
set -e

git config --global user.name "Travis CI"
git config --global user.email "noreply+travis@fossasia.org"

python scraper.py
python event.py

# don't continue if no changes
if git diff-index --quiet HEAD; then
  exit 0
fi
git pull
git commit -m '[Auto] updated json files [ci skip]' out/*.json || echo "no changes"
git push "https://${GH_TOKEN}@github.com/OpenTechSummit/open-event-scraper" HEAD:master

git clone --depth=1 "https://${GH_TOKEN}@github.com/OpenTechSummit/2016.opentechsummit.net.git" ots-repo

node schedule/generator > ots-repo/programm/index.html

cd ots-repo
rm -rf programm/speakers
rsync -r ../speakers/* programm/speakers
rm -rf programm/audio
rsync -r ../audio/* programm/audio
rsync -r ../img/* programm/img
git add programm/index.html programm/speakers/*.jpg programm/audio/*.mp3 programm/img/*
git commit -m '[Auto] updated schedule' || echo "no changes"
git push origin gh-pages

exit 0
