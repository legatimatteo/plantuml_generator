class java_class:
    def __init__ (self, name, attributes, methods):
        self.name = name
        self.attributes = attributes
        self.methods = methods

    def __str__(self):
        class_name_str = "\n".join([f"visibility={name['visibility']} name={name['name']}" for name in self.name])
        attributes_str = "\n".join([f"visibility={attr['visibility']} static={attr['static']} final={attr['final']} data_type={attr['data_type']} name={attr['name']}" for attr in self.attributes])
        methods_str = "\n".join([f"visibility={method['visibility']} static={method['static']} return_type={method['return_type']} name={method['name']}(p={method['parameters']})" for method in self.methods])

        return f"Class: {class_name_str}\nAttributes:\n{attributes_str}\nMethods:\n{methods_str}"
    
    def toPlantUML(self):
        class_name = "class " + ''.join([f"{name['name']}" for name in self.name]) + '{'
        attributes = "".join([f"\n\t {attr['visibility']} {'{static}' if 'static' in attr and attr['static'] else ''} {attr['name']} : {attr['data_type']} {'= ' + attr['var_value'] if 'var_value' in attr and attr['var_value'] else ''} {'{readOnly}' if 'final' in attr and attr['final'] else ''}" for attr in self.attributes])
        methods = "".join([f"\n\t {method['visibility']} {'{static}' if 'static' in method and method['static'] else ''} {method['name']}({method['parameters']})" for method in self.methods])
        close_bracket = "\n}\n"

        return f"{class_name} {attributes} {methods} {close_bracket}"