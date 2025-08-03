import unittest
from models import Subject, Teacher, StudentGroup, Room, TimeSlot, Lesson
from scheduler import Scheduler

class TestSchedulerConstraints(unittest.TestCase):
    def setUp(self):
        """Set up a scheduler and some sample data for each test."""
        self.teacher1 = Teacher("Lehrer A")
        self.group1 = StudentGroup("Klasse 1", 10)
        self.room1 = Room("Raum A", 15)
        self.slot1 = TimeSlot("Montag", "08:00", "08:45")
        self.slot2 = TimeSlot("Montag", "09:00", "09:45")
        self.subject1 = Subject("Mathe")

        # Create a scheduler instance with minimal data needed for constraint tests
        # The scheduler's main data lists are not used by the constraint helpers,
        # which only depend on the `timetable` list.
        self.scheduler = Scheduler({
            "subjects": [], "teachers": [], "student_groups": [], "rooms": [], "timeslots": []
        })

    def test_teacher_availability(self):
        """Test the _is_teacher_available constraint."""
        # Initially, the teacher should be available
        self.assertTrue(self.scheduler._is_teacher_available(self.teacher1, self.slot1))

        # Add a lesson to the timetable
        lesson = Lesson(self.subject1, self.teacher1, self.group1, self.room1, self.slot1)
        self.scheduler.timetable.append(lesson)

        # Now, the teacher should NOT be available at the same time slot
        self.assertFalse(self.scheduler._is_teacher_available(self.teacher1, self.slot1))

        # But the teacher should be available at a different time slot
        self.assertTrue(self.scheduler._is_teacher_available(self.teacher1, self.slot2))

    def test_student_group_availability(self):
        """Test the _is_student_group_available constraint."""
        self.assertTrue(self.scheduler._is_student_group_available(self.group1, self.slot1))
        lesson = Lesson(self.subject1, self.teacher1, self.group1, self.room1, self.slot1)
        self.scheduler.timetable.append(lesson)
        self.assertFalse(self.scheduler._is_student_group_available(self.group1, self.slot1))
        self.assertTrue(self.scheduler._is_student_group_available(self.group1, self.slot2))

    def test_room_availability(self):
        """Test the _is_room_available constraint."""
        self.assertTrue(self.scheduler._is_room_available(self.room1, self.slot1))
        lesson = Lesson(self.subject1, self.teacher1, self.group1, self.room1, self.slot1)
        self.scheduler.timetable.append(lesson)
        self.assertFalse(self.scheduler._is_room_available(self.room1, self.slot1))
        self.assertTrue(self.scheduler._is_room_available(self.room1, self.slot2))

    def test_room_suitability(self):
        """Test the _is_room_suitable constraint."""
        special_subject = Subject("Sport", requires_special_room=True)
        normal_room = Room("Raum B", 10, is_special_room=False)
        special_room = Room("Turnhalle", 20, is_special_room=True)
        small_room = Room("Besprechung", 5, is_special_room=False)

        # Normal subject in normal room is fine
        self.assertTrue(self.scheduler._is_room_suitable(self.subject1, normal_room, self.group1))
        # Special subject needs special room
        self.assertFalse(self.scheduler._is_room_suitable(special_subject, normal_room, self.group1))
        self.assertTrue(self.scheduler._is_room_suitable(special_subject, special_room, self.group1))
        # Room must have enough capacity
        self.assertFalse(self.scheduler._is_room_suitable(self.subject1, small_room, self.group1))

if __name__ == '__main__':
    unittest.main()


class TestSchedulerGeneration(unittest.TestCase):
    def setUp(self):
        """Set up a realistic set of data for generation tests."""
        self.subjects = [Subject("Deutsch"), Subject("Mathe")]
        self.teachers = [Teacher("Lehrer A")]
        self.student_groups = [StudentGroup("Klasse 1", 10)]
        self.rooms = [Room("Raum 101", 10)]
        self.timeslots = [
            TimeSlot("Montag", "08:00", "08:45"),
            TimeSlot("Montag", "09:00", "09:45")
        ]
        self.school_data = {
            "subjects": self.subjects,
            "teachers": self.teachers,
            "student_groups": self.student_groups,
            "rooms": self.rooms,
            "timeslots": self.timeslots
        }

    def test_successful_generation(self):
        """Test that a valid timetable is generated when possible."""
        lessons_to_schedule = [
            {'subject': 'Deutsch', 'teacher': 'Lehrer A', 'student_group': 'Klasse 1'},
            {'subject': 'Mathe', 'teacher': 'Lehrer A', 'student_group': 'Klasse 1'},
        ]
        # With 1 teacher and 2 timeslots, this should be possible.
        scheduler = Scheduler(self.school_data)
        timetable = scheduler.generate_timetable(lessons_to_schedule)

        self.assertIsNotNone(timetable)
        self.assertEqual(len(timetable), 2)

    def test_failed_generation(self):
        """Test that the scheduler returns None when a timetable is impossible."""
        lessons_to_schedule = [
            {'subject': 'Deutsch', 'teacher': 'Lehrer A', 'student_group': 'Klasse 1'},
            {'subject': 'Mathe', 'teacher': 'Lehrer A', 'student_group': 'Klasse 1'},
            {'subject': 'Deutsch', 'teacher': 'Lehrer A', 'student_group': 'Klasse 1'},
        ]
        # With only 1 teacher and 2 timeslots, scheduling 3 lessons is impossible.
        scheduler = Scheduler(self.school_data)
        timetable = scheduler.generate_timetable(lessons_to_schedule)

        self.assertIsNone(timetable)
