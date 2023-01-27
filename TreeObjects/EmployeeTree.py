from OrganisationObjects.Boss import Boss
from Utility import util
from Utility.util import contains_number

"""
EMPLOYEETREE - object that represents our unordered tree data structure allowing us to represent the hierarchical
nature of an organisation. This allows us to create a root value which has children, which also may or may not have
further children nodes. These links to create the structure representing a company.
"""


class EmployeeTree:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self  # set the parent to the tree that was invoking this method
        self.children.append(child)  # then add to the children of that object to the object passed in

    def get_level(self):  # count how many parents node has to get level
        level = 0  # initialise root as level 0
        parent_node = self.parent
        while parent_node:  # if it has a parent node, increment level
            level += 1
            parent_node = parent_node.parent  # reset parent node
        return level

    def print_tree(self, sort=False):
        spaces = ' ' * self.get_level() * 3  # if level is 2, then 2 * 3 spaces
        prefix = spaces + "|--" if self.parent else ""
        if type(self.data) is Boss:
            print(prefix, self.data.name)
        else:
            print(prefix, self.data.firstname, self.data.surname, "(", self.data.job_title, ")")
        if self.children:
            if sort is True:
                #self.children = util.sort_by_name(self.children)
                #self.children = util.quick_sort(self.children, 0, len(self.children) - 1)
                self.children = util.insertion_sort(self.children)

                for child in self.children:
                    child.print_tree(sort=True)
            else:
                for child in self.children:
                    child.print_tree()

    # will find employees with EXACT match
    def find_employees_by_name_exact(self, job_title=None, uin=None, firstname=None, surname=None,
                                     employees_found=None):
        if employees_found is None:
            employees_found = []

        # DEPTH FIRST TRAVERSAL
        # iterate over the children held in the current object
        for child in self.children:
            # depending on the parameter passed in, look to see whether there is a match with the current child node
            if uin is not None:
                if str(child.data.uin) == uin: # if there is a match, then we can add the current node to the 'found' list
                    employees_found.append(child)
                # otherwise we use recursion to go deeper into the tree, searching the child nodes children
                child.find_employees_by_name_exact(uin=uin, employees_found=employees_found)  # recurse with children
            elif firstname is not None and surname is not None:
                if firstname == child.data.firstname and surname == child.data.surname:
                    employees_found.append(child)
                child.find_employees_by_name_exact(firstname=firstname, surname=surname,
                                                   employees_found=employees_found)  # recurse with children
            elif job_title is not None:
                if job_title == child.data.job_title:
                    employees_found.append(child)
                child.find_employees_by_name_exact(job_title=job_title,
                                                   employees_found=employees_found)  # recurse with children

        if employees_found:
            return employees_found
        else:
            return False  # if no matches found, tell calling function that

    # function to determine what type of search we are executing on the tree
    def filter_search(self, value_type):
        if value_type == "name":
            while True:
                firstname = input("Enter the firstname: ")
                if len(firstname.strip()) == 0 or contains_number(firstname):
                    print("Not an appropriate choice.")
                else:
                    break

            while True:
                surname = input("Enter the surname: ")
                if len(surname.strip()) == 0 or contains_number(surname):
                    print("Not an appropriate choice.")
                else:
                    break

            return self.find_employees_by_name_exact(firstname=firstname.capitalize(),
                                                     surname=surname.capitalize())
        elif value_type == "uin":
            while True:
                uin = input("Enter the uin: ")
                if len(uin.strip()) == 0:
                    print("Not an appropriate choice.")
                else:
                    break
            return self.find_employees_by_name_exact(uin=uin)

        elif value_type == "job_title":
            while True:
                job_title = input("Enter the job title: ")
                if len(job_title.strip()) == 0 or contains_number(job_title):
                    print("Not an appropriate choice.")
                else:
                    break
            return self.find_employees_by_name_exact(job_title=job_title)
        else:
            return False
