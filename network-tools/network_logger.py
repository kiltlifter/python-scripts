#!/usr/bin/python2.7
import socket
from struct import *
import sqlite3
import os
from multiprocessing import Process


class PacketParser:
	def __init__(self):
		self.ether_header_len = 14
		self.ether_bin_format = '!6s6sH'
		self.ip_packet_bin_format = '!BBHHHBBH4s4s'
		self.tcp_packet_bin_format = '!HHLLBBHHH'
		self.udp_packet_bin_format = '!HHHH'
		self.ethernet_protocol_int = 8
		self.tcp_protocol_int = 6
		self.udp_protocol_int = 17

	def process_packet(self, packet):
		packet_data = packet[0]
		interface = packet[1][0]
		ethernet = unpack(self.ether_bin_format, packet_data[:self.ether_header_len])
		ethernet_proto = socket.ntohs(ethernet[2])
		if ethernet_proto == self.ethernet_protocol_int:
			raw_ip_header = packet_data[self.ether_header_len:20+self.ether_header_len]
			ip_header = unpack(self.ip_packet_bin_format, raw_ip_header)
			protocol = ip_header[6]
			ip_header_len = (ip_header[0] & 0xF) * 4
			ether_data = {"interface": interface, "src": socket.inet_ntoa(ip_header[8]),
						  "dst": socket.inet_ntoa(ip_header[9]), "src_mac": self.ether_addrs(packet_data[0:6]),
						  "dst_mac": self.ether_addrs(packet_data[6:12])}
			if protocol == self.tcp_protocol_int:
				return self._parse_tcp_packet(packet_data, ip_header_len, ether_data)
			elif protocol == self.udp_protocol_int:
				return self._parse_udp_packet(packet_data, ip_header_len, ether_data)

	def _parse_tcp_packet(self, tcp_packet, ip_header_len, packet_data):
		try:
			tcp_packet_len = ip_header_len + self.ether_header_len
			raw_tcp_header = tcp_packet[tcp_packet_len:tcp_packet_len+20]
			tcp_header = unpack(self.tcp_packet_bin_format, raw_tcp_header)
			packet_data["proto"] = "tcp"
			packet_data["src_port"] = tcp_header[0]
			packet_data["dst_port"] = tcp_header[1]
			return packet_data
		except BaseException as e:
			print "Error processing TCP packet\n{0}: {1}".format(e.__class__.__name__, e.args[-1])

	def _parse_udp_packet(self, udp_packet, ip_header_len, packet_data):
		try:
			udp_packet_len = ip_header_len + self.ether_header_len
			raw_udp_header = udp_packet[udp_packet_len:udp_packet_len+8]
			udp_header = unpack(self.udp_packet_bin_format, raw_udp_header)
			packet_data["proto"] = "udp"
			packet_data["src_port"] = udp_header[0]
			packet_data["dst_port"] = udp_header[1]
			return packet_data
		except BaseException as e:
			print "Error processing TCP packet\n{0}: {1}".format(e.__class__.__name__, e.args[-1])

	@staticmethod
	def ether_addrs(binary_rep):
		hex_address = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(binary_rep[0]), ord(binary_rep[1]),
				ord(binary_rep[2]), ord(binary_rep[3]), ord(binary_rep[4]), ord(binary_rep[5]))
		return hex_address


