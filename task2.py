from flask import request
import json
from flask_marshmallow import Marshmallow, fields


def menu(self):
    run = True
    while run:
        choice = int(
            input('co chcesz zrobić? 1 - dodać notatkę, 2 - usunąć notatkę, 3 - zobaczyć notatki,'
                  ' 4 - edytować notatki: '))
        if choice == 1:
            self.add_note()
        elif choice == 2:
            self.delete_note()
        elif choice == 3:
            self.show_notes()
        elif choice == 4:
            self.edit_note()


def add_note(self):
    title = input('tytuł notatki: ')
    note = input('treść notatkę: ')
