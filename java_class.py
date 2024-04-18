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
    
    def toPlantUML(self):
        class_name = "class " + ''.join([f"{name['name']}" for name in self.name]) + '{'
        attributes = "".join([f"\n\t {'+' if attr['visibility'] == 'public' else '-'} {attr['name']} : {attr['data_type']}" for attr in self.attributes])
        methods = "".join([f"\n\t {'+' if method['visibility'] == 'public' else '-'} {method['name']}({method['parameters']}) : {method['return_type']}" for method in self.methods])
        close_bracket = "\n}\n"

        return f"{class_name} {attributes} {methods} {close_bracket}"