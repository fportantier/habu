import glob
entries = []

for file in sorted(glob.glob("habu/cli/cmd_*.py")):
    cmd_file = file.replace('habu/cli/', '').replace('.py', '')
    cmd_name = cmd_file.replace('cmd_', 'habu.').replace('_', '.')
    #print(file, cmd_file, cmd_name)
    entries.append("{cmd_name} = habu.cli.{cmd_file}:{cmd_file}".format(cmd_file=cmd_file, cmd_name=cmd_name))

print('\n'.join(entries))