class DBMaker:
	def __init__(self, db_name=None):
		self.db_name = db_name if db_name else "net_profile.db"
		self.init_db = False
		self.connection = self._db_connect()
		if self.init_db:
			self._build_tables()

	def _db_connect(self):
		if not os.path.isfile(self.db_name):
			print "Creating database: {0}".format(self.db_name)
			self.init_db = True
			return sqlite3.connect(self.db_name)
		else:
			return sqlite3.connect(self.db_name)

	def _enable_foreign_keys(self):
		print "Enabling foreign keys."
		self.exec_command('''PRAGMA foreign_keys = ON''')

	def _build_tables(self):
		try:
			# Create the protocol table
			self.exec_command('''CREATE TABLE proto (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									name TEXT NOT NULL,
									CONSTRAINT proto_name UNIQUE (name)
								)''')
			# Create the ports table
			self.exec_command('''CREATE TABLE ports (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									port INTEGER NOT NULL,
									proto INTEGER NOT NULL,
									FOREIGN KEY(proto) REFERENCES proto(id),
									CONSTRAINT port_proto UNIQUE (port, proto)
								)''')
			# Create the source table
			self.exec_command('''CREATE TABLE source (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									ip TEXT NOT NULL,
									CONSTRAINT src_ip UNIQUE (ip)
								)''')
			# Create the destination table
			self.exec_command('''CREATE TABLE destination (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									ip TEXT NOT NULL,
									CONSTRAINT dst_ip UNIQUE (ip)
								)''')
			# Create the interface table
			self.exec_command('''CREATE TABLE interfaces (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									iface TEXT NOT NULL,
									CONSTRAINT interface UNIQUE (iface)
								)''')
			self.exec_command('''CREATE TABLE traffic (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									source TEXT NOT NULL,
									source_port INTEGER NOT NULL,
									destination TEXT NOT NULL,
									destination_port INTEGER NOT NULL,
									interface TEXT NOT NULL,
									CONSTRAINT unique_traffic UNIQUE (
										source, source_port, destination, destination_port, interface
									)
								)''')
		except AttributeError as e:
			print "Error creating default tables: {0}\n{1}".format(e.__class__.__name__, e.args[-1])
		# except sqlite3.OperationalError as o:
		#     print "Operational Error: {0}".format(o.message)

	def exec_command(self, statement):
		try:
			with self.connection:
				self.connection.execute(statement)
		except sqlite3.IntegrityError:
			# print "Error running statement:\n{0}".format(statement)
			# print "{0}: {1}".format(e.__class__.__name__, e.args[-1])
			None

	def exec_command_verbose(self, statement, values=None):
		c = self.connection.cursor()
		try:
			if values:
				c.execute(statement, values)
			else:
				c.execute(statement)
			for e in c:
				print e
		except Exception as e:
			print "Error running command: {0}\n{1}".format(e.__class__.__name__, e.message)
		finally:
			c.close()

	def insert_sample_data(self):
		self.exec_command("INSERT INTO proto (name) VALUES ('tcp')")
		self.exec_command("INSERT INTO proto (name) VALUES ('udp')")

		self.exec_command("INSERT INTO source (ip) VALUES ('127.0.0.1')")
		self.exec_command("INSERT INTO source (ip) VALUES ('192.168.1.101')")
		self.exec_command("INSERT INTO destination (ip) VALUES ('127.0.0.1')")
		self.exec_command("INSERT INTO destination (ip) VALUES ('192.168.1.1')")

		self.exec_command("INSERT INTO ports (port, proto) VALUES (22, 1)")
		self.exec_command("INSERT INTO ports (port, proto) VALUES (443, 1)")
		self.exec_command("INSERT INTO ports (port, proto) VALUES (5544, 1)")
		self.exec_command("INSERT INTO ports (port, proto) VALUES (137, 2)")
		self.exec_command("INSERT INTO ports (port, proto) VALUES (137, 1)")

		self.exec_command("INSERT INTO interfaces (iface) VALUES ('eth0')")


def main():
	db = DBMaker()
	try:
		s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
	except socket.error, msg:
		print "Socket could not be created. Error Code: %s, Message: %s" % (str(msg[0]), str(msg[1]))
		exit()

	parser = PacketParser()
	try:
		with open("logfile.log", "w") as f:
			while True:
				# data = {
				# 'src': '127.0.1.1',
				# 'dst_mac': '00:00:00:00:00:00',
				# 'src_port': 53,
				# 'proto':'udp',
				# 'dst': '127.0.0.1',
				# 'dst_port': 40801,
				# 'interface': 'lo',
				# 'src_mac': '00:00:00:00:00:00'
				# }
				data = parser.process_packet(s.recvfrom(65565))
				if data:
					insert_cmd = "INSERT INTO traffic (" +\
								 "source, source_port, destination, destination_port, interface" + \
								 ") VALUES (" \
								 "'{0}', {1}, '{2}', {3}, '{4}')".format(data['src'], data['src_port'], data['dst'], data['dst_port'], data['interface'])
					try:
						db.exec_command(insert_cmd)
					except sqlite3.IntegrityError:
						None
	except Exception as e:
		print "Error processing packet\n{0}: {1}".format(e.__class__.__name__, e.args[-1])
		s.close()
	except KeyboardInterrupt:
		print "Exiting..."
	finally:
		s.close()


if __name__ == "__main__":
	try:
		p = Process(target=main)
		p.start()
		p.join()
	except KeyboardInterrupt:
		print "Exiting..."
