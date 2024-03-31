from Cheetah.Template import Template

templateDef = """
 #for $sensor_comp in $comp_info.sensor_comps
    this->${sensor_comp}PortOut_out(0);
    #end for
    #for $handle_comp in $comp_info.handle_comps
    this->${handle_comp}PortOut_out(0);
    #end for 
    
    $abc is abc
"""

t1 = Template(templateDef)
t1.comp_info = {'sensor_comps': ['sensor_comp1', 'sensor_comp2'], 'handle_comps': ['handle_comp1', 'handle_comp']}
t1.abc = 'abc'
print(t1)

# nameSpace = {"title": "Hello World", "contents": "Hello World!"}

# t = Template(templateDef, searchList=[nameSpace])
# print(t)

# t2 = Template(templateDef)
# t2.title = "Hello World"
# t2.contents = "Hello World!"
# print(t2)

# class Template3(Template):
#     title = "Hello World"
#     contents = "Hello World!"
# t3 = Template3(templateDef)
# print(t3)