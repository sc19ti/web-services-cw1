import requests, json

#x = requests.get('http://127.0.0.1:8000/module/viewall')
#print(x.content)

#y = requests.post('http://127.0.0.1:8000/rateprofessor/sc19ti/Introduction_to_Programming/Professor_1/4/')
#print(y.text)
isAuthenticated = False
username = ''


while True:
    print("""\n\nRATE MY PROFESSOR
-------------------------------------------
-------------------------------------------
Please don't input any additional whitespace other than what is specfied. List of Commands:
    1. "list" - list all modules, the semester, year and professor
    2. "view" - view all professors
    3. "average *professor_id*" - view the average rating of a professor given their ID
    4. "rate *professor_id* *module_id* *rating*" - rate a professor of a particular module. Rating should be an integer between 1 and 5
    5. "register" - register as a user. You must register before or login before using any other command.
    6. "login" - login to the service.
    7. "logout" - logout of the service.
    8. "quit" - quit the application.
    \n\n""")
    inputCommand = input('Please input your command:')
    if inputCommand == "register":
        if isAuthenticated == True:
            print("\nYou are already logged in. \n")
        else:
            print("Do not include any whitespace in username email or password.\n")
            username = input('username:')
            email = input('email:')
            password = input('password:')
            if " " in username or " " in email or " " in password:
                print("Do not include any whitespace in username email or password.\n")
            else:
                registerUser = requests.post('http://127.0.0.1:8000/register/' + username + '/' + password + '/' + email + '/')
                if bytes.decode(registerUser.content) == "Failed":
                    print("Failed to create user.\n")
                elif bytes.decode(registerUser.content) == "username already in use":
                    print("Username already in use. Please select another username.\n")
                elif bytes.decode(registerUser.content) == "Successfully created user":
                    print("Successfully created user.\n")
            
    elif "login" in inputCommand:
        if isAuthenticated == True:
            print("\nYou are already logged in. \n")
        else:
            username = input('username:')
            password = input('password:')
            login = requests.get('http://127.0.0.1:8000/login/' + username + '/' + password + '/')
            print(login.content)
            if bytes.decode(login.content) == 'Authenication Successfull':
                isAuthenticated = True
                print("Login Sucessfull.\n")
            else:
                print("username or password is incorrect.\n")
            
    elif inputCommand == "logout":
        if isAuthenticated == False:
            print("\nYou are not logged in so you can't log out. \n")
        else:
            isAuthenticated = False
            print("Logout Successfull.\n")
        
    elif inputCommand == "list":
        if isAuthenticated == True:
            moduleList = requests.get('http://127.0.0.1:8000/module/viewall/')           
            if bytes.decode(moduleList.content) == "No Modules found":
                print("No Modules found. \n")
            else:
                print("---------------------------------------------------------------------------------")
                print("|id   |name                               |year  |semester | lecturer(s)(id,name)|")
                print("---------------------------------------------------------------------------------")    
                for module in json.loads(bytes.decode(moduleList.content))['module_list']:
                    print("|"+str(module['id']).ljust(5,' ')+"|"+ str(module['name']).ljust(35,' ')+"|"+ str(module['year']).ljust(6,' ') +"|"+ str(module['semester']).ljust(9,' ')+"|", [x for x in module['professors']],"|")
                    print("---------------------------------------------------------------------------------")
        else:
            print('Please login or register before giving other commands.\n')

    elif inputCommand == "view":
        if isAuthenticated == True:
            professorList = requests.get('http://127.0.0.1:8000/professor/viewall')
            if bytes.decode(moduleList.content) == "No Professors found":
                print("No Professors found. \n")
            else:
                for professor in json.loads(bytes.decode(professorList.content))['professor_list']:
                    print("The average rating of professor",professor['id'],",", professor['name'], "is", professor['rating'])
        else:
            print('Please login or register before giving other commands.\n')
        
    elif "average" in inputCommand:
        if isAuthenticated == True:
            parsedCommand = inputCommand.split(' ')
            if len(parsedCommand) == 2:
                professorAverage = requests.get('http://127.0.0.1:8000/professor/view/' + parsedCommand[1] + '/')
                if bytes.decode(professorAverage.content) == 'Professor not found':
                    print('Professor not found.\n')
                elif bytes.decode(professorAverage.content) == 'No ratings found for this Professor':
                    print('No ratings found for this Professor. \n')
                else:
                    professor_dict = json.loads(bytes.decode(professorAverage.content))
                    print("The average rating of professor", professor_dict['prof']['name'], "is", professor_dict['prof']['rating'])
            else:
                print("\nPlease input exactly one professor ID.\n")
        else:
            print('Please login or register before giving other commands.\n')
        
    elif  "rate" in inputCommand:
        if isAuthenticated == True:
            parsedCommand = inputCommand.split(' ')
            if len(parsedCommand) == 4:
                rateProfessor = requests.post('http://127.0.0.1:8000/rateprofessor/' + username + '/' + parsedCommand[1] + '/' + parsedCommand[2] + '/' + parsedCommand[3]+'/')
                if bytes.decode(rateProfessor.content) == "Integer rating between 1 and 5 only":
                    print("Integer rating between 1 and 5 only")
                elif bytes.decode(rateProfessor.content) == "Professor not found":
                    print("Professor not found")
                elif bytes.decode(rateProfessor.content) == "Module not found":
                    print("Module not found")
                elif bytes.decode(rateProfessor.content) == "Specified Professor does not teach the specified module.":
                    print ("Specified Professor does not teach the specified module.")
                elif bytes.decode(rateProfessor.content) == "success":
                    print("successfully added rating")
                    
            else:
                print("\nPlease input exactly 3 integer arguments in addition to the command as specified in the index.\n")
            #requests.post('http://127.0.0.1:8000/rateprofessor/sc19ti/Introduction_to_Programming/Professor_1/4/')
        else:
            print('Please login or register before giving other commands.\n')
        
    elif inputCommand == "quit":
        quit()
    else:
        print("\nPlease input a valid command.")
    
