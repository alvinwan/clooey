# clooey

Python Command Line Interface (CLI) to an HTML form. This is the Javascript
API, which can run immediately on page load even without a Python runtime -- at 
least, to generate the form. The API is the same as the Python version.

See the single-file implementation in `clooey.js`.

Using *almost* the same example as the Python README, here's a Python snippet.
For the sake of a simpler demo, the last line below is not a print statement.
Instead, it's a string that will be returned to the Javascript API.

```python
"""Tell me about you

A simple hello world application to greet you!
"""

name = input("Enter your name: ")
age = int(input("Enter your age: "))
city = input("Enter your city [Seattle]: ") or 'Seattle'

f"Welcome to {city}, {name} ({age})!"
```

and given this nunjucks template

```html
{% if cli.title %}<h1>{{ cli.title }}</h1>{% endif %}
{% if cli.description %}<p>{{ cli.description }}</p>{% endif %}
<form method="post">
    {% for input in cli.inputs %}
    <label>{{ input.label }}</label>
    <input type="text" name="{{ loop.index }}" placeholder="{{ input.placeholder }}">
    {% endfor %}
    <input type="submit" value="submit">
</form>
```

You now get the following HTML form.

```html
<h1>Tell me about you</h1>
<p>A simple hello world application to greet you!</p>
<form method="post">
    
    <label>Enter your name: </label>
    <input type="text" name="1" placeholder="">
    
    <label>Enter your age: </label>
    <input type="text" name="2" placeholder="">
    
    <label>Enter your city :</label>
    <input type="text" name="3" placeholder="Seattle">
    
    <input type="submit" value="submit">
</form>
```


<img width="952" alt="Screenshot 2024-06-19 at 12 42 36 AM" src="https://github.com/alvinwan/clooey/assets/2068077/8b72a259-6239-46af-86bc-cd4a182c9719">