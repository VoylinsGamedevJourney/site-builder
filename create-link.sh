#!/bin/bash

current_folder=$(pwd)

if [ ! -f "$current_folder/site-builder.sh" ]; then
  echo "Error: site-builder.sh file not found in $current_folder"
  exit 1
fi
if [ -L /usr/local/bin/site-builder ]; then
  sudo rm /usr/local/bin/site-builder
fi
if [ -L /etc/bash_completion.d/site-builder.sh ]; then
  sudo rm /etc/bash_completion.d/site-builder.sh
fi

sudo ln -s "$current_folder/site-builder.sh" /usr/local/bin/site-builder

sudo cp "$current_folder/site-builder-completion.sh" /etc/bash_completion.d/site-builder.sh
sudo chmod +x /etc/bash_completion.d/site-builder.sh
