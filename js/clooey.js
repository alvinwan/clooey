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
        prompts.push(matches[1]);
    }

    return prompts;
}

TEMPLATE_FORM = `
<form method="post">
    {% for input in inputs %}
    <label>{{ input }}</label>
    <input type="text" name="{{ loop.index }}">
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
    return nunjucks.renderString(template, { inputs: cli });
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