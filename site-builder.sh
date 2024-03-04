#!/bin/bash

symlink_path=$(readlink -f /usr/local/bin/site-builder)
dir_path=$(dirname "$symlink_path")
args=( "$@" )
python "$dir_path/run.py" "${args[@]}"