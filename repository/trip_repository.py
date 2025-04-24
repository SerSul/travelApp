from datetime import date

from entity.enums import TripStatus
from entity.models import BusinessTrip
from .base_repository import *

class TripRepository(BaseRepository):
    def __init__(self):
        super().__init__(BusinessTrip)

    def get_employee_trips(self, employee_id: int) -> List[BusinessTrip]:
        return self.filter_by(employee_id=employee_id)

    def get_active_trips(self) -> List[BusinessTrip]:
        return self.model.query.filter(
            BusinessTrip.status.in_([TripStatus.PLANNED, TripStatus.IN_PROGRESS])
        ).all()

    def get_trips_in_date_range(self, start: date, end: date) -> List[BusinessTrip]:
        return self.model.query.filter(
            BusinessTrip.start_date >= start,
            BusinessTrip.end_date <= end
        ).all()