import sys
import build
import yaml
import os
import subprocess


def run(type):
  if type == 'build':
    build.build()
  elif type == 'publish':
    publish()
  elif type == 'help':
    pass
  else: print('Invalid command!')
  

def publish():
  # Check if yaml file present
  if len(sys.argv) < 3:
    print("Please add yaml file with required info as an argument!")
    return
  with open(os.getcwd() + '/' + sys.argv[2], "r") as f:
    config = yaml.safe_load(f)

  ssh_port = config["ssh_port"]
  remote_host = config["remote_host"]
  remote_folder = config["remote_folder"]
  local_folder = os.getcwd() + '/' + "_site/"
  subprocess.run(
    [
      "rsync",
      "-avz",
      "-e",
      f"ssh -p {ssh_port}",
      local_folder,
      f"{remote_host}:{remote_folder}",
    ])


if __name__ == '__main__':
  if len(sys.argv) < 2:
    run('help')
  else:
    run(sys.argv[1])
