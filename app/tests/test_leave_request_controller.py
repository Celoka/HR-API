import json
import jwt

from datetime import datetime


from app import app, db
from app.services.user_service import User
from app.models.user_model import UserModel
from app.services.leave_request_service import LeaveRequestService


leave_start = datetime.strptime('2023-09-10', '%Y-%m-%d')
leave_end = datetime.strptime('2023-09-12', '%Y-%m-%d')


def test_create_leave_request():
    # Create a user and manager for testing
    with app.app_context():
        user = UserModel(
            first_name='User',
            last_name='Name',
            email_address='user@example.com',
            password='password',
            role='Staff',
        )

        manager = UserModel(
            first_name='Manager',
            last_name='Name',
            email_address='manager@example.com',
            password='password',
            role='Admin',
        )

        super_admin = UserModel(
            first_name='Super',
            last_name='Admin',
            email_address='super.admin@example.com',
            password='password',
            role='Super admin',
        )

        db.session.add(user)
        db.session.add(manager)
        db.session.add(super_admin)

        db.session.commit()

        client = app.test_client()


        super_admin_payload = {'user_id': super_admin.id, 'role': 'Super admin'}
        super_admin_secret_key = 'your_secret_key'
        super_admin_token = jwt.encode(super_admin_payload, super_admin_secret_key, algorithm='HS256')

        response = client.post('/api/v1/user/assign-manager', json={
            'subordinateId': user.id,
            'managerId': manager.id,
            'superAdminId': super_admin.id,
        }, headers={'Authorization': f'Bearer {super_admin_token}'})

        # Create a JWT for the user
        payload = {'user_id': user.id, 'role': 'Staff'}
        secret_key = 'your_secret_key'
        token = jwt.encode(payload, secret_key, algorithm='HS256')


        # Perform the creation of a leave request
        response = client.post('/api/v1/leave-request/create', json={
            'userId': user.id,
            'leaveStart': '2023-09-10',
            'leaveEnd': '2023-09-12',
            'eventType': 'Holiday',
            'description': 'We are planning a day off',
        }, headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 201

        data = json.loads(response.data)
        assert 'request' in data['payload']
        assert data['payload']['request']['eventType'] == 'Holiday'

        leave_request_service = LeaveRequestService()
        leave_requests = leave_request_service.filter_by(user_id=user.id)
        assert len(leave_requests) == 1
        assert leave_requests[0].event_type == 'Holiday'


def test_get_calendar_events():
    with app.app_context():

        user = UserModel(
            first_name='User',
            last_name='Name',
            email_address='user@example.com',
            password='password',
            role='Staff',
        )

        db.session.add(user)
        db.session.commit()

        leave_request_service = LeaveRequestService()
        leave_request_service.create_leave_request(
            user_id=user.id,
            leave_start=leave_start,
            leave_end=leave_end,
            event_type='Holiday',
            description='We are planning a day off',
        )

        payload = {'user_id': user.id, 'role': 'Staff'}
        secret_key = 'your_secret_key'
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        client = app.test_client()

        response = client.get(f'/api/v1/leave-request/calendar-events/{user.id}',
                              headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'calendar_events' in data['payload']
        assert len(data['payload']['calendar_events']) == 1
        assert data['payload']['calendar_events'][0]['eventType'] == 'Holiday'
