import json

def load_contacts():
    try:
        with open('contacts.json', 'r') as file:
            contacts = json.load(file)
    except FileNotFoundError:
        contacts = {}
    return contacts

def save_contacts(contacts):
    with open('contacts.json', 'w') as file:
        json.dump(contacts, file)

def display_menu():
    print("\nCommand-line Contact Management System")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Exit")

def add_contact(contacts):
    name = input("Enter contact name: ")
    if name in contacts:
        print("Contact already exists!")
    else:
        phone = input("Enter contact phone number: ")
        email = input("Enter contact email: ")
        contacts[name] = {'Phone': phone, 'Email': email}
        print("Contact added successfully!")

def search_contact(contacts):
    name = input("Enter contact name to search: ")
    if name in contacts:
        print(f"Contact Information for {name}:")
        print(f"Phone: {contacts[name]['Phone']}")
        print(f"Email: {contacts[name]['Email']}")
    else:
        print("Contact not found!")

def update_contact(contacts):
    name = input("Enter contact name to update: ")
    if name in contacts:
        print(f"Current Contact Information for {name}:")
        print(f"Phone: {contacts[name]['Phone']}")
        print(f"Email: {contacts[name]['Email']}")
        phone = input("Enter new phone number (press enter to keep current): ")
        email = input("Enter new email (press enter to keep current): ")
        if phone:
            contacts[name]['Phone'] = phone
        if email:
            contacts[name]['Email'] = email
        print("Contact updated successfully!")
    else:
        print("Contact not found!")

def main():
    contacts = load_contacts()

    while True:
        display_menu()

        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            search_contact(contacts)
        elif choice == '3':
            update_contact(contacts)
        elif choice == '4':
            save_contacts(contacts)
            print("Exiting Contact Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()

