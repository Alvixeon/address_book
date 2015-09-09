import unittest
from address_book import address_book

class TestAB(unittest.TestCase):

	def setUp(self):
		self.ab = address_book()

	def test_login(self):
		self.assertTrue(self.ab.login('testa', 'test1'))
		self.assertFalse(self.ab.login('testb', 'test2'))

	def test_failed_login(self):
		self.assertFalse(self.ab.login('testa', 'test'))
		self.assertFalse(self.ab.login('test', 'test1'))

	def test_logout(self):
		self.assertFalse(self.ab.logout())
		self.assertTrue(self.ab.login('testa', 'test1'))
		self.assertTrue(self.ab.logout())

	def test_create_user(self):
		with open("users.txt") as f:
			original_content = f.readlines()
		self.assertFalse(self.ab.login('new_user', 'new_pw'))
		self.assertTrue(self.ab.create_user('new_user', 'new_pw', 'new_name', 'new_info'))
		created = False
		with open("users.txt") as f:
			for line in f:
				if 'new_user new_pw;new_name;new_info' in line:
					created = True
					break
		self.assertTrue(created)
		with open("users.txt", "w") as f:
			f.writelines(original_content)

	def test_create_duplicate_user(self):
		self.assertFalse(self.ab.create_user('testa', 'test1', 'name1', 'info1'))

	def test_delete_user(self):
		with open("users.txt") as f:
			original_content = f.readlines()
		self.assertTrue(self.ab.login('testa', 'test1'))
		self.assertTrue(self.ab.delete_user('testa', 'test1'))
		deleted = True
		with open("users.txt") as f:
			for line in f:
				if 'testa test1;name1;info1' in line:
					deleted = False
		self.assertTrue(deleted)
		with open("users.txt", "w") as f:
			f.writelines(original_content)

	def test_failed_delete_user(self):
		self.assertFalse(self.ab.delete_user('no_user', 'no_pw'))
		self.assertFalse(self.ab.delete_user('testa', 'test1'))
		self.ab.login('testa', 'test1')
		self.assertFalse(self.ab.delete_user('testa', 'test'))

	def test_modify_user(self):
		with open("users.txt") as f:
			original_content = f.readlines()
		self.ab.login('testa', 'test1')
		self.assertTrue(self.ab.modify_user(1, 'new_info'))
		modified = False
		with open("users.txt") as f:
			for line in f:
				if 'testa test1;name1;new_info' in line:
					modified = True
					break
		self.assertTrue(modified)
		with open("users.txt", "w") as f:
			f.writelines(original_content)

	def test_failed_modify_user(self):
		with open("users.txt") as f:
			original_content = f.readlines()
		self.ab.login('testa', 'test1')
		self.assertFalse(self.ab.modify_user(4, 'new_info'))
		modified = False
		with open("users.txt") as f:
			for line in f:
				if 'testa test1;name1;new_info' in line:
					modified = True
					break
		self.assertFalse(modified)
		with open("users.txt", "w") as f:
			f.writelines(original_content)

	def test_load_users(self):
		self.ab.load_users()
		self.assertIsNotNone(self.ab.get_users())
		self.assertIn('testa', self.ab.get_users())

	def test_load_contacts(self):
		self.ab.login('testa', 'test1')
		self.assertIsNotNone(self.ab.get_user_contacts())
		self.assertIn('contact1', self.ab.get_user_contacts())

	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()
