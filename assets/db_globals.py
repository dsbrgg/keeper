#!/usr/bin/env python

import os, re

class Globals :
	def __init__(self, scrt) :
		print(scrt)
		self.bin = None
		self.salt = scrt['salt']
		self.key32 = scrt['key32']
		self.aes = scrt['aes']
		self.path = scrt['path']
		self.table      = 'COMPANY'+' '*17+'ACCOUNT'+' '*17+'PASSWORD\n'+'-'*20+' '*4+'-'*20+' '*4+'-'*20+' '*4 +'\n'
		self.new_line   = ''

	def read(self) :
		self.bin = open(self.path).read()
		return self

	def decrypt(self) :
		########	BYTE PADDING	########
		def pad(text):
			while len(text) % 8 != 0:
				text += ' '
			return text

		# pad_string = pad(string)
		# aes_encrypt = self.aes.encrypt(pad_string)
		#
		# self.aes_encrypt
		# new_file = open(path_to_data,"w+")
		# new_file.write(aes_encrypt)

		return self.aes.decrypt(self.bin)

	def switch(self, command, regex, array) :
		def company() :
			index = 0
			while index < len(array)-1 :
				line 		= array[index]
				regex_match = re.match(regex, line)

				if regex_match :
					acc_line = array[index+1]
					pwd_line = array[index+2]

					self.new_line += (line + ' '*(24-len(line))) + (acc_line + ' '*(24-len(acc_line))) + (pwd_line + ' '*(24-len(pwd_line))) + '\n'
					self.table += self.new_line
					self.new_line = ''

				index += 3

			return self.table

		def account() :
			index = 0
			while index < len(array)-1 :
				line 		= array[index]
				regex_match = re.match(regex, line)

				if regex_match :
					comp_line = array[index-1]
					pwd_line = array[index+1]

					self.new_line += (comp_line + ' '*(24-len(comp_line))) + (line + ' '*(24-len(line))) + (pwd_line + ' '*(24-len(pwd_line))) + '\n'
					self.table += self.new_line
					self.new_line = ''

				index += 1

			return self.table

		def default() :
			for index, line in enumerate(array):
				is_company = True if ((index+3) % 3) == 0 else False

				if is_company and index :
					self.new_line += '\n'
					self.table += self.new_line
					self.new_line = ''

				self.new_line += line + ' '*(24-len(line))

			return self.table

		return {
			'-c' : company,
			'-a' : account,
			''	 : default
		}[command]
