#!/bin/bash

LANG=en_US.UTF-8 \
    ~/.pyenv/shims/python3 ~/git/twitter2facebook/twitter2facebook.py \
    true

# Since our pkill run with parent pid filtering (pid == 1), we need to
# kill geckodriver first, then firefox-esr afterwards.
pkill -P 1 geckodriver || true
pkill -P 1 firefox-esr || true
