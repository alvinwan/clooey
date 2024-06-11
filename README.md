# clooey

Command Line Interface (CLI) to a minimal Web UI.

## Getting Started

Start by installing clooey using pip.

```bash
pip install pip+https://github.com/alvinwan/clooey.git
```

You can then use the API to convert a script into a form.

```python
import clooey

cli = clooey.parse('sample.py')
html = clooey.generate(cli, clooey.TEMPLATE_FORM) # use default jinja2 template
```

For customizing your own form HTML, you must use the loop index for input names.
The template is provided with one `inputs` list of strings, which are the
prompts provided to `input` function calls.

# Web Demo

See an actual web form by running the following command:

```bash
python main.py web sample.py
```

From left to right, you'll see the launched Flask app with the following form,
fill out the form as you would the CLI, then submit the form to see the output.

<img width="33%" alt="Screenshot 2024-06-10 at 9 40 48 PM" src="https://github.com/alvinwan/clooey/assets/2068077/5bc66be5-ef4f-47ba-8280-68c6c975d521">
<img width="33%" alt="Screenshot 2024-06-10 at 9 41 58 PM" src="https://github.com/alvinwan/clooey/assets/2068077/cd9f9e1d-7773-4f2b-9c59-431eef86f8e3">
<img width="33%" alt="Screenshot 2024-06-10 at 9 41 09 PM" src="https://github.com/alvinwan/clooey/assets/2068077/73119a3e-cca3-46d5-91ad-1558425c134f">

## CLI Demo

Run the CLI.

```bash
python main.py cli sample.py
```

You'll then see the following output

```html
<form method="post">
    
    <label>Enter your name: </label>
    <input type="text" name="1">
    
    <label>Enter your age: </label>
    <input type="text" name="2">
    
    <label>Enter your city: </label>
    <input type="text" name="3">
    
    <input type="submit" value="submit">
</form>
```

Next, the script will prompt you for input, as though you were filling out the
web form.

```
Enter your name: Alvin
Enter your age: 1000
Enter your city: Seattle
```

Finally, the script will execute the Python script with the input values.

```
Welcome to Seattle, Alvin (1000)!
```
