import tkinter as tk
from tkinter import messagebox
from tkinter import *
from licensing.models import *
from licensing.methods import Key, Helpers
import pickle  # Dodano import modułu pickle
import subprocess

# Create the main window
root = tk.Tk()
root.title("License Activation")

# Set the size of the window to 200x200 pixels
root.geometry("400x300")

# Set the background color to grey
root.configure(bg="#10121f")  # You can adjust the color code as needed


result_labell = tk.Label(root, text="", bg="#10121f", fg="white")  # Set text color to white
result_labell.pack(side='top', anchor=CENTER, pady=30)

# Create a text entry widget with background color #25292e
text_entry = tk.Entry(root, width=30, bg="#25292e", fg="white")  # Set text color to white
text_entry.pack(pady=10)
text_entry.pack(side='top', anchor=CENTER, pady=10)

def get_text_from_entry(entry_widget):
    return entry_widget.get()



def new_win():
    subprocess.run(['python', 'GhostOptimizer.py'])

def activate_license():
    RSAPubKey = "<RSAKeyValue><Modulus>i5XW4q7h+JbUPcf5XQo/KCEs/OqJmchV+/vC4i4wFD8tnaAqxuxRn3Qjnng7SsiPzDP6CPYp9KQuQ1JrfqhNphuzJUpHAkkmkAzd7fGvMiylVIrr2+yTXE9OrGNC7QANoppxDAVgIkEP4P5m6fa2kPzXYXfmrlautdxZhR1oAA0Tj3H0oHl31PI+hvjJxvFOEaJRWupAzpujsQ0Dq2OfTFhMJwt+a8U90aZHzvJ8pKE30EhmLRjoVS+wZV/xtxqmGYcFJvjkGi2xYeDerfxL1a9yyKm27zK/I5vimKLsl/l4jcsbZVA1dW7FkJBqMcVXxWB2D1UgsAbnGHgHw1P9iQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
    auth = "WyI3MzAzNjE4NCIsIk9QRjZCMHhxNGxTUkkwSzZwajFNOFppMU9xQ2hpTlZsbzR3YlRsdE0iXQ=="

    result = Key.activate(token=auth,\
                       rsa_pub_key=RSAPubKey,\
                       product_id=23761, \
                       key=text_entry.get(),  # Using the key entered in the text entry
                       machine_code=Helpers.GetMachineCode(v=2))

    if result[0] == None:
        # an error occurred or the key is invalid or it cannot be activated
        # (eg. the limit of activated devices was achieved)
        result_label.config(text="The license does not work: {0}".format(result[1]))
    else:
        with open("data.pkl", "wb") as file:
            data = {"text": get_text_from_entry(text_entry)}
            pickle.dump(data, file)
        root.destroy()
        new_win()



# Create a button to activate the license with background color #25292e
activate_button = tk.Button(root, text="Activate License", command=activate_license, bg="#25292e", fg="white")  # Set text color to white
activate_button.pack(pady=10)
activate_button.pack(side='top', anchor=CENTER, pady=10)

# Create a label to display the result with background color #25292e
result_label = tk.Label(root, text="", bg="#10121f", fg="white")  # Set text color to white
result_label.pack(side='top', anchor=CENTER, pady=10)




# Center the widgets horizontally and vertically
root.update_idletasks()  # Make sure the window size is updated
width = root.winfo_width()
height = root.winfo_height()
x_pos = (root.winfo_screenwidth() // 2) - (width // 2)
y_pos = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x_pos, y_pos))

# Run the Tkinter event loop
root.mainloop()
