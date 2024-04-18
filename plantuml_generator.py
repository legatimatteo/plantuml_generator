from java_class import java_class
import re, sys, os

def parse_java_file(file_path):
    with open(file_path, 'r') as file:
        java_code = file.read()

    # find class name and visibility
    class_name_visibility = re.search(r'(public|private|protected)?\s*class\s+(\w+)', java_code)
    if class_name_visibility:
        name = []
        class_visibility = class_name_visibility.group(1)
        class_name = class_name_visibility.group(2)
        name = [{"visibility" : class_visibility, "name" : class_name}]
    else:
        print("No classes found in " + file_path)
        return

    # finds attributes
    attributes = re.findall(r'(public|private|protected)?\s+(\w+)\s+(\w+);', java_code)
    if attributes:
        attributes_list = []
        for attr in attributes:
            if len(attr) == 3:
                visibility, data_type, attr_name = attr
                if visibility != '':
                    attributes_list.append(
                        {"visibility" : visibility, "data_type" : data_type, "name" : attr_name}
                    )

    # find methods
    methods = re.findall(r'(public|private|protected)?\s+(\w+)\s+(\w+)\((.*?)\)', java_code)
    if methods:
        methods_list = []
        for method in methods:
            if len(method) == 4:
                visibility, return_type, method_name, parameters = method
                if return_type != 'new':
                    methods_list.append(
                        {"visibility" : visibility, "return_type" : return_type, "name" : method_name, "parameters" : parameters}
                    )

    return java_class(name, attributes_list, methods_list)



    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    if not os.path.exists(project_path):
        print(project_path + ", file does not exist.")    
        sys.exit(1)

    classes_list = []
    for file in os.listdir(project_path):
        classes_list.append(parse_java_file(project_path + '/' + os.fsdecode(file)))
    
    for j_class in classes_list:
        print(j_class.toPlantUML())