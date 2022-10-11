# Simple django task manager demo
[![Actions Status](https://github.com/BasedOnEvidence/python-project-lvl4/workflows/build/badge.svg)](https://github.com/BasedOnEvidence/python-project-lvl4/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/9ac5612e7a335e9f9108/maintainability)](https://codeclimate.com/github/BasedOnEvidence/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9ac5612e7a335e9f9108/test_coverage)](https://codeclimate.com/github/BasedOnEvidence/python-project-lvl4/test_coverage)


## Demostration
You can find project demo <a href="https://task-manager-template.herokuapp.com/" target="_blank">here</a>.
Username: test
Password: Qwerty!@
Or <a href="https://task-manager-template.herokuapp.com/users/create/" target="_blank">register</a> your own account!

## Build
```
cd ~
git clone git@github.com:BasedOnEvidence/task-manager.git
cd task-manager
sudo apt update -y
sudo apt install -y python3-venv libpq-dev python3-dev
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
make start
```
Now you can connect to your webserver via browser http://127.0.0.1:8000