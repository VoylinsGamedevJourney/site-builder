import sys
import build

def run(type):
  if type == 'build':
    build.build()
  elif type == 'publish':
    pass
  elif type == 'help':
    pass
  else: print('Invalid command!')
  

if __name__ == '__main__':
  if len(sys.argv) < 2:
    run('help')
  else:
    run(sys.argv[1])
