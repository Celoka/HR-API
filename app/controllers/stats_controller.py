from sqlalchemy import func, extract, and_, case

from app import db
from app.controllers.base_controller import BaseController
from app.services.leave_request_service import LeaveRequestService
from app.models.leave_requests_model import LeaveRequest
from app.services.user_service import User
from app.utils.helper import conflict_handler


class StatisticsController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.user_service = User()
        self.leave_request_service = LeaveRequestService()
        self.leave_request_model = LeaveRequest()

    def get_all_dashboard_stats(self):
        total_employees = self.user_service.count()
        total_pending_applications = self.leave_request_service.filter_and_count(
            **{'status': 'Pending'})
        total_leave_applications = self.leave_request_service.count()
        total_paid_leave = self.leave_request_service.filter_and_count(
            **{'is_paid_leave': 'Yes'})


        time_off_stats = db.session.query(
            extract('year', self.leave_request_service._model.leave_start).label('year'),
            extract('month', self.leave_request_service._model.leave_start).label('month'),
            func.count().label('total_leave_requests'),
            func.sum(
                case(
                    (and_(
                        self.leave_request_service._model.event_type == 'Sick leave',
                        self.leave_request_service._model.is_paid_leave == 'Yes'
                    ), 1),
                    else_=0
                )
            ).label('paid_sick_leave'),
            func.sum(
                case(
                    (and_(
                        self.leave_request_service._model.event_type == 'Sick leave',
                        self.leave_request_service._model.is_paid_leave == 'No'
                    ), 1),
                    else_=0
                )
            ).label('unpaid_sick_leave')
        ).group_by('year', 'month').all()

        time_off_stats_result = []
        for row in time_off_stats:
            time_off_stats_result.append({
                'year': row.year,
                'month': row.month,
                'total_leave_requests': row.total_leave_requests,
                'paid_sick_leave': row.paid_sick_leave,
                'unpaid_sick_leave': row.unpaid_sick_leave
            })

        final_result = {
            'total_employees': total_employees,
            'total_pending_applications': total_pending_applications,
            'total_leave_applications': total_leave_applications,
            'total_paid_leave': total_paid_leave,
            'time_off_stats': time_off_stats_result
        }



        return self.handle_response('Ok', payload=final_result)
