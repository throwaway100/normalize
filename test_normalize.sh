#!/bin/bash
# Intended to run on MacOS
# Requirements: python3 and pip3 on path
# Easiest way to do this:
# 	- Install homebrew: /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# 	- Install python3: brew install python3
# Invocation:
# 	- ./test_normalize.sh
readonly script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
readonly venv_dir="${script_dir}/.test_venv"
python3 -m venv ${venv_dir}
source ${venv_dir}/bin/activate
pip3 install -qr ${script_dir}/requirements-dev.txt
pip3 install -qr ${script_dir}/requirements.txt
pytest