# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date
import time

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def valid_username(name, in_list = True):
    """Function checks user has input valid username and allows them to retry or leave if not"""
    # Loop to check if name is in list of username passwords
    while in_list:
        if name not in username_password:
            # Returns exit so user is returned to menu
            if name == "exit":
                return "exit"
            name = input("User does not exist. Please enter a valid username or enter exit to go back to menu\n").lower()
        # If name in list allows user to continue
        else:
            return name
    # Loop to check if name is not in list of username passwords
    while not in_list:
        if name in username_password:
            if name == "exit":
                return "exit"
            name = input("User already exists. Please enter a new username or enter exit to go back to menu\n").lower()
        # If name not in list allows user to continue
        else:
            return NameError
        
def due_date_collection():
    """Function asks user for a due date only allowing times in the future and datetime date format"""
    while True:
        try:
            due_date_time = datetime.strptime(input("Due date of task (YYYY-MM-DD): "), DATETIME_STRING_FORMAT)
            # - Checks due date is in the future
            if due_date_time.date() < date.today():
                print("Date cannot be in the past. Please re-enter date")
            else: 
                # Returns due date in correct format
                return due_date_time
        # If user inputs datetime format allows tells them to retry
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

def save_task_list():
    """Function saves the list task_list used throughout program to the tasks text file in the correct format"""
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        #Creates a list of the tasks in strings to save to the txt file
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

def task_editor(new_value,edit_list,task_value: str):
    "Function that edits different parts of the task_list variable"
    counter = 0
    for tasks in task_list:
        if edit_list in tasks.values():
            task_list[counter][task_value] = new_value
        counter += 1

def reg_user():
    """Function adds a new user to the user.txt file"""
    # - Request input of a new username and check that it doesn't already exist
    new_username = input("New Username: ").lower()
    new_username = valid_username(new_username,False)
    if new_username == "exit":
        return
    # - Request input of a new password
    new_password = input("New Password: ")
    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        #Creates a list of the key:values in the dictionary and saves them to user.txt
        with open("user.txt", "w") as out_file:
            save_user_data = []
            for k in username_password:
                save_user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(save_user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")
    time.sleep(1.5)

def add_task():
    '''
    Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.
    '''
    task_username = input("Name of person assigned to task: ").lower()
    task_username = valid_username(task_username)
    if task_username == "exit": 
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
        # -Gets the current date.
    due = due_date_collection()
    #Adds the new task to the task.txt file as incomplete
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due,
        "assigned_date": date.today(),
        "completed": False
    }

    task_list.append(new_task)
    save_task_list()
    print("Task successfully added.")
    time.sleep(1.5)

