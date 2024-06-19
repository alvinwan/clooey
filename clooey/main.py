"""
This simple script only supports input(...) command-line interfaces.
"""

import os
import sys

from io import StringIO 
from pathlib import Path

from . import clooey
from jinja2 import Template


DIRECTORY = Path(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_PROGRAM = DIRECTORY / 'examples' / 'sample.py'


def maybe_get_program(program):
    if os.path.exists(program):
        with open(program) as f:
            program = f.read()
    return program


def cli(*, program=DEFAULT_PROGRAM):
    """Run a CLI for clooey that shows the results in stdout."""
    program = maybe_get_program(program)

    # Parse the program and print the web form
    cli = clooey.parse(program)
    print(clooey.generate(cli, clooey.TEMPLATE_FORM))

    # Grab the user's actual responses
    responses = [input(_input.label) for _input in cli.inputs]

    # Execute program with the user's responses
    clooey.execute(responses, program)


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
                clooey.execute(responses, program)
            output = outputs[0]

        prompts = clooey.parse(program)
        html_form = clooey.generate(prompts, clooey.TEMPLATE_FORM)
        
        # Render both form and outputs.
        return Template(TEMPLATE_FLASK).render(form=html_form, output=output)
    
    app.run()


def main():
    from clize import run
    run([cli, web])


if __name__ == '__main__':
    main()