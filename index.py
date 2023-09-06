import os
import zipfile

#global errorhandling program
def errorHandling(param1,param2):
        try:
            valid_inp = int(input("\nEnter your choice here: "))
            if(valid_inp > param1 and valid_inp < param2):
                return valid_inp
            else:
                 print('Enter in range of [1,2]')
        except ValueError:
            print("Error! Enter an integer value!! You fkin' dump asshole")
        except KeyboardInterrupt:
            print("OOPs feelin' like a very strong keyboard stroke")
            raise Exception("Thanks for coming!!")


def create_passwd_protected_zip(file_name,passwd):

    # Create a zip file with the given password

    with zipfile.ZipFile(f"{file_name}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.setpassword(passwd.encode())
        zipf.write(file_name)
    print("Zip file created successfully.")
# else:
    # print("File not found in the current directory.")

    print(str(os.path.isfile(file_name)))
    while str(os.path.isfile(file_name)) != "True":
         print("Oops! File is missing in the current directory")
    file_size = os.path.getsize(file_name)


    #Check if encoded file exists
    file_num = 1
    if os.path.exists(f'{file_name}.mp4') is False:
         pass
    else:
         while os.path.exists(f'{file_name}({file_num}).mp4'):
              file_num += 1
         file_name = f'{file_name}({file_num})'


def encoding():
    file_name = input("Enter a file or folder name [e.g. file.txt] which you want to encode into frames: ")
    passwd = input("Enter the password to protect zip file: ")
    create_passwd_protected_zip(file_name,passwd)

def decoding():
     print("DECODING DONE!!")

def __main__():
    #Asking for input
    print(f'What would you like to do?\n\t[1] ENCODING the file\n\t[2] DECODING the video')

    #Validating input
    user_choice = errorHandling(0,3)

    #switch case as per response
    match user_choice:
         
         #It will call the encoding function
         case 1:
              encoding()
         case 2:
              decoding()
         case _:
              print("Encounter Error, Run again!!")

if __name__ == "__main__":
    __main__()









from zipfile import ZipFile
import os

def zip_create(directory, password):
    def get_all_file_paths(directory):
        file_paths = []
        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        return file_paths
    
    file_paths = get_all_file_paths(directory)
    print(file_paths)
    
    for file_name in file_paths:
        print(file_name)
    
    with ZipFile(directory + '.zip', 'w') as zip:
        zip.setpassword(password)  # Set the password for the zip file
        os.chdir(directory)
        
        for file in file_paths:
            zip.write(file)
        
        print('All files zipped successfully!')

# Example usage:
zip_create('/path/to/directory', 'password123')
