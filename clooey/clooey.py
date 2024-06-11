import ast
from jinja2 import Template


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

    exec(program, {'input': custom_input})