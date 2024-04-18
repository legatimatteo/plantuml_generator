from java_class import java_class
import re, sys, os

VISIBILITY_MODIFIER = {
    'public' : '+',
    'private' : '-',
    'protected' : '#'
}

def print_help():
    print("Usage: plantuml_generator.py [options] [directory_path | file_path]")
    print("Available options:")
    print("\t-f [--file]\t\t Create file to generate UML of the selected file")
    print("\t-d [--directory]\t Create file to generate UML of all selected files")
    print("\t-r [--recursive]\t Create file to generate UML of all files in all subdirectories")
    print("\t-h [--help]\t\t Display this help message")

def write_file(filename, classes):
    with open(filename, 'w') as file:
        file.write('@startuml\n')
        for j_class in classes:
            file.write(j_class.toPlantUML())

        file.write('@enduml\n')

def parse_java_file(file_path):
    with open(file_path, 'r') as file:
        java_code = file.read()

    visibility_regex = '|'.join(VISIBILITY_MODIFIER.keys())

    # find class name and visibility
    class_name_visibility = re.search(r'(' + visibility_regex + ')?\s*class\s+(\w+)', java_code)
    if class_name_visibility:
        name = []
        class_visibility = class_name_visibility.group(1)
        class_name = class_name_visibility.group(2)
        name = [{"visibility" : VISIBILITY_MODIFIER[class_visibility], "name" : class_name}]
    else:
        print("No classes found in " + file_path)
        return

    # finds attributes
    attributes = re.findall(r'(' + visibility_regex + ')?\s+(\w+)\s+(\w+);', java_code)
    if attributes:
        attributes_list = []
        for attr in attributes:
            if len(attr) == 3:
                visibility, data_type, attr_name = attr
                if visibility != '':
                    attributes_list.append(
                        {"visibility" : VISIBILITY_MODIFIER[visibility], "data_type" : data_type, "name" : attr_name}
                    )

    methods_list = []
    #find constructors
    methods = re.findall(r'(public)\s+(\w+)\s*\((.*?)\)', java_code)
    visibility, method_name, parameters = methods[0]
    methods_list.append(
        {"visibility" : VISIBILITY_MODIFIER[visibility], "return_type" : "constructor", "name" : method_name, "parameters" : parameters}
    )
    # find methods
    methods = re.findall(r'(' + visibility_regex + ')\s+(\w+)?\s+(\w+)\s*\((.*?)\)', java_code)
    if methods:
        for method in methods:
            # if len(method) == 4:
            #print(method)
            visibility, return_type, method_name, parameters = method
            if return_type != 'new':
                methods_list.append(
                    {"visibility" : VISIBILITY_MODIFIER[visibility], "return_type" : return_type, "name" : method_name, "parameters" : parameters}
                )

    return java_class(name, attributes_list, methods_list)



    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_help()
        sys.exit(1)

    classes_list = []
    option = sys.argv[1]
    project_path = sys.argv[2]

    if option == '-f' or option == '--file':
        if not os.path.isfile(project_path):
            print(project_path + ", file does not exist.")    
            sys.exit(1)
        
        classes_list.append(parse_java_file(project_path))
    
    elif option == '-d' or option ==  '--directory':
        if not os.path.exists(project_path):
            print(project_path + ", folder does not exist.")    
            sys.exit(1)

        for file in os.listdir(project_path):
            classes_list.append(parse_java_file(project_path + '/' + os.fsdecode(file)))
    
    elif option == '-r' or option == '--recursive':
        if not os.path.exists(project_path):
            print(project_path + ", folder does not exist.")    
            sys.exit(1)

    else:
        print_help()
        sys.exit(1)



    OUTPUT_FOLDER = 'plantuml_code/'
    filename = 'plantuml_code.txt'

    write_file(OUTPUT_FOLDER + filename, classes_list)
    print(option)
    print("File created.")