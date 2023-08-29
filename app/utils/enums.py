import enum


class LeaveRequestType(str, enum.Enum):
    holiday = "Holiday"
    time_off = "Time off"
    sick_leave = "Sick leave"
    maternity_leave = "Maternity leave"
    paternity_leave = "Paternity leave"
    training_day = "Training day"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class PermissionLevels(str, enum.Enum):
    super_admin = "Super admin"
    admin = "Admin"
    staff = "Staff"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
