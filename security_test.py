# security_test.py
def vulnerable_function():
    user_input = input("Enter something to evaluate: ")
    # HIGH SEVERITY: eval is dangerous as it executes raw strings as code
   # return eval(user_input) 

if __name__ == "__main__":
    vulnerable_function()