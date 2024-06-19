# clooey

Python Command Line Interface (CLI) to an HTML form.

> For a Javascript API that does not depend on a Python runtime to
> *generate* the form, see the `js/` directory in this repository.

## Getting Started

Start by installing clooey using pip.

```bash
pip install clooey
```

Here's a sample Python script that has `input` calls.

```python
name = input("Enter your name: ")
city = input("Enter your city: ")

print(f"Welcome to {city}, {name}!")
```

clooey can convert this Python script into a form, based on its calls to
`input`.

```python
import clooey

TEMPLATE_FORM = """
<form method="post">
{% for input in cli.inputs %}
    <label>{{ input.label }}</label>
    <input type="text" name="{{ loop.index }}">
{% endfor %}
    <input type="submit" value="submit">
</form>
"""

cli = clooey.parse('sample.py')
html = clooey.generate(cli, TEMPLATE_FORM)
print(html)
```

Running the above conversion script gives the following HTML output.

```html
<form method="post">
    
    <label>Enter your name: </label>
    <input type="text" name="1">
    
    <label>Enter your city: </label>
    <input type="text" name="2">
    
    <input type="submit" value="submit">
</form>
```

# Advanced

There are several more features that clooey supports:
- Each prompt can contain a `[placeholder]` value, delimited by square brackets,
    that will be used as the placeholder text in the form.
- You can provide a title and description for the form. The title is the first
    non-whitespace line of the docstring, and the description is the rest of the
    docstring.

Here's a sample Python script that has `input` calls.

```python
"""Tell me about you

A simple hello world application to greet you!
"""

name = input("Enter your name: ")
age = int(input("Enter your age: "))
city = input("Enter your city [Seattle]: ") or 'Seattle'

print(f"Welcome to {city}, {name} ({age})!")
```

clooey can convert this Python script into a form, based on its calls to
`input`.

```python
import clooey

TEMPLATE_FORM = """
{% if cli.title %}<h1>{{ cli.title }}</h1>{% endif %}
{% if cli.description %}<p>{{ cli.description }}</p>{% endif %}
<form method="post">
    {% for input in cli.inputs %}
    <label>{{ input.label }}</label>
    <input type="text" name="{{ loop.index }}" placeholder="{{ input.placeholder }}">
    {% endfor %}
    <input type="submit" value="submit">
</form>
"""

cli = clooey.parse('sample.py')
html = clooey.generate(cli, TEMPLATE_FORM)
print(html)
```

Notice that the HTML template is
[Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) formatted. You can
customize this HTML as you see fit, as long as the there are input fields
with the names `1`, `2`, `3`, etc. The above script gives us this output.

```html
<h1>Tell me about you</h1>
<p>A simple hello world application to greet you!</p>
<form method="post">
    
    <label>Enter your name: </label>
    <input type="text" name="1" placeholder="">
    
    <label>Enter your age: </label>
    <input type="text" name="2" placeholder="">
    
    <label>Enter your city:</label>
    <input type="text" name="3" placeholder="Seattle">
    
    <input type="submit" value="submit">
</form>
```

If you save this HTML in a file and open the file in a browser, you'll then see
the following:

<img width="952" alt="Screenshot 2024-06-19 at 12 42 36 AM" src="https://github.com/alvinwan/clooey/assets/2068077/9935a978-0989-4701-8f18-27b3ace61422">

# Web Demo

See an actual web form by running the following command:

```bash
clooey web
```

From left to right, you'll see the launched Flask app with the following form,
fill out the form as you would the CLI, then submit the form to see the output.

<img width="30%" alt="Screenshot 2024-06-10 at 9 40 48 PM" src="https://github.com/alvinwan/clooey/assets/2068077/5bc66be5-ef4f-47ba-8280-68c6c975d521">
<img width="30%" alt="Screenshot 2024-06-10 at 9 41 58 PM" src="https://github.com/alvinwan/clooey/assets/2068077/cd9f9e1d-7773-4f2b-9c59-431eef86f8e3">
<img width="30%" alt="Screenshot 2024-06-10 at 9 41 09 PM" src="https://github.com/alvinwan/clooey/assets/2068077/73119a3e-cca3-46d5-91ad-1558425c134f">

You can optionally provide your own script to parse. For example,

```bash
wget https://github.com/alvinwan/clooey/blob/main/clooey/examples/password.py
clooey web --program password.py
```

## CLI Demo

Run the CLI.

```bash
clooey cli
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

You can optionally provide your own script to parse. For example,

```bash
wget https://github.com/alvinwan/clooey/blob/main/clooey/examples/piglatin.py
clooey cli --program piglatin.py
```
