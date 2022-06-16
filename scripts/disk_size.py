import psutil

def to_gb(bytes):
	return bytes / 1024**3
	
disk_usage = psutil.disk_usage("/")
size = to_gb(disk_usage.total)

if size < 40: 
	exit(0)
else: 
	exit(5)
