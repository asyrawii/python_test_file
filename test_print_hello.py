# Disclaimer :- This is from ChatGPT
# Write a Python3 function *print_hello()* that prints "Hello world!".
"""Sample code
def print_hello():
    print("Hello world!")
"""


from exercise import print_hello  # import your function

def test_say_hello_output(capsys):
    # Call the function (it prints but does not return)
    print_hello()
    
    # Capture printed output
    captured = capsys.readouterr()
    
    # Check if the output matches exactly
    assert captured.out.strip() == "Hello world!"
