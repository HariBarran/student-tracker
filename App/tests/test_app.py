import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import User, StudentModel, reviewModel, Reviews
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user,
    validate_vote,
    create_student,
    create_review,
    get_student,
    validate_student_id,
    get_all_students,
    update_review,
    karma_calc
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_toJSON(self):
        user = User("rob", "robpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"id":None, "username":"rob"})
    
    def test_new_student(self):
        student = StudentModel(812019285,"James")
        student_json = student.toJSON()
        self.assertDictEqual((student_json), {"id":None, "studentId": 812019285, "name":"James", "karma": 0.0, "reviews":[]})
    
    def test_new_review(self):
        review = Reviews(812014285, "life is hard", 10, 5)
        review_Json = review.toJSON()
        self.assertDictEqual(review_Json, {"id":None, "studentId": 812014285, "message": "life is hard", "upvote" : 10, "downvote" : 5})
    
    # def test_hashed_password(self):
    #     password = "mypass"
    #     hashed = generate_password_hash(password, method='sha256')
    #     user = User("bob", password)
    #     assert user.password != password

    # def test_check_password(self):
    #     password = "mypass"
    #     user = User("bob", password)
    #     assert user.check_password(password)

    # def test_upvote_validation(self):
    #     vote = {'upvote': 1,'downvote':0}
    #     string = validate_vote(vote)
    #     #print (string.append( "this is something !!!!"))
    #     assert (string == "")

    # def test_downvote_validation(self):
    #     vote = {'upvote': 0, 'downvote':1}
    #     string = validate_vote(vote)
    #     #print (string.append("this is nothing !!!!"))
    #     assert (string == "")

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert authenticate("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"
    

    def test_create_student(self):
        student = create_student(812394821, "Richard")
        assert student
    
    def test_create_review(self):
        review = create_review( "Hello! this peepee sucks poopoo", 812394821, 1, 0)
        assert review.message == "Hello! this peepee sucks poopoo"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    #Function to ensure the student ID entered contains the correct values
    def test_studentID_validation(self):
        studentId = 816014286
        valid = validate_student_id(studentId)
        assert valid

    def test_get_student(self):
        student = get_student(812394821)
        assert student.studentId == 812394821
    

    #Test to ensure an updated user is retrieved with the updated values
    # Tests data changes in the database 
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
    
    def test_karma_calculation(self):
        karma_calc(812394821)
        student = get_student(812394821)
        assert student.karma == 100
    
    def test_update_review(self):
        update_review(1, 1.0, 0)
        student = get_student(812394821)
        assert student.reviews[0].upvote == 2
    
    
