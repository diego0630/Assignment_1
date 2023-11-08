import random
import sqlite3
import csv

conn = sqlite3.connect('StudentDB.sqlite')  # establishes connection to database
mycursor = conn.cursor()  # the cursor allows python to execute SQL statements

advisors = ["Ewan Smith", "Elijah Guerrero", "Matthew Jimenez", "Michael Shen", "Matt Shugarte"]

states = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut",
               "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho",
               "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine",
               "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota",
               "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma",
               "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
               "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia",
               "Wyoming"]


def importData():
    with open('students.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mycursor.execute(
                "INSERT INTO Student('FirstName', 'LastName', 'GPA', 'Major',"
                " 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted')  "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (row['FirstName'], row['LastName'], row['GPA'], row['Major'], random.choice(advisors),
                 row['Address'], row['City'], row['State'], row['ZipCode'], row['MobilePhoneNumber'], 0))



def compareTo(input_val, colNum):
    located = False
    mycursor.execute("SELECT * FROM Student WHERE IsDeleted = 0")
    result = mycursor.fetchall()
    for x in result:
        if (x[colNum] == input_val):
            located = True
    return located




exitProgram = False
programLaunched = True


while (exitProgram != True):

    if (programLaunched == True):
        importData()
        programLaunched = False

    userInput = input(
        '\nEnter "Display" to display all students\nEnter "Add" to add a new student\n'
        'Enter "Update" to update a student\nEnter "Delete" to delete a student\n'
        'Enter "Search" to search for a student\nElse type "Exit" to exit the program\n')

    if (userInput == 'Display'):

        mycursor.execute("SELECT * FROM Student Where isDeleted = 0")
        result = mycursor.fetchall()
        for x in result:
            print(x)

    elif (userInput == 'Add'):

        firstName = input("Enter the first name of the student\n")
        while (firstName.isalpha() != True):
            firstName = input("Please enter an alphabetical value\n")
        lastName = input("Enter the last name of the student\n")
        while (lastName.isalpha() != True):
            lastName = input("Enter an alphabetical value\n")
        gpa = input("Enter the GPA of the student\n")
        gpaExists = False
        while (gpaExists == False):
            if (gpa.replace(".", "").isnumeric() == False):
                gpa = input("Please enter a numerical value\n")
                continue
            if (round(float(gpa)) < 5.0):
                break
            else:
                gpa = input("GPA does not meet requirements, enter another value\n")

        major = input("Enter the major of the student\n")
        while (major.isalpha() != True):
            major = input("Please enter an alphabetical value\n")
        advisor = input("Enter the faculty advisor of the student\n")
        advisorExists = False
        while (advisorExists == False):
            if (advisor.isnumeric() == True):
                advisor = input("Please enter an alphabetical value\n")
                continue
            if (advisor in advisors):
                break
            else:
                advisor = input("Advisor does not exist, enter an existing advisor\n")

        address = input("Enter the address of the student\n")

        city = input("Enter the city of the student\n")
        while (city.isnumeric() == True):
            city = input("Please enter an alphabetical value\n")

        state = input("Enter the state of the student\n")
        stateExists = False
        while (stateExists == False):
            if (state.isnumeric() == True):
                state = input("Please enter an alphabetical value\n")
                continue
            if (state in states):
                break
            else:
                state = input("State does not exist, enter an existing value\n")

        zip = input("Enter the zipcode of the student\n")
        zipExists = False
        while (zipExists == False):
            if (zip.isnumeric() == False):
                zip = input("Please enter a numerical value\n")
                continue
            if (len(zip) == 5):
                break
            else:
                zip = input("Invalid value, please enter a valid zipcode\n")

        phone = input("What is the student's phone number?\n")
        phoneExists = False
        while (phoneExists == False):
            if (phone.isnumeric() == False):
                phone = input('Invalid phone number, enter a valid ten digits of the new phone number\n')
                continue
            if (len(phone) == 10):
                break
            else:
                phone = input("Invalid value, please enter a valid phone")

        mycursor.execute(
            "INSERT INTO Student('StudentId','FirstName', 'LastName', 'GPA',"
            " 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode',"
            " 'MobilePhoneNumber', 'isDeleted')  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (None, firstName, lastName, gpa, major, advisor, address, city, state, zip, phone, 0))

        print("Student added.")

    elif (userInput == 'Update'):
        contain = False
        id = input("Enter the ID of the student\n")
        mycursor.execute("SELECT * FROM Student Where isDeleted = 0")
        result = mycursor.fetchall()

        continueAllowed = False
        while (contain == False):
            if (id.isnumeric() == False):
                id = input("Enter a numeric value\n")
                continue
            else:
                continueAllowed = True
            if (continueAllowed == True):
                for x in result:
                    if (x[0] == int(id)):
                        contain = True
                        break
                if (contain == False):
                    id = input("ID does not exist, enter an existing value\n")

        type = input(
            'What field would you like to update?\nEnter "Major" to update Major field\n'
            'Enter "Advisor" to update Advisor field\nEnter "Phone" to update MobilePhoneNumber field\n')
        if (type == 'Major'):
            major = input('What is the new major for the student?\n')
            majorExists = False
            while (majorExists == False):
                if (major.isnumeric() == True):
                    major = input("Please enter an alphabetical value\n")
                    continue
                majorExists = compareTo(major, 4)
                if (majorExists):
                    mycursor.execute("UPDATE Student SET Major = ? WHERE StudentId = ?", (major, id,))
                    print("Field successfully updated")
                    break
                else:
                    major = input("Major does not exist, enter an existing value\n")
        if (type == 'Advisor'):
            advisor = input('Who is the new advisor for the student?\n')
            advisorExists = False
            while (advisorExists == False):
                if (advisor.isnumeric() == True):
                    advisor = input("Please enter an alphabetical value\n")
                    continue
                if (advisor in advisors):
                    mycursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?", (advisor, id,))
                    print("Field successfully updated")
                    break
                else:
                    advisor = input("Advisor does not exist, enter an existing value\n")
        if (type == 'Phone'):
            phone = input('Enter ten digits of the the new mobile phone number for the student\n')
            phoneExists = False
            while (phoneExists == False):
                if (phone.isnumeric() == False):
                    phone = input('Invalid phone number, enter a different ten digits of the new phone number\n')
                    continue
                if (len(phone) == 10):
                    mycursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?", (phone, id,))
                    print("Field successfully updated")
                    break
                else:
                    phone = input("Phone number does not exist, enter an existing ten digit number")



    elif (userInput == 'Delete'):
        contain = False
        id = input("Enter the ID of the student you would like to delete\n")
        mycursor.execute("SELECT * FROM Student Where isDeleted = 0")
        result = mycursor.fetchall()

        continueAllowed = False
        while (contain == False):
            if (id.isnumeric() == False):
                id = input("Enter a numeric value\n")
                continue
            else:
                continueAllowed = True
            if (continueAllowed == True):
                for x in result:
                    if (x[0] == int(id)):
                        contain = True
                        mycursor.execute("UPDATE Student SET isDeleted = 1 WHERE StudentId = ?", (id,))
                        print("Succesfully deleted")
                        break
                if (contain == False):
                    id = input("ID does not exist\n")

    elif (userInput == 'Search'):
        type = input(
            'What field would you like to search by?\nEnter "Major" to search for Major field\n'
            'Enter "GPA" to search by GPA field\nEnter "City" to search by City field\n'
            'Enter "State" to search by State field\nEnter "Advisor" to search by FacultyAdvisor" field\n')

        if (type == "Major"):
            major = input('What is the major of the student?\n')
            majorExists = False
            while (majorExists == False):
                if (major.isnumeric() == True):
                    major = input("Please enter an alphabetical value\n")
                    continue
                majorExists = compareTo(major, 4)
                if (majorExists):
                    mycursor.execute("SELECT * FROM Student WHERE Major = ? and isDeleted = 0", (major,))
                    result = mycursor.fetchall()
                    for x in result:
                        print(x)
                    break
                else:
                    major = input("Major does not exist, enter an existing value\n")
        if (type == "GPA"):
            gpa = input("Enter the GPA of the student\n")
            gpaExists = False
            while (gpaExists == False):
                if (gpa.isalpha() == True):
                    gpa = input("Please enter a numerical value\n")
                    continue

                located = False
                mycursor.execute("SELECT * FROM Student WHERE IsDeleted = 0")
                result = mycursor.fetchall()
                for x in result:
                    if (float(x[3]) == float(gpa)):
                        located = True

                if (located):
                    mycursor.execute("SELECT * FROM Student WHERE GPA = ? and isDeleted = 0", (gpa,))
                    result = mycursor.fetchall()
                    for x in result:
                        print(x)
                    break
                else:
                    gpa = input("GPA does not exist, enter an existing value\n")

        if (type == "City"):
            city = input("What city is the student from?\n")
            cityExists = False
            while (cityExists == False):
                if (city.isnumeric() == True):
                    city = input("Please enter an alphabetical value\n")
                    continue
                cityExists = compareTo(city, 7)
                if (cityExists):
                    mycursor.execute("SELECT * FROM Student WHERE City = ? and isDeleted = 0", (city,))
                    result = mycursor.fetchall()
                    for x in result:
                        print(x)
                    break
                else:
                    city = input("City does not exist, enter an existing value\n")
        if (type == "State"):
            state = input("What state is the student from?\n")
            stateExists = False
            while (stateExists == False):
                if (state.isnumeric() == True):
                    state = input("Please enter an alphabetical value\n")
                    continue
                stateExists = compareTo(state, 8)
                if (stateExists):
                    mycursor.execute("SELECT * FROM Student WHERE State = ? and isDeleted = 0", (state,))
                    result = mycursor.fetchall()
                    for x in result:
                        print(x)
                    break
                else:
                    state = input("State does not exist, enter an existing value\n")
        if (type == "Advisor"):
            advisor = input("Who is the faculty advisor for the student?\n")
            advisorExists = False
            while (advisorExists == False):
                if (advisor.isnumeric() == True):
                    advisor = input("Please enter an alphabetical value\n")
                    continue
                if (advisor in advisors):
                    mycursor.execute("SELECT * FROM Student WHERE FacultyAdvisor = ? and isDeleted = 0", (advisor,))
                    result = mycursor.fetchall()
                    for x in result:
                        print(x)
                    break
                else:
                    advisor = input("Advisor does not exist, enter an existing value\n")

    elif (userInput == 'Exit'):
        exitProgram = True

    else:
        print("Please enter a valid input from the following options:")

conn.close()


