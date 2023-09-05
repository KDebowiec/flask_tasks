import requests


def menu():
    run = True

    while run:
        print("1.Dodaj notatkę, 2.Usuń notatkę, 3.Wyświetl wszystkie notatki, 4.Edytuj notatkę, 5. zamknij")
        choice = int(input("co chcesz zrobić: "))

        if choice == 1:
            new_note = input('wpisz notatke: ')
            requests.post('http://localhost:5000/note',
                          json={
                              "content": new_note
                          })

        elif choice == 2:
            note_id = int(input('podaj id notatki: '))
            requests.delete(f'http://localhost:5000/note/{note_id}')

        elif choice == 3:
            requests.get('http://localhost:5000/notes')

        elif choice == 4:
            note_id = int(input('podaj id notatki: '))
            new_content = input('nowa treść notatki: ')
            requests.put(f'http://localhost:5000/note/{note_id}',
                         json={
                             "content": new_content
                         })
        elif choice == 5:
            run = False


menu()