#!/bin/python3
import os, sys, pwd, grp, gzip 

def write_attribute(key, value, output, first=False, last=False):
  key = key.replace("\\", "\\\\").replace('"', '\\"')

  if first:
    output.write('{')

  output.write(f'"{key}":')

  if type(value) == str:
    value = value.replace('"', '\\"')
    output.write(f'"{value}"')
  elif type(value) == int or type(value) == float:
    output.write(str(value))
  else:
    raise RuntimeError(f"Unknown value type found when converting to JSON")

  if last:
    output.write('}')
  else:
    output.write(',')

def scan_dir(dir_path, output):
  output.write("[")
  # Check each file in directory
  first_file = True
  for entry in os.listdir(dir_path):
    # Get file attributes
    if first_file:
      first_file = False
    else:
      output.write(',')

    write_attribute("filename", entry, output, first=True)
    path = os.path.join(dir_path, entry)
    stat = os.lstat(path)
    write_attribute('ctime', stat.st_ctime, output)
    write_attribute('mtime', stat.st_mtime, output)
    write_attribute('mode', stat.st_mode, output)
    write_attribute('user', pwd.getpwuid(stat.st_uid).pw_name, output)
    write_attribute('group', grp.getgrgid(stat.st_gid).gr_name, output)

    # Determine the file's type
    if os.path.islink(path):    # Symlink
      write_attribute('type', 'symlink', output)
      write_attribute('target', os.readlink(path), output, last=True)
    elif os.path.isdir(path):   # Directory
      write_attribute('type', 'dir', output)
      output.write('"contents":')
      scan_dir(path, output)
      output.write('}')
    elif os.path.isfile(path):  # File
      write_attribute('type', 'file', output, last=True)
    else:                       # Unknown
      raise RuntimeError(f"Unknown item type found: {path}")
  output.write("]")


if __name__ == "__main__":
  # Make sure the right cmd arguments were given
  if len(sys.argv) != 3:
    print(f"Wrong number of arguments. Usage: {sys.argv[0]} scan_dir output_file.gz", file=sys.stderr)
    exit(1)
  elif not os.path.exists(sys.argv[1]):
    print(f"Given scan path doesn't exist. Usage: {sys.argv[0]} scan_dir output_file.gz", file=sys.stderr)
    exit(1)
  else:
    # Cmd arguments are good
    with gzip.open(sys.argv[2], mode='wt') as output_file:
      scan_dir(sys.argv[1], output_file)
