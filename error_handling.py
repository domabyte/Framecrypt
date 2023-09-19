import os 

#global error_handling 
def prompt_user(prompt, validator):
    while True:
        try:
            user_input = input(prompt).strip("'\"")
            if validator(user_input):
                return user_input
            else:
                print("Invalid input. Please try again.\n")
        except KeyboardInterrupt:
            print("User interrupted the process.")
            raise SystemExit("Thanks for using this tool!")
        except SystemExit:
            pass

def prompt_user_file(prompt,validator):
    while True:
        try:
            user_input = input(prompt).strip("'\"")
            dir_file = os.path.join("encoded_videos",user_input)
            if validator(dir_file):
                return user_input
            else:
                print("Invalid input. Please try again.\n")
        except KeyboardInterrupt:
            print("User interrupted the process.")
            raise SystemExit("Thanks for using this tool!")
        except SystemExit:
            pass