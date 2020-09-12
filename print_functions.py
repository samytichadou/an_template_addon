from .global_variables import addon_print_prefix

# print and report
# type in {"INFO", "ERROR", "WARNING"}
def print_and_report(self, message, type):
    #print(addon_print_prefix + message)
    if self:
        self.report({type}, message)
    else:
        print(addon_print_prefix + message)
