import sys
import time
import pandas as pd
from OrganisationObjects.Boss import Boss
from OrganisationObjects.Employee import Employee
from TreeObjects.EmployeeTree import EmployeeTree
from Utility.util import get_input_from_user

"""
BT offers an internal directory for all employee's to use. With the user of a 'power search' we can search by OUC which
is BT's division codes. This allows us to see the majority of employee's in the 'Global' department. 

However, the search is not perfect for organisational hierarchy purposes. The top levels of the chart are not ideal,
the top and second level data had to be taken from elsewhere and placed in manually to complete the chart.
I.e. 
Bas Burger
    |--Chet
    |--James
    |--Joris
"""

""" 
DATAFRAME - these functions relate to processing the information within the CSV file that we are processing.
It is important to process the dataset before executing any further searches or modifications made by the user.
"""


# Function takes in a whole dataframe and will create a Employee out of the row specified
# The init of this object takes in quite a few attributes so it is easier to do it this way and also reduces code
def create_employee(org_chart_df, row_number):
    return Employee(org_chart_df['Surname'][row_number], org_chart_df['Initials'][row_number],
                    org_chart_df['First Name'][row_number],
                    org_chart_df['Title'][row_number], org_chart_df['OUC'][row_number],
                    org_chart_df['Job Title'][row_number],
                    org_chart_df['UIN'][row_number], org_chart_df['Tel'][row_number],
                    org_chart_df['Mobile'][row_number],
                    org_chart_df['Manager UIN'][row_number], org_chart_df['Manager name'][row_number],
                    org_chart_df['Building Code'][row_number],
                    org_chart_df['Country'][row_number])


# 1. iterate through row, create employee node, find UIN
# 2. search for occurrences of that UIN in manager column
# 3. create employee node of those occurrences, and add to children of original
# 4. if UIN is already in tree, then don't repeat
def find_team_members(data_frame, manager_node):
    if type(
            manager_node) is Boss:  # if the node passed in is the boss (of whole company/tree) then make it the root node by initialising the tree with it
        manager_node = EmployeeTree(manager_node)

    boss_team_members = data_frame.loc[data_frame['Manager UIN'] == manager_node.data.uin]  # find instances of manager
    if not boss_team_members.empty:  # if this person is a manager and has team members
        for row_number in boss_team_members.index:  # iterate over each team member
            new_team_member = EmployeeTree(
                create_employee(data_frame, row_number))  # create employee object from the retrieved row
            manager_node.add_child(
                new_team_member)  # add that employee object to be a child of that manager in the tree
            find_team_members(data_frame,
                              new_team_member)  # recurse so we find every employee and team members down the tree
    return manager_node


# Function takes in dataframe of organisation and returns the boss
# The boss, is the top node in the Tree data object we are creating
# The boss does not have as many attributes as a usual employee as it is is simply inferred from the dataset
# There is a name mentioned in the 'manager' section but does not appear in the 'employee' section, meaning that person
# is at the top of that tree
def find_boss(data_frame):
    # FIND BOSS
    for row in data_frame.index:
        manager_uin = data_frame['Manager UIN'][row]  # find current row employee's manager's UIN

        manager_row = data_frame.loc[
            data_frame['UIN'] == manager_uin]  # look to see if the managers UIN occurs in the employee section
        if manager_row.empty:  # if it doesn't occur then this is the top level staff as it has no parents/managers
            return Boss(data_frame['Manager name'][row], manager_uin)


""" 
MENU - all functions directly related to displaying console menu options to the user.
"""


