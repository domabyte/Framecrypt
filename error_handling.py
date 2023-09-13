#global error_handling 
def prompt_user(prompt, validator):
    while True:
        try:
            user_input = input(prompt).strip("'\"")
            if validator(user_input):
                return user_input
            else:
                print("Invalid input. Please try again.")
        except KeyboardInterrupt:
            print("User interrupted the process.")
            raise Exception("Thanks for using this tool!")