import random

from shiny import App, render, ui, reactive

my_css = """
html {
  height: 100%;
}

body {
    height: 100%;
    width: 100%;
    text-align: center;
    background-color: yellow;
    font-size: 24px;
    font-family: 'Jost', sans-serif;
}

h2 {
    font-size: 48px;
    font-family: 'Lobster', sans-serif;
}

.container {
    height: 100%;
    width: 100%;
    display: table;
    table-layout: fixed;
}

.inside {
    vertical-align: middle;
    display: table-cell;
}
"""

app_ui = ui.page_fixed(
    ui.tags.link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css?family=Jost"
    ),
    ui.tags.link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css?family=Lobster"
    ),
    ui.tags.style(my_css),
    ui.div(
        {"class": "inside"},
        ui.h2("WTF is my open-source strategy?"),
        ui.div(
            ui.output_text("verb", inline=True),
            " ",
            ui.output_text("noun", inline=True),
            " by ",
            ui.output_text("action", inline=True),
            " in order to increase ",
            ui.output_text("maximize", inline=True),
        ),
        ui.br(),
        ui.input_action_button(
            "redo",
            ui.output_text("button_msg")
        ),
    ),
    ui.tags.script(ui.HTML("""
$(document).on('shiny:connected', function(event) {
  Shiny.setInputValue(
    'redo', 
    1
  );
});
    """))
)


def server(input, output, session):
    
    verbs = [
        "Drive",
        "Disrupt",
        "Influence",
        "Amplify",
        "Sanitize",
        "Energize",
    ]
    nouns = [
        "inbound sales leads",
        "machine learning",
        "the developer community",
        "our brand identity",
        "our corporate reputation",
        "the blockchain",
        "our stock price",
        "our Series B funding",
    ]
    by_doing = [
        "writing a blog post",
        "trolling",
        "merging stale pull requests",
        "refactoring the test suite",
        "donating unmaintainable code",
        "upstreaming bugfixes",
        "reviewing pull requests",
        "marking issues as wontfix",
        "writing detailed documentation",
    ]
    maximize_this = [
        "monthly download counts",
        "GitHub stars",
        "Twitter followers",
        "Hackernews upvotes",
        "unique contributors",
        "new contributors",
        "ABI stability",
        "lock-in",
    ]
    buttons = [
        "Ship it!",
        "YOLO!",
        "Rebase!",
        "Pull!",
        "Fork!"
    ]

    def sample_one(wordlist):
        return wordlist[random.randint(0, len(wordlist) - 1)]

    @output
    @render.text
    @reactive.event(input.redo)
    def verb():
        return sample_one(verbs)

    @output
    @render.text
    @reactive.event(input.redo)
    def noun():
        return sample_one(nouns)
       
    @output
    @render.text
    @reactive.event(input.redo)
    def action():
        return sample_one(by_doing)
    
    @output
    @render.text
    @reactive.event(input.redo)
    def maximize():
        return sample_one(maximize_this)

    @output
    @render.text
    @reactive.event(input.redo)
    def button_msg():
        return sample_one(buttons)

app = App(app_ui, server)
