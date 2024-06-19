import ast
from dataclasses import dataclass
from jinja2 import Template
from typing import List
import re


@dataclass
class Input:
    label: str
    placeholder: str = ''


@dataclass
class CLI:
    inputs: List[Input]
    title: str = ''
    description: str = ''


class InputCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.input_calls = []

    def visit_Call(self, node):
        # Check if the function called is 'input'
        if isinstance(node.func, ast.Name) and node.func.id == 'input':
            self.input_calls.append(parse_prompt(node.args[0].value)) # input only takes one arg
        self.generic_visit(node)


def parse_prompt(prompt):
    """Parses a prompt string into a dictionary with 'label' and 'placeholder' keys.
    
    Args:
        prompt (str): The input string to parse.
    
    >>> parse_prompt("Your city [Seattle]:")
    Input(label='Your city:', placeholder='Seattle')
    
    >>> parse_prompt("Your city: [Seattle]")
    Input(label='Your city:', placeholder='Seattle')
    
    >>> parse_prompt("Your city \\[Seattle\\]:")
    Input(label='Your city [Seattle]:', placeholder='')
    
    >>> parse_prompt("Your city \\[Seattle\\]: [Placeholder]")
    Input(label='Your city [Seattle]:', placeholder='Placeholder')
    """
    pattern = r'^(.*)?(?<!\\)\[(.*)(?<!\\)\](.*)?$'
    match = re.match(pattern, prompt)
    
    if match:
        label = match.group(1).strip() + match.group(3).strip()
        placeholder = match.group(2).strip() if match.group(2) else ''
    else:
        label, placeholder = prompt, ''
    
    label = label.replace('\\[', '[').replace('\\]', ']')
    return Input(label, placeholder)


def parse(program):
    """Parse a program, and return a representation of its CLI
    
    Args:
        program (str): Stringified code to parse

    Returns:
        List[Input]: Specifying CLI using a list of Input objects

    >>> cli = parse(\"'''\\nBlurple\\nBlack and purple color mix\\n'''\")
    >>> cli.title
    'Blurple'
    >>> cli.description
    'Black and purple color mix'
    >>> cli = parse(\"'''Blurple\\nBlack and purple color mix\\n'''\")
    >>> cli.title
    'Blurple'
    >>> cli = parse(\"'''Blurple\\n\\nBlack and purple color mix\\n'''\")
    >>> cli.title
    'Blurple'
    """
    tree = ast.parse(program)
    visitor = InputCallVisitor()
    visitor.visit(tree)
    
    if docs := ast.get_docstring(tree):
        title, description = docs.strip().split('\n', 1)
    return CLI(visitor.input_calls, title.strip(), description.strip())


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
""".strip()


def generate(cli, template):
    """Take a CLI, and generate a basic form.
    
    Args:
        cli List[Input]: Returned representation of CLI from parse
        template str: Jinja2 template for form HTML
    """
    return Template(template).render(cli=cli)


def execute(responses, program):
    """
    Executes the program using a list of provided form submission.
    
    Args:
        responses List[str]: Responses for each input call prompt
        program (str): Stringified code to run
    """
    inputs_iterator = iter(responses)

    def custom_input(prompt=None):
        """
        Custom implementation of input that simply returns from the iterable of
        responses. In this way, we can mimic user interaction with the script.
        """
        try:
            return next(inputs_iterator)
        except StopIteration:
            raise RuntimeError("Not enough inputs provided")

    exec(program, {'input': custom_input})