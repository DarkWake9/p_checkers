import tkinter as tk

root = tk.Tk()
root.title("Temperature Converter")

def convert():
    try:
        temperature = float(entry.get())
        if var.get() == 1:
            result = (temperature * 9/5) + 32
            output_label.config(text=f"{temperature}°C = {result}°F")
        else:
            result = (temperature - 32) * 5/9
            output_label.config(text=f"{temperature}°F = {result}°C")
    except ValueError:
        output_label.config(text="Invalid input")

var = tk.IntVar()

celsius_radio = tk.Radiobutton(root, text="Celsius to Fahrenheit", variable=var, value=1)
celsius_radio.pack()

fahrenheit_radio = tk.Radiobutton(root, text="Fahrenheit to Celsius", variable=var, value=2)
fahrenheit_radio.pack()

entry = tk.Entry(root)
entry.pack()

convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.pack()

output_label = tk.Label(root)
output_label.pack()

root.mainloop()