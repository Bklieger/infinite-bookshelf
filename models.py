import uuid

class Subject:
    """Represents a subject or activity in the school."""
    def __init__(self, name: str, requires_special_room: bool = False):
        self.id = str(uuid.uuid4())
        self.name = name
        self.requires_special_room = requires_special_room

    def __repr__(self):
        return f"Subject(name='{self.name}')"

class Teacher:
    """Represents a teacher, therapist, or staff member."""
    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name

    def __repr__(self):
        return f"Teacher(name='{self.name}')"

class StudentGroup:
    """Represents a group of students (a class)."""
    def __init__(self, name: str, size: int):
        self.id = str(uuid.uuid4())
        self.name = name
        self.size = size

    def __repr__(self):
        return f"StudentGroup(name='{self.name}', size={self.size})"

class Room:
    """Represents a physical room in the school."""
    def __init__(self, name: str, capacity: int, is_special_room: bool = False):
        self.id = str(uuid.uuid4())
        self.name = name
        self.capacity = capacity
        self.is_special_room = is_special_room

    def __repr__(self):
        return f"Room(name='{self.name}', capacity={self.capacity})"

class TimeSlot:
    """Represents a specific time block in a day."""
    def __init__(self, day: str, start_time: str, end_time: str):
        self.id = str(uuid.uuid4())
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f"{self.day} {self.start_time}-{self.end_time}"

class Lesson:
    """Represents a single scheduled lesson, connecting all other components."""
    def __init__(self, subject: Subject, teacher: Teacher, student_group: StudentGroup, room: Room, timeslot: TimeSlot):
        self.id = str(uuid.uuid4())
        self.subject = subject
        self.teacher = teacher
        self.student_group = student_group
        self.room = room
        self.timeslot = timeslot

    def __repr__(self):
        return (f"Lesson: {self.subject.name} with {self.teacher.name} "
                f"for {self.student_group.name} in {self.room.name} "
                f"at {self.timeslot}")
