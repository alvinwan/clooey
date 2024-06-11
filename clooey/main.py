"""
This simple script only supports input(...) command-line interfaces.
"""
import ast
from jinja2 import Template
import sys
import os
from io import StringIO 
import sys
from pathlib import Path


DIRECTORY = Path(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_PROGRAM = DIRECTORY / 'examples' / 'sample.py'


class InputCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.input_calls = []

    def visit_Call(self, node):
        # Check if the function called is 'input'
        if isinstance(node.func, ast.Name) and node.func.id == 'input':
            self.input_calls.append(node.args[0].value) # input only takes one arg
        self.generic_visit(node)


def parse(program):
    """Parse a program, and return a representation of its CLI
    
    Args:
        program (str): Stringified code to parse
    """
    tree = ast.parse(program)
    visitor = InputCallVisitor()
    visitor.visit(tree)
    return visitor.input_calls


TEMPLATE_FORM = """
<form method="post">
    {% for input in inputs %}
    <label>{{ input }}</label>
    <input type="text" name="{{ loop.index }}">
    {% endfor %}
    <input type="submit" value="submit">
</form>
""".strip()


def generate(cli, template):
    """Take a CLI, and generate a basic form.
    
    Args:
        cli List[str]: Returned representation of CLI from parse
        template str: Jinja2 template for form HTML
    """
    return Template(template).render(inputs=cli)


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

    exec(program, {}, {'input': custom_input})


def maybe_get_program(program):
    if os.path.exists(program):
        with open(program) as f:
            program = f.read()
    return program


def cli(*, program=DEFAULT_PROGRAM):
    """Run a CLI for clooey that shows the results in stdout."""
    program = maybe_get_program(program)

    # Parse the program and print the web form
    prompts = parse(program)
    print(generate(prompts, TEMPLATE_FORM))

    # Grab the user's actual responses
    responses = [input(prompt) for prompt in prompts]

    # Execute program with the user's responses
    execute(responses, program)


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.append(self._stringio.getvalue())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def web(*, program=DEFAULT_PROGRAM):
    """Launch a small web app for clooey for web interactions"""
    from flask import Flask, request

    TEMPLATE_FLASK = """
    {{ form }}
    <p>{{ output }}</p>
    """

    program = maybe_get_program(program)

    app = Flask(__name__)

    @app.route('/', methods=['POST', 'GET'])
    def root():
        output = ""

        # Parse the program and return the web form. Parsed on each page load,
        # so that the script can be updated.
        if request.method == 'POST':
            # Transform dictionary from {'1': 'a', '2': 'b'} into ['a', 'b'].
            # Assumes 1-indexing.
            submission = request.form.to_dict()
            responses = [submission[str(i + 1)] for i in range(len(submission))]

            # Capture all outputs from stdout and store in outputs variable.
            with Capturing() as outputs:
                execute(responses, program)
            output = outputs[0]

        prompts = parse(program)
        html_form = generate(prompts, TEMPLATE_FORM)
        
        # Render both form and outputs.
        return Template(TEMPLATE_FLASK).render(form=html_form, output=output)
    
    app.run()


def main():
    from clize import run
    run([cli, web])


if __name__ == '__main__':
    main()