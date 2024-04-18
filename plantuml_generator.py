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
            if j_class is not None:
                file.write(j_class.toPlantUML())

        file.write('@enduml\n')

def parse_java_file(file_path):
    with open(file_path, 'r') as file:
        java_code = file.read()

    print(file_path)

    map_regex = '(?:\s*<\s*\w+\s*(?:,\s*\w+\s*)*>)'

    # find class name and visibility
    class_name_visibility = re.search(r'(public|private|protected)?\s*class\s+(\w+)', java_code)
    print("CLASS NAME\n")
    print(class_name_visibility)
    if class_name_visibility:
        name = []
        class_visibility = class_name_visibility.group(1)
        class_name = class_name_visibility.group(2)
        name = [{"visibility" : VISIBILITY_MODIFIER[class_visibility], "name" : class_name}]
    else:
        print("No classes found in " + file_path)
        return

    # finds attributes
    #attributes = re.findall(r'(public|private|protected)\s*(static)?\s*(final)?\s+(\w+' + map_regex + r'?)\s+(\w+);', java_code)
    attributes = re.findall(r'(public|private|protected)\s*(static)?\s*(final)?\s+(\w+' + map_regex + r'?)\s+(\w+)(?:\s*=\s*)?(.*?)?;', java_code)

    print("ATTRIBUTES\n")
    print(attributes)
    if attributes:
        attributes_list = []
        for attr in attributes:
            if len(attr) >= 3:
                visibility, static, final, data_type, attr_name, value = attr
                if visibility != '':
                    attributes_list.append(
                        {"visibility" : VISIBILITY_MODIFIER[visibility], "static" : static, "final" : final, "data_type" : data_type, "name" : attr_name, "var_value" : value}
                    )

    methods_list = []
    #find constructors
    methods = re.findall(r'(public)\s+(\w+)\s*\((.*?)\)', java_code)
    print("CONSTRUCTORS\n")
    print(methods)
    if methods:
        visibility, method_name, parameters = methods[0]
        methods_list.append(
            {"visibility" : VISIBILITY_MODIFIER[visibility], "return_type" : "constructor", "name" : method_name, "parameters" : parameters}
        )
    # find methods
    methods = re.findall(r'(public|private|protected)\s*(static)?\s+(\w+)\s+(\w+)\s*\((.*?)\)', java_code)
    print("METHODS\n")
    print(methods)
    if methods:
        for method in methods:
            # if len(method) == 4:
            #print(method)
            visibility, static, return_type, method_name, parameters = method
            if return_type != 'new':
                methods_list.append(
                    {"visibility" : VISIBILITY_MODIFIER[visibility], "static" : static, "return_type" : return_type, "name" : method_name, "parameters" : parameters}
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
            if os.path.isfile(project_path + '/' + os.fsdecode(file)):
                if file.endswith('.java') and not file.startswith('.'):
                    classes_list.append(parse_java_file(project_path + '/' + os.fsdecode(file)))
    
    elif option == '-r' or option == '--recursive':
        if not os.path.exists(project_path):
            print(project_path + ", folder does not exist.")    
            sys.exit(1)
        
        file_list = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith('.java') and not file.startswith('.'):
                    file_list.append(os.path.join(root, file))

        file_list.remove
        for file in file_list:
            classes_list.append(parse_java_file(file))

    else:
        print_help()
        sys.exit(1)



    OUTPUT_FOLDER = 'plantuml_code/'
    filename = 'plantuml_code.txt'

    write_file(OUTPUT_FOLDER + filename, classes_list)
    print("File created.")