def view_all():
    '''
    Reads all tasks from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Completed: \t {t['completed']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
    time.sleep(3)


def view_mine():
    '''
    Reads the users tasks from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling). Then allows user to edit tasks and mark them completed
    '''
    curr_user_task_info = []
    edit_task_info = []
    counter = 0
    print("\n\nEnter task number for more information or -1 to return to menu")
    print("Tasks:")
    for t in task_list:
        if t['username'] == curr_user:
            #Counter to allow readability of tasks for user
            counter += 1
            #Creates a display string for the user information for the reader to drill into
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Completed: \t {t['completed']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            curr_user_task_info.append(disp_str)
            print(f"{counter}. {t['title']}\n{t['description']}")
            #Creates lists of editable attributes of tasks to be changed later in function
            edit_task_info.append([t['title'],t['due_date']])
    #Check that user input is a number from the options or returns to menu if -1
    while True:
        try:
            drill = int(input())
            if  0 < drill <= counter:
                break
            elif drill == -1:
                return
            else: 
                print("Please enter one of the given options")
        except ValueError:
            print("Please enter a number")
    print("\n" + curr_user_task_info[drill-1])
    # Checks to see if the selected task has been completed before giving the option of editing
    for tasks in task_list:
        if tasks['completed'] and tasks['title'] == edit_task_info[drill-1][0]:
            print("Task has been completed and can not be edited.")
            time.sleep(5) 
            return
    
    ed_count = 1
    #Matches to the edit count variable which allows the user to choose whether or not to edit certain parts
    while True:
        match ed_count:
            case 1:
                edit = input("Would you like to edit the task?\n").lower()
                #if user says no skips to asking if task is finished
                if edit == "no":
                    ed_count = 3
            case 2:
                edit = input("Would you like to change who the task is assigned to?\n").lower()
            case 3:
                edit = input("Would you like to change the due date of the task?\n").lower()
            case 4:
                edit = input("Has the Task been completed?\n").lower()
            # breaks loop
            case 5:
                break
        if edit == "yes":
            match ed_count:
                case 2:
                    # Checks for valid username input then edits who the task is assigned to
                    name = input("Who would you like to assigned the task to?\n").lower()
                    name = valid_username(name)
                    # Allows user to return to menu
                    if name == "exit": 
                        return
                    task_editor(name,edit_task_info[drill-1][0],"username")
                case 3:
                    # Collects valid due date then changes the due date of task
                    due = due_date_collection()
                    task_editor(due,edit_task_info[drill-1][1],"due_date")
                case 4:
                    # Changes the task to complete
                    task_editor(True,edit_task_info[drill-1][0],"completed")
            ed_count += 1
        elif edit == "no":
            ed_count += 1
        # Only allows the user input of yes or no else loops again
        else:
            print("Please enter either yes or no")
    #Saves edits to the task list text file
    save_task_list()
    print("Changes successfully saved.")
    time.sleep(1.5)

def generate_report():
    """
    Function that generates text file reports of task and user information
    Creates a Task overview file that displays:
    - number of tasks
    - number of completed tasks
    - number of incomplete tasks
    - number of overdue tasks
    - Percentages of each of these numbers

    Creates User overview file that contains:
    - Total number of users being managed
    - Total number of tasks
    - Then for each user:
        - Total number of tasks assigned to user
        - Percentage of total tasks assigned to that user
        - The percentage of tasks assigned to user that have been completed
        - The percentage of tasks that have been assigned to that user that must still be completed
        - The Percentage of incomplete and overdue tasks a user has
    """
    finished = 0
    unfinished = 0
    unfinished_and_over = 0
    user_tasks = []
    # Creates list of dictionaries, with each dictionary holding user specific task information
    for names in username_password.keys():
        curr_u = {}
        curr_u['username'] = names
        curr_u['finished'] = 0
        curr_u['unfinished'] = 0
        curr_u['unfinished_and_over'] = 0
        user_tasks.append(curr_u)
    
    # Iterates for the number of tasks, adding to a counter for finished and unfinished throughout
    for tasks in task_list:
        match tasks['completed']:
            case True:
                finished += 1
                #Loops through user_tasks list to add to each individual's list of task info
                for x,users in enumerate(user_tasks):
                    if tasks['username'] == users['username']:
                        user_tasks[x]['finished'] += 1
            case False:
                unfinished += 1
                for x,users in enumerate(user_tasks):
                    if tasks['username'] == users['username']:
                        user_tasks[x]['unfinished'] += 1
                # Checks due date against today's date to check if due
                if tasks['due_date'].date() < date.today():
                    unfinished_and_over += 1
                    for x,users in enumerate(user_tasks):
                        if tasks['username'] == users['username']:
                            user_tasks[x]['unfinished_and_over'] += 1
    #String of task information created in a readable fashion
    task_overview = f'''There are currently {len(task_list)} tasks being managed:
{finished} ({finished*100/len(task_list)}%) tasks have been completed.
{unfinished} ({unfinished*100/len(task_list)}%) tasks have not been completed.
with {unfinished_and_over} ({unfinished_and_over*100/len(task_list)}%) of incomplete tasks being overdue.
'''
    # creates and writes a report to a txt file
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(task_overview)

    # For loop to create string of user report information presented in reader friendly way
    user_overview = f"There are currently {len(task_list)} tasks and {len(username_password)} users being managed"
    for individual in user_tasks:
        tot_user_task = individual['finished'] + individual['unfinished']
        user_overview += "\n----------------------------------------"
        user_overview += f"\nUser:\t{str(individual['username'])}"
        user_overview += f"\nTotal number of tasks assigned: {str(tot_user_task)}"
        user_overview += f"\nPercentage of total tasks: \t{str(round(tot_user_task*100/len(task_list),1))}%"
        user_overview += f"\nCompleted:\t\t\t{str(round(individual['finished']/tot_user_task*100,1))}%"
        user_overview += f"\nIncompleted:\t\t\t{str(round(individual['unfinished']/tot_user_task*100,1))}%"
        user_overview += f"\nOverdue:\t\t\t{str(round(individual['unfinished_and_over']/tot_user_task*100,1))}%"
    #Saves Users string to a txt file
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(user_overview)
    print("Generated Reports.")
    # Returns strings of both strings so they can be printed on display stats
    return(task_overview, user_overview)

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}
    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    task_list.append(curr_t)


#====Login Section====
'''
This code reads usernames and password from the user.txt file to 
allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    menu = input('''\nSelect one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == "gr":
        generate_report()
    elif menu == 'ds' and curr_user == 'admin': 
        # If the user is an admin they can display statistics about number of users and tasks.
        overviews = generate_report()
        print("\n-------------------------------------------")
        print(overviews[0])
        print("-------------------------------------------")
        print(overviews[1]) 
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")