# security_test.py
def vulnerable_function():
    input = input("Enter something to evaluate: ")
    # HIGH SEVERITY: eval is dangerous as it executes raw strings as code
    return eval(input) 

if __name__ == "__main__":
    vulnerable_function()