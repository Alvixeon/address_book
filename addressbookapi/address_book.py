class address_book(object):

	def __init__(self):
		self.user_id = None
		self.logged_in = False
		self.users = {}
		self.user_info = None
		self.contacts = {}
		self.load_users()
		
	def login(self, user, pw):
		if user in self.users and self.logged_in == False:
			if pw == self.users[user][0]:
				self.user_info = self.users[user][1:]
				self.logged_in = True
				self.user_id = user
				self.load_contacts()
				return self.logged_in
		return False

	def logout(self):
		if self.logged_in == True:
			self.user_info = {}
			self.logged_in = False
			self.user_id = None
			self.contacts = {}
			return True
		return False

	def create_user(self, user, *info):
		if user not in self.users:
			with open("users.txt", 'a') as f:
				f.write("\n" + user + " " + ';'.join(info))
			self.users[user] = info
			return True
		return False

	def delete_user(self, user, pw):
		data = None
		deleted = False
		if user in self.users and pw == self.users[user][0] and self.logged_in == True:
			with open("users.txt") as f:
				data = f.readlines()
			with open("users.txt", "w") as f:
				for line in data:
					if user not in line:
						f.write(line)
					else:
						deleted = True
		return deleted

	# Returns list of users (for testing)
	def get_users(self):
		return self.users.keys()

	# Returns user info
	def get_user_info(self):
		return self.user_info

	# Returns list of user contacts
	def get_user_contacts(self):
		return self.contacts

	# Modifies user field as specified by input
	# Can be replaced with an update of SQL table entry
	# 0 - Name, 1 - Phone number, etc
	def modify_user(self, field, new_value):
		try:
			self.user_info[field] = new_value
		except:
			return False
		line_to_change = 0
		data = None
		with open("users.txt") as f:
			data = f.readlines()
			f.seek(0)
			for num, line in enumerate(f, 1):
				if self.user_id in line:
					line_to_change = num
		data[line_to_change-1] = "{} {};{}\n".format(self.user_id, self.users[self.user_id][0], ';'.join(self.user_info))
		with open("users.txt", 'w') as f:
			f.writelines(data)
		return True

	# Load users lists with address book accounts
	# Can be replaced with SQL query
	# > select * from users
	def load_users(self):
		with open("users.txt") as f:
			for line in f:
				(user, info) = line.split()
				self.users[user] = info.split(';')
		
	# Load contacts list for user
	# Can be replaced with SQL query
	# > select * from contacts where user="account";
	def load_contacts(self):
		with open("contacts.txt") as f:
			for line in f:
				(user, contact) = line.split()
				if user == self.user_id:
					name = contact.split(';')[0]
					info = contact.split(';')[1:]
					self.contacts[name] = info
					
