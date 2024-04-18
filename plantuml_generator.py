import re, sys, os

class java_class:
    def __init__ (self, name, attributes, methods):
        self.name = name
        self.attributes = attributes
        self.methods = methods

    def __str__(self):
        class_name_str = "\n".join([f"{name['visibility']} {name['name']}" for name in self.name])
        attributes_str = "\n".join([f"{attr['visibility']} {attr['data_type']} {attr['name']}" for attr in self.attributes])
        methods_str = "\n".join([f"{method['visibility']} {method['return_type']} {method['name']}({method['parameters']})" for method in self.methods])

        return f"Class: {class_name_str}\nAttributes:\n{attributes_str}\nMethods:\n{methods_str}"


def parse_java_file(file_path):
    with open(file_path, 'r') as file:
        java_code = file.read()

    # find class name and visibility
    class_name_visibility = re.search(r'(public|private|protected)?\s*class\s+(\w+)', java_code)
    if class_name_visibility:
        class_visibility = class_name_visibility.group(1)
        class_name = class_name_visibility.group(2)
        print(class_name_visibility)
        name = [{"visibility" : class_visibility, "name" : class_name}]
    else:
        print("No classes found in " + file_path)

    # finds attributes
    attributes = re.findall(r'(public|private|protected)?\s*(\w+)\s+(\w+);', java_code)
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
    methods = re.findall(r'(public|private|protected)?\s*(\w+)\s+(\w+)\((.*?)\)', java_code)
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

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(file_path + ", file does not exist.")    
        sys.exit(1)

    print(parse_java_file(file_path))