from models import Subject, Teacher, StudentGroup, Room, TimeSlot, Lesson
from typing import List, Dict, Optional

class Scheduler:
    """
    Handles the logic of generating a valid timetable based on a set of constraints.
    """
    def __init__(self, data: Dict):
        self.subjects: List[Subject] = data["subjects"]
        self.teachers: List[Teacher] = data["teachers"]
        self.student_groups: List[StudentGroup] = data["student_groups"]
        self.rooms: List[Room] = data["rooms"]
        self.timeslots: List[TimeSlot] = data["timeslots"]
        self.timetable: List[Lesson] = []

    def _is_teacher_available(self, teacher: Teacher, timeslot: TimeSlot) -> bool:
        """Checks if the teacher is already booked for the given timeslot."""
        for lesson in self.timetable:
            if lesson.teacher.id == teacher.id and lesson.timeslot.id == timeslot.id:
                return False
        return True

    def _is_student_group_available(self, student_group: StudentGroup, timeslot: TimeSlot) -> bool:
        """Checks if the student group is already in a lesson at the given timeslot."""
        for lesson in self.timetable:
            if lesson.student_group.id == student_group.id and lesson.timeslot.id == timeslot.id:
                return False
        return True

    def _is_room_available(self, room: Room, timeslot: TimeSlot) -> bool:
        """Checks if the room is already booked for the given timeslot."""
        for lesson in self.timetable:
            if lesson.room.id == room.id and lesson.timeslot.id == timeslot.id:
                return False
        return True

    def _is_room_suitable(self, subject: Subject, room: Room, student_group: StudentGroup) -> bool:
        """Checks if the room is suitable for the subject and has enough capacity."""
        if subject.requires_special_room and not room.is_special_room:
            return False
        if room.capacity < student_group.size:
            return False
        return True

    def find_available_slot(self, subject: Subject, teacher: Teacher, student_group: StudentGroup) -> Optional[Lesson]:
        """A simple method to find the first available slot (for initial testing)."""
        for timeslot in self.timeslots:
            for room in self.rooms:
                if (self._is_teacher_available(teacher, timeslot) and
                    self._is_student_group_available(student_group, timeslot) and
                    self._is_room_available(room, timeslot) and
                    self._is_room_suitable(subject, room, student_group)):

                    lesson = Lesson(subject, teacher, student_group, room, timeslot)
                    self.timetable.append(lesson)
                    return lesson
        return None

    def generate_timetable(self, lessons_to_schedule: List[Dict]) -> Optional[List[Lesson]]:
        """
        Main backtracking method to generate the full timetable.
        `lessons_to_schedule` is a list of dicts, e.g.,
        [{'subject': 'Deutsch', 'teacher': 'Herr Meier', 'student_group': 'Klasse A'}, ...]
        """
        # Base case: If there are no more lessons to schedule, we are done.
        if not lessons_to_schedule:
            return self.timetable

        # Take the next lesson to be scheduled
        lesson_request = lessons_to_schedule[0]
        remaining_lessons = lessons_to_schedule[1:]

        subject_name = lesson_request['subject']
        teacher_name = lesson_request['teacher']
        group_name = lesson_request['student_group']

        # Find the actual objects from the names
        subject = next((s for s in self.subjects if s.name == subject_name), None)
        teacher = next((t for t in self.teachers if t.name == teacher_name), None)
        student_group = next((sg for sg in self.student_groups if sg.name == group_name), None)

        if not all([subject, teacher, student_group]):
            print(f"Error: Could not find matching data for request {lesson_request}")
            return self.generate_timetable(remaining_lessons) # Skip invalid request

        # Try to place this lesson in any available timeslot and room
        for timeslot in self.timeslots:
            for room in self.rooms:
                # Check all constraints
                if (self._is_teacher_available(teacher, timeslot) and
                    self._is_student_group_available(student_group, timeslot) and
                    self._is_room_available(room, timeslot) and
                    self._is_room_suitable(subject, room, student_group)):

                    # If valid, create the lesson and add it to the current timetable
                    new_lesson = Lesson(subject, teacher, student_group, room, timeslot)
                    self.timetable.append(new_lesson)

                    # Recursively try to schedule the rest of the lessons
                    result = self.generate_timetable(remaining_lessons)
                    if result:
                        return result # Success!

                    # Backtrack: If the recursive call failed, undo the choice
                    self.timetable.pop()

        # If we get here, we couldn't find a place for the current lesson, so backtrack
        return None
