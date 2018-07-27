import socket


#table = {num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
table = [ num for name,num in vars(socket).items() if name.startswith("IPPROTO") ]
table = list(sorted(set(table)))

print(table)
