from collections import defaultdict
from models import Subject, Teacher, StudentGroup, Room, TimeSlot, Lesson
from scheduler import Scheduler
from typing import List

def setup_data():
    """Sets up the initial data for the school."""
    # Fächer (Subjects)
    deutsch = Subject(name="Deutsch")
    mathe = Subject(name="Mathematik")
    sport = Subject(name="Sport", requires_special_room=True)

    # Lehrer (Teachers)
    herr_meier = Teacher(name="Herr Meier")
    frau_schmidt = Teacher(name="Frau Schmidt")

    # Schülergruppen (Student Groups)
    klasse_a = StudentGroup(name="Klasse A", size=8)
    klasse_b = StudentGroup(name="Klasse B", size=7)

    # Räume (Rooms)
    raum_101 = Room(name="Raum 101", capacity=10)
    raum_102 = Room(name="Raum 102", capacity=10)
    turnhalle = Room(name="Turnhalle", capacity=20, is_special_room=True)

    # Zeitfenster (Time Slots)
    timeslots = [
        TimeSlot(day="Montag", start_time="08:00", end_time="08:45"),
        TimeSlot(day="Montag", start_time="08:45", end_time="09:30"),
        TimeSlot(day="Dienstag", start_time="08:00", end_time="08:45"),
        TimeSlot(day="Dienstag", start_time="08:45", end_time="09:30"),
    ]

    return {
        "subjects": [deutsch, mathe, sport],
        "teachers": [herr_meier, frau_schmidt],
        "student_groups": [klasse_a, klasse_b],
        "rooms": [raum_101, raum_102, turnhalle],
        "timeslots": timeslots
    }

class TimetableCLI:
    """Handles the Command-Line Interface for the timetable program."""
    def __init__(self):
        self.school_data = setup_data()
        self.lessons_to_schedule = []

    def display_menu(self):
        """Prints the main menu and gets user choice."""
        print("\n--- Stundenplan-Programm Hauptmenü ---")
        print("1. Schuldaten anzeigen (Lehrer, Fächer, etc.)")
        print("2. Zu planende Stunden definieren (Beispieldaten)")
        print("3. Stundenplan generieren und anzeigen")
        print("4. Beenden")
        return input("Wählen Sie eine Option: ")

    def run(self):
        """Main loop for the CLI."""
        print("CLI wird im Demo-Modus ausgeführt...")
        self.define_lessons()
        self.generate_and_show_timetable()

    def view_data(self):
        """Displays the current school data."""
        print("\n--- Aktuelle Schuldaten ---")
        for key, value in self.school_data.items():
            print(f"\n{key.capitalize()}:")
            if not value:
                print("- Keine Daten vorhanden.")
            for item in value:
                print(f"- {item}")

    def define_lessons(self):
        """Defines a sample list of lessons to be scheduled."""
        print("\n--- Stunden definieren ---")
        self.lessons_to_schedule = [
            {'subject': 'Deutsch', 'teacher': 'Herr Meier', 'student_group': 'Klasse A'},
            {'subject': 'Mathematik', 'teacher': 'Frau Schmidt', 'student_group': 'Klasse B'},
            {'subject': 'Mathematik', 'teacher': 'Frau Schmidt', 'student_group': 'Klasse A'},
            {'subject': 'Deutsch', 'teacher': 'Herr Meier', 'student_group': 'Klasse B'},
            {'subject': 'Sport', 'teacher': 'Herr Meier', 'student_group': 'Klasse A'},
        ]
        print(f"{len(self.lessons_to_schedule)} Stunden wurden zur Planung hinzugefügt.")

    def generate_and_show_timetable(self):
        """Generates and displays the timetable."""
        if not self.lessons_to_schedule:
            print("\nFehler: Bitte zuerst die zu planenden Stunden definieren (Option 2).")
            return
            
        print("\nGeneriere Stundenplan...")
        scheduler = Scheduler(self.school_data)
        timetable = scheduler.generate_timetable(self.lessons_to_schedule)

        if timetable:
            print("\n--- Stundenplan erfolgreich erstellt ---")
            self.display_timetable_as_grid(timetable)
        else:
            print("\n--- Es konnte kein gültiger Stundenplan erstellt werden. ---")
            print("Mögliche Gründe: Zu wenige Zeitfenster, Räume oder Lehrer für die angeforderten Stunden.")

    def display_timetable_as_grid(self, timetable: List[Lesson]):
        """Displays the timetable in a visual grid format."""
        grid = defaultdict(dict)
        
        # Define the correct order for the days of the week to ensure correct sorting
        day_order = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        
        present_days = set(l.timeslot.day for l in timetable)
        # Sort the days based on the predefined order
        days = sorted(list(present_days), key=lambda d: day_order.index(d) if d in day_order else float('inf'))

        time_slots_str = sorted(list(set(f"{l.timeslot.start_time}-{l.timeslot.end_time}" for l in timetable)))

        for lesson in timetable:
            time_key = f"{lesson.timeslot.start_time}-{lesson.timeslot.end_time}"
            grid[time_key][lesson.timeslot.day] = lesson

        # --- Print the grid ---
        # Header
        header = f"| {'Zeit':<12} |" + " | ".join([f"{day:<25}" for day in days]) + " |"
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        # Rows
        for time_str in time_slots_str:
            row_str = f"| {time_str:<12} |"
            for day in days:
                lesson = grid[time_str].get(day)
                if lesson:
                    cell_content = f"{lesson.student_group.name}: {lesson.subject.name} ({lesson.teacher.name}) @ {lesson.room.name}"
                    row_str += f" {cell_content:<25} |"
                else:
                    row_str += f" {'':<25} |"
            print(row_str)

        print("-" * len(header))

def main():
    """Main function to start the CLI."""
    cli = TimetableCLI()
    cli.run()

if __name__ == "__main__":
    main()
