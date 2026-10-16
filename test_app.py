import unittest
import sqlite3
from app import app, init_db, get_db

class AssessmentTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'test_students.db'
        self.client = app.test_client()
        init_db()

        # Clear students table before testing
        conn = get_db()
        conn.execute("DELETE FROM students")
        conn.commit()
        conn.close()

    def test_level1_and_level2_registration(self):
        # 1. Register a new student
        data = {
            'name': 'Sarah Connor',
            'email': 'sarah@test.com',
            'age': '22',
            'gender': 'Female',
            'course': 'Computer Science',
            'password': 'password123'
        }
        res = self.client.post('/register', data=data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Welcome, Sarah Connor! You have successfully registered.", res.data)

        # 2. Check DB storage
        conn = get_db()
        row = conn.execute("SELECT * FROM students WHERE email = ?", ('sarah@test.com',)).fetchone()
        conn.close()
        self.assertIsNotNone(row)
        self.assertEqual(row['name'], 'Sarah Connor')
        self.assertEqual(row['age'], 22)
        self.assertEqual(row['gender'], 'Female')
        self.assertEqual(row['course'], 'Computer Science')

        # 3. Duplicate email try/except handling
        res_dup = self.client.post('/register', data=data)
        self.assertEqual(res_dup.status_code, 400)
        self.assertIn(b"already registered", res_dup.data)

    def test_level3_login_and_profile(self):
        # Insert student
        data = {
            'name': 'John Doe',
            'email': 'john@test.com',
            'age': '20',
            'gender': 'Male',
            'course': 'Software Engineering',
            'password': 'secretpassword'
        }
        self.client.post('/register', data=data)

        # Invalid login
        res_bad = self.client.post('/login', data={'email': 'john@test.com', 'password': 'wrong'})
        self.assertIn(b"Invalid email or password", res_bad.data)

        # Valid login
        res_good = self.client.post('/login', data={'email': 'john@test.com', 'password': 'secretpassword'}, follow_redirects=True)
        self.assertEqual(res_good.status_code, 200)
        self.assertIn(b"Welcome, John Doe", res_good.data)
        self.assertIn(b"Software Engineering", res_good.data)

        # Profile route
        prof = self.client.get('/profile')
        self.assertIn(b"john@test.com", prof.data)
        self.assertIn(b"20", prof.data)

        # Logout
        logout = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b"Student Login", logout.data)

        # Profile access blocked after logout
        blocked = self.client.get('/profile', follow_redirects=True)
        self.assertIn(b"Student Login", blocked.data)

    def test_level4_course_update(self):
        # Register and login
        data = {
            'name': 'Alex Smith',
            'email': 'alex@test.com',
            'age': '23',
            'gender': 'Male',
            'course': 'Information Technology',
            'password': 'password123'
        }
        self.client.post('/register', data=data)
        self.client.post('/login', data={'email': 'alex@test.com', 'password': 'password123'})

        # AJAX update course
        res = self.client.post('/update-course', data={'course': 'Data Science'})
        self.assertEqual(res.status_code, 200)
        json_data = res.get_json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['course'], 'Data Science')

        # Check DB updated
        conn = get_db()
        row = conn.execute("SELECT course FROM students WHERE email = ?", ('alex@test.com',)).fetchone()
        conn.close()
        self.assertEqual(row['course'], 'Data Science')

if __name__ == '__main__':
    unittest.main()