def menu(df=None, boss=None, root_of_tree=None):
    # below if statement will determine whether to process the CSV file again or not
    # the excel file should not be processed if already done, only on the first time of executing the process
    # this is done to improve efficiency of code
    if (df is None or boss is None or root_of_tree is None) or df.empty:
        # read csv file into pandas dataframe object
        df = pd.read_csv("Utility/orgChart.csv")

        # find the top node of the tree, aka the boss of this whole section of the organisation
        boss = find_boss(df)

        # FIND TEAM MEMBERS OF TOP DOG
        root_of_tree = find_team_members(df, boss)

        # first time entering, processing data and so we must welcome user
        print(
            "Welcome to your organisation chart! This application will allow you to search through your company's hierarchy of employee's")
    else:
        # already entered and processed data, so user can have different message
        print("Welcome back to the menu!")

    # define options for user to choose from
    print("From the options below please select what you would like to do.('1' or '2' or '3' etc.):")
    menu_options = {
        "1": "Display whole organisation chart",
        "2": "Search for employee by exact name match",
        "3": "Find by UIN",
        "4": "Find all employees matching Job Title"
    }
    print(menu_options)

    option_choice = get_input_from_user("Please enter your choice: ", ("1", "2", "3", "4"))

    # call function dependent on answer
    if option_choice == "1":
        print_tree(root_of_tree)
    elif option_choice == "2":
        search_by_exact_match(root_of_tree, "name")  # find node(s) by name
    elif option_choice == "3":
        search_by_exact_match(root_of_tree, "uin")  # find node(s) by uin
    elif option_choice == "4":
        search_by_exact_match(root_of_tree, "job_title")  # find node(s) by job title

    navigate_menu()


def navigate_menu(df=None, boss=None, root_of_tree=None):
    menu_or_exit = get_input_from_user(
        "Enter 'Menu' to return to the main text menu, or 'Exit' to exit the application.", ("Menu", "Exit"))

    if menu_or_exit.capitalize() == "Menu":  # return to menu
        print("\n\n")
        menu(df, boss, root_of_tree)
    elif menu_or_exit.capitalize() == "Exit":  # exit the application completely (force shutdown)
        print("\n\nThanks for using the Organisation Chart. Now exiting", end='')
        time.sleep(0.5)
        print(".", end='')  # animate loading dots for user effect
        time.sleep(0.5)
        print(".", end='')
        time.sleep(0.5)
        print(".\n\n", end='')
        sys.exit()


def search_by_exact_match(root_of_tree, value_type):
    # use OOP methods to search entire tree object and retrieve all matches
    employees_found = root_of_tree.filter_search(value_type)

    if employees_found:  # if any matches have been found
        if len(employees_found) > 1:  # determine whether multiple matches were found for messages purposes
            message = "Multiple employees found"
        else:
            message = "Employee found"
        attributes_to_display = input(
            f"{message} - which attributes would you like to display?\n1. Surname\n2. Initials\n3. First Name\n4. Title\n5. OUC\n6. Job Title\n7. UIN\n8. Telephone\n9. Mobile\n10. Manager UIN\n11. Manager name\n12.Building code\n13. Country\n14. All attributes\nPlease enter in format (1, 2, 3..): ")

        # if employee(s) found, iterate through and display their attributes
        for e in employees_found:
            e.data.select_and_pretty_print(attributes_to_display)

        # optionally display everyone under this employee in the tree
        expand = get_input_from_user(
            "Would you like to see everyone under this employee's management? (Yes/Y/No/N)", ("Yes", "Y", "No", "N"))

        if expand.capitalize() == "Yes" or expand.capitalize() == "Y":
            for e in employees_found:
                if e.children:
                    print_tree(e)
                else:
                    print(f"{e.data.firstname} {e.data.surname} is not a manager. So this can not be expanded.\n")
    else:
        print("Employee not found.")

    # optionally search again or return to menu or exit applications
    search_again = get_input_from_user(
        "Would you like to search again? (Yes/Y/No/N)", ("Yes", "Y", "No", "N"))

    if search_again.capitalize() == "Yes" or search_again.capitalize() == "Y":
        search_by_exact_match(root_of_tree, value_type)
    else:
        navigate_menu()


# function to display all employees under current node
# this has been created so that the code to ask the user if they want to sort by name does not have to be repeated
def print_tree(root_node):
    # optionally sort data by name
    search_again = get_input_from_user(
        "Would you like to sort it by first name in alphabetical order? (Yes/Y/No/N)", ("Yes", "Y", "No", "N"))

    if search_again.capitalize() == "Yes" or search_again.capitalize() == "Y":
        root_node.print_tree(sort=True)
    else:
        root_node.print_tree(sort=False)


# must call menu function to execute console code for the user
menu()
