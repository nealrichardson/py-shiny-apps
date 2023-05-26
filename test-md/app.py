import re

from shiny import App, render, ui

def unescape(x):
    """
    Some code arguments inside the markdown get escaped into HTML.
    Un-escape them so we can evaluate them as Python code.
    """

    x = re.sub('&quot;', '"', x)
    return x

def eval_shiny_in_md(code, deps):
    rendered = eval(code).render()
    deps.append(rendered['dependencies'])
    return rendered['html']

def ui_from_md(md):
    html = ui.markdown(md)
    # Collect any dependencies from the Tags inside the ${{ }} blocks
    deps = []
    # Replace all ${{ expr }} with the result of that Python expr
    html = re.sub(r"\$\{\{ (.*) \}\}", lambda x: eval_shiny_in_md(unescape(x.group()[4:-3]), deps), html)
    # Replace all {id} with ui.output_text(id, inline=True)
    html = re.sub(r"\{(.*?)\}", r'<span id="\1" class="shiny-text-output"></span>', html)
    # Return the dependencies and the HTML from the markdown
    return ui.TagList(*deps, ui.tags.div(ui.HTML(html)))


app_ui = ui.page_fluid(
    ui_from_md("""
        ## Hello Shiny!

        ${{ ui.input_slider("n", "N", 0, 100, 20) }}

        `n * 2` is {n2}
    """)
)

def server(input, output, session):
    @output
    @render.text
    def n2():
        return input.n() * 2


app = App(app_ui, server)
