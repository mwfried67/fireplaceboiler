****Using GIT****

To pull branch B1: git clone -b B1 https://github.com/mwfried67/fireplaceboiler.git

Make some changes an then check status: git status
Check what branch you are working on: git branch

Then stage changes for commit: git add .
Then commit locally with comment: git commit -m "fixed path in boilercontrol.sh"
Then push to branch B1: git push origin B1


To update from remote: git pull origin master