#!/bin/bash

CONFIG_FILE="ssh.yaml"
CONFIG=$(cat ${CONFIG_FILE})

# Parse the YAML file
SSH_PORT=$(echo "${CONFIG}" | yq -r '.ssh_port')
REMOTE_HOST=$(echo "${CONFIG}" | yq -r '.remote_host')
REMOTE_FOLDER=$(echo "${CONFIG}" | yq -r '.remote_folder')

# Set the local folder to sync
LOCAL_FOLDER="_site/"

# Execute the rsync command
rsync -avz -e "ssh -p ${SSH_PORT}" "${LOCAL_FOLDER}" "${REMOTE_HOST}:${REMOTE_FOLDER}"