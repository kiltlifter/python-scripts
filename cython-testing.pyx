import time

def print_time():
	print "The time is " + str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) + \
	":" + str(time.localtime().tm_sec)

def main():
	print_time()

if __name__ == '__main__':
	main()


