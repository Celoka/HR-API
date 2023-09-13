# test_user_controller.py

import json
import jwt

from datetime import datetime

from app import app, db
from app.services.user_service import User
from app.models.user_model import UserModel
from app.services.leave_request_service import LeaveRequestService


client = app.test_client()

def test_create_staff_user():
    response = client.post('/api/v1/user/create', json={
        'firstName': 'Staff',
        'lastName': 'User',
        'emailAddress': 'staff.user@example.com',
        'password': 'password'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'user' in data['payload']


def test_create_super_admin_user():
    response = client.post('/api/v1/user/super-admin/create', json={
        'firstName': 'Super Admin',
        'lastName': 'User',
        'emailAddress': 'super.admin.user@example.com',
        'password': 'password'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'user' in data['payload']


def test_login():
    client.post('/api/v1/user/super-admin/create', json={
        'firstName': 'Super Admin',
        'lastName': 'User',
        'emailAddress': 'super.admin.user@example.com',
        'password': 'password'
    })
    response = client.post('/api/v1/user/login', json={
        'emailAddress': 'super.admin.user@example.com',
        'password': 'password'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'user' in data['payload']

def test_list_users_and_status():
    with app.app_context():
        client = app.test_client()
        db.create_all()
    
        user1 = UserModel(
            first_name='John',
            last_name='Doe',
            email_address='john@example.com',
            password='password',
            role='Staff',
        )

        user2 = UserModel(
            first_name='Jane',
            last_name='Smith',
            email_address='jane@example.com',
            password='password',
            role='Staff',
        )

        user3 = UserModel(
            first_name='Super ',
            last_name='admin',
            email_address='super.admin@example.com',
            password='password',
            role='Super admin',
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()

        leave_request_service = LeaveRequestService()

        leave_start = datetime.strptime('2023-09-10', '%Y-%m-%d')
        leave_end = datetime.strptime('2023-09-12', '%Y-%m-%d')

        # Create leave requests for the users
        leave_request_service.create_leave_request(user_id=user1.id,
                                                   leave_start=leave_start,
                                                   leave_end=leave_end,
                                                   event_type= "Holiday",
                                                   description= "We are planining a day")

        leave_request_service.create_leave_request(user_id=user2.id, 
                                                   leave_start=leave_start,
                                                   leave_end=leave_end,
                                                   event_type="Holiday",
                                                   description="We are planining a day")

        payload = {'user_id': 3, 'role': 'Admin'}
        secret_key = 'your_secret_key'
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        client = app.test_client()
        response = client.get('/api/v1/user/admin/all-users',
                              headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200

def test_assign_manager():
    with app.app_context():

        manager = UserModel(
            first_name='Manager',
            last_name='User',
            email_address='manager@example.com',
            password='password',
            role='Admin',
        )

        subordinate = UserModel(
            first_name='Subordinate',
            last_name='User',
            email_address='subordinate@example.com',
            password='password',
            role='Staff',
        )

        super_admin = UserModel(
            first_name='Super',
            last_name='Admin',
            email_address='super.admin@example.com',
            password='password',
            role='Super admin',
        )

        db.session.add(manager)
        db.session.add(subordinate)
        db.session.add(super_admin)
        db.session.commit()

        payload = {'user_id': super_admin.id, 'role': 'Super admin'}
        secret_key = 'your_secret_key'
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        client = app.test_client()

        response = client.post('/api/v1/user/assign-manager', json={
            'subordinateId': subordinate.id,
            'managerId': manager.id,
            'superAdminId': super_admin.id,
        }, headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'msg' in data
        assert data['msg'] == 'Manager assigned successfully'

        user_service = User()
        subordinate_from_db = user_service.get(subordinate.id)

        assert subordinate_from_db.manager == manager
        assert manager.role == 'Admin'


def test_uplift_staff_to_manager():
    with app.app_context():

        staff = UserModel(
            first_name='Staff',
            last_name='User',
            email_address='staff@example.com',
            password='password',
            role='Staff',
        )

        super_admin = UserModel(
            first_name='Super',
            last_name='Admin',
            email_address='super.admin@example.com',
            password='password',
            role='Super admin',
        )

        admin = UserModel(
            first_name='Admin',
            last_name='User',
            email_address='admin@example.com',
            password='password',
            role='Admin',
        )

        db.session.add(staff)
        db.session.add(super_admin)
        db.session.add(admin)
        db.session.commit()

        payload = {'user_id': super_admin.id, 'role': 'Super admin'}
        secret_key = 'your_secret_key'
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        client = app.test_client()

        response = client.post('/api/v1/user/uplift-user', json={
            'userId': staff.id,
            'superAdminId': super_admin.id,
        }, headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'msg' in data
        assert data['msg'] == 'Admin role assigned successfully'

        user_service = User()
        staff_from_db = user_service.get(staff.id)
        assert staff_from_db.role == 'Admin'
