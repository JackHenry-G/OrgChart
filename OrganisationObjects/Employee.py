"""
EMPLOYEE - object represents all the employees found in the organisation chart. This is each row of data in the CSV file
and is packaged into a singular object which houses several attributes about each data row. This object will make up
each node in the overall tree. (apart from the root node which is the BOSS object).
"""


class Employee:
    def __init__(self, surname, initials, firstname, title, ouc, job_title, uin, tel, mobile, manager_uin, manager_name,
                 building_code, country):
        self.surname = surname  # 1
        self.initials = initials  # 2
        self.firstname = firstname  # 3
        self.title = title  # 4
        self.ouc = ouc  # 5
        self.job_title = job_title  # 6
        self.uin = uin  # 7
        self.tel = tel  # 8
        self.mobile = mobile  # 9
        self.manager_uin = manager_uin  # 10
        self.manager_name = manager_name  # 11
        self.building_code = building_code  # 12
        self.country = country  # 13
        # 14 = all attributes

    def select_and_pretty_print(self, attribute_list):
        # builds a dictionary object to hold each attribute retrieved form the CSV
        # a dictionary is a key value pair storage option
        # the key acts as a title, and must be unique, in this case would be one of the attributes like 'name'
        # we can then store as many 'value's as we want under this key, such as, 'Jack' or 'Lily'
        returned_attributes = {}

        # the following set of if statements will look at which options the user has passed in
        # and when detected will add the attribute to the above dictionary
        if "1" in attribute_list:
            returned_attributes['Surname'] = self.surname

        if "2" in attribute_list:
            returned_attributes['Initials'] = self.initials

        if "3" in attribute_list:
            returned_attributes['First Name'] = self.firstname

        if "4" in attribute_list:
            returned_attributes['Title'] = self.title

        if "5" in attribute_list:
            returned_attributes['OUC'] = self.ouc

        if "6" in attribute_list:
            returned_attributes['Job title'] = self.job_title

        if "7" in attribute_list:
            returned_attributes['UIN'] = self.uin

        if "8" in attribute_list:
            returned_attributes['Telephone'] = self.tel

        if "9" in attribute_list:
            returned_attributes['Mobile'] = self.mobile

        if "10" in attribute_list:
            returned_attributes['Manager UIN'] = self.manager_uin

        if "11" in attribute_list:
            returned_attributes['Manager Name'] = self.manager_name

        if "12" in attribute_list:
            returned_attributes['Building Code'] = self.building_code

        if "13" in attribute_list:
            returned_attributes['Country'] = self.country

        # 14 option relates to 'all' attributes so add all to the dictionary
        if "14" in attribute_list:
            returned_attributes['Surname'] = self.surname
            returned_attributes['Initials'] = self.initials
            returned_attributes['First Name'] = self.firstname
            returned_attributes['Title'] = self.title
            returned_attributes['OUC'] = self.ouc
            returned_attributes['Job title'] = self.job_title
            returned_attributes['UIN'] = self.uin
            returned_attributes['Telephone'] = self.tel
            returned_attributes['Mobile'] = self.mobile
            returned_attributes['Manager UIN'] = self.manager_uin
            returned_attributes['Manager Name'] = self.manager_name
            returned_attributes['Building Code'] = self.building_code
            returned_attributes['Country'] = self.country

        # uses list comprehension to iterate over the key-value pairs in the dictionary
        # and print them in a more user
        [print(key, ':', value) for key, value in returned_attributes.items()]
