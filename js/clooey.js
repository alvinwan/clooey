class CLI {
    constructor(inputs, title = '', description = '') {
        this.inputs = inputs;
        this.title = title;
        this.description = description;
    }
}

class Input {
    constructor(label, placeholder = '') {
        this.label = label;
        this.placeholder = placeholder;
    }
}

/**
 * Converts a piece of Python source code into a list of prompts. Assumes that
 * all calls to the input function contain only a string as an argument. No
 * variables.
 * 
 * @param {*} pythonCode - stringified Python source code
 * @returns - list of strings, representing input prompts
 */
function parse(pythonCode) {
    const inputPromptRegex = /input\(["']([^"']+)["']\)/g;
    let matches;
    const prompts = [];

    while ((matches = inputPromptRegex.exec(pythonCode)) !== null) {
        prompts.push(parsePrompt(matches[1]));
    }

    const docComment = pythonCode.match(/(?:\"\"\"|\'\'\')([\s\S]*?)(?:\"\"\"|\'\'\')/);
    let title = '', description = '';
    
    if (docComment) {
        const docs = docComment[1].trim().split('\n');
        title = docs[0].trim();
        description = docs.slice(1).join('\n').trim();
    }

    return new CLI(prompts, title, description);
}

/**
 * Parse the prompt into a label and placeholder.
 * 
 * @param {*} prompt - raw string prompt
 * @returns - Input object
 * 
 * Examples:
 * 
 * console.log(parsePrompt("Your city [Seattle]:"));
 * console.log(parsePrompt("Your city: [Seattle]"));
 * console.log(parsePrompt("Your city \\[Seattle\\]:"));
 * console.log(parsePrompt("Your city \\[Seattle\\]: [Placeholder]"));
 * 
 * should give the following outputs
 * 
 * Input {label: 'Your city :', placeholder: 'Seattle'}
 * Input {label: 'Your city:', placeholder: 'Seattle'}
 * Input {label: 'Your city [Seattle]:', placeholder: ''}
 * Input {label: 'Your city [Seattle]:', placeholder: 'Placeholder'}
 */
function parsePrompt(prompt) {
    // Define the pattern to match the input string
    const pattern = /^(.*?)(?<!\\)\[(.*?)(?<!\\)\](.*)?$/;
    const match = prompt.match(pattern);
    
    let label, placeholder;
    
    if (match) {
        var suffix = match[3] ? match[3] : '';
        label = (match[1] + suffix).trim();
        placeholder = match[2].trim();
    } else {
        label = prompt;
        placeholder = '';
    }

    // Replace escaped square brackets with actual square brackets
    label = label.replace('\\[', '[').replace('\\]', ']');
    
    return new Input(label, placeholder);
}

TEMPLATE_FORM = `
{% if cli.title %}<h1>{{ cli.title }}</h1>{% endif %}
{% if cli.description %}<p>{{ cli.description }}</p>{% endif %}
<form method="post">
    {% for input in cli.inputs %}
    <label>{{ input.label }}</label>
    <input type="text" name="{{ loop.index }}" placeholder="{{ input.placeholder }}">
    {% endfor %}
    <input type="submit" value="submit">
</form>
`

/**
 * Generates form from CLI.
 * 
 * Note that `nunjucks does not sandbox execution so it is not safe to run
 * user-defined templates or inject user-defined content into template
 * definitions.` As a result, the template passed to this function should be
 * developer-provided, not user-provided.
 * 
 * @param {*} cli - list of strings, representings input prompts
 * @param {*} template - nunjucks template
 * @returns - HTML form
 */
function generate(cli, template) {
    template = template || TEMPLATE_FORM;
    return nunjucks.renderString(template, { cli });
}

/**
 * Execute the provided Python script with the given predetermined input
 * responses.
 * 
 * TODO: May need to save and restore the original stdin handler.
 * 
 * @param {*} responses - list of strings, representing responses
 * @param {*} pythonCode - stringified Python source code
 * @param {*} pyodide - optional argument, for the active pyodide instance
 */
async function execute(responses, pythonCode, pyodide) {
    if (!pyodide) {
        const { loadPyodide } = await import("https://cdn.jsdelivr.net/pyodide/v0.26.1/full/pyodide.mjs");
        pyodide = await loadPyodide();
    }

    // Calls to stdin simply returns from the list of responses
    var responseIndex = 0;
    pyodide.setStdin({ stdin: () => { return responses[responseIndex++ ]; }});

    // Run Python
    var out = pyodide.runPython(pythonCode);
    return out;
}

/**
 * Convenience utility to get submission data from a form.
 * 
 * @param {*} el - DOM element
 * @returns - list of strings, representing responses
 */
function getResponsesFromForm(form) {
    const formData = new FormData(form);

    var responses = [];
    for (const [key, value] of formData) {
        responses[parseInt(key) - 1] = value;
    }
    return responses;
}