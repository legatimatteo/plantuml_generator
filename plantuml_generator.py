from java_class import java_class
import re, sys, os

VISIBILITY_MODIFIER = {
    'public' : '+',
    'private' : '-',
    'protected' : '#',
    'interface' : '+',
    'default' : '~'
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
        file.write('@startuml\nleft to right direction\n\n')
        for j_class in classes:
            if j_class is not None:
                file.write(j_class.toPlantUML('Attributes', 'Methods'))

        file.write('@enduml\n')

def parse_java_file(file_path, classes_founded):
    with open(file_path, 'r') as file:
        java_code = file.read()

    map_regex = '(?:\s*<\s*\w+\s*(?:,\s*\w+\s*)*>)'
    class_name_regex = '|'.join([item["name"] for item in classes_founded if item["type"] == "class"])
    interface_name_regex = '|'.join([item["name"] + '\s*.*?' for item in classes_founded  if item["type"] == "interface"] )

    # find class name and visibility
    class_name_result = re.search(r'(public|private|protected)?\s*(class|interface)\s+('+ class_name_regex + '|' + interface_name_regex +r')\s*(implements\s+(' + interface_name_regex + r')*)?\s*(extends\s+(' + class_name_regex + r')*)?(?:\s*{)', java_code)
    if class_name_result is None:
        print("No classes/interfaces found in " + file_path)
        return
    
    class_visibility = class_name_result.group(1)
    class_type = class_name_result.group(2)
    class_name = class_name_result.group(3)
    class_dependencies = class_name_result.group(4) 
    
    print(class_type)
    print(class_name)
    print(class_dependencies)
    name = [{"visibility" : VISIBILITY_MODIFIER[class_visibility], "type" : class_type, "name" : class_name, "dependencies" : class_dependencies}]

    # finds attributes
    attributes_list = []
    attributes = re.findall(r'(public|private|protected)\s*(static)?\s*(final)?\s+(\w+' + map_regex + r'?)\s+(\w+)(?:\s*=\s*)?(.*?)?;', java_code)
    #print('ATTRIBUTES')
    #print(attributes)
    if attributes:
        for attr in attributes:
            if len(attr) >= 3:
                visibility, static, final, data_type, attr_name, value = attr
                if visibility != '':
                    attributes_list.append(
                        {"visibility" : VISIBILITY_MODIFIER[visibility], "static" : static, "final" : final, "data_type" : data_type, "name" : attr_name, "var_value" : value}
                    )

    methods_list = []
    if class_type == 'class':
        #find constructors
        methods = re.findall(r'(public)\s+(\w+)\s*\((.*?)\)', java_code)
        if methods:
            visibility, method_name, parameters = methods[0]
            methods_list.append(
                {"visibility" : VISIBILITY_MODIFIER[visibility], "return_type" : "constructor", "name" : method_name, "parameters" : parameters}
            )
        # find methods
        methods = re.findall(r'(public|private|protected)\s*(static)?\s+(\w+)\s+(\w+)\s*\((.*?)\)', java_code)
        #print('METHODS')
        #print(methods)
        if methods:
            for method in methods:
                visibility, static, return_type, method_name, parameters = method
                if return_type != 'new' and visibility != '':
                    methods_list.append(
                        {"visibility" : VISIBILITY_MODIFIER[visibility], "static" : static, "return_type" : return_type, "name" : method_name, "parameters" : parameters}
                    )

    # find methods interface
    if class_type == 'interface':
        methods = re.findall(r'(public|private|protected)?\s*(static)?\s+(\w+)\s+(\w+)\s*\((.*?)\)', java_code)
        #print('METHODS')
        #print(methods)
        if methods:
            for method in methods:
                visibility, static, return_type, method_name, parameters = method
                print('VISIBILITY')
                print(visibility)
                if not visibility:
                    visibility = 'interface'
                
                methods_list.append(
                    {"visibility" : VISIBILITY_MODIFIER[visibility], "static" : static, "return_type" : return_type, "name" : method_name, "parameters" : parameters}
                )

    return java_class(name, attributes_list, methods_list)

def parse_java_class (file_path):
    with open(file_path, 'r') as file:
        java_code = file.read()
        
        # find class name and visibility
        class_search = re.search(r'(?:public|private|protected)?\s*(class|interface)\s+(\w+)\s*(?:{)?', java_code)
        if class_search is None:
            print("No classes/interfaces found in " + file_path)
            return
            
        class_type = class_search.group(1)
        class_name = class_search.group(2)
        return {"type" : class_type, "name" : class_name}
    

    
if __name__ == '__main__':
    if len(sys.argv) < 3:

        print_help()
        sys.exit(1)

    classes_list = []
    classes_founded = []
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

        for file in file_list:
            classes_founded.append(parse_java_class(file))
        
        for file in file_list:
            classes_list.append(parse_java_file(file, classes_founded))

            
            
        

    else:
        print_help()
        sys.exit(1)



    OUTPUT_FOLDER = 'plantuml_code/'
    filename = 'plantuml_code.txt'

    write_file(OUTPUT_FOLDER + filename, classes_list)
    print("File created.")