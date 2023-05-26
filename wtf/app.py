from pathlib import Path
import random


from shiny import App, render, ui, reactive


def local_file(path):
    return Path(__file__).parent / path


def click_button_on_load(id):
    "Use jQuery to fire event `id` on shiny:connected"
    
    script = f"""
        $(document).on('shiny:connected', function(event) {{
        Shiny.setInputValue(
            '{id}', 
            1
        );
        }});
    """
    return ui.tags.script(ui.HTML(script))


app_ui = ui.page_fixed(
    ui.include_css(local_file("style.css")),
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
        ui.input_action_button("redo", ui.output_text("button_msg")),
    ),
    click_button_on_load("redo"),
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
    buttons = ["Ship it!", "YOLO!", "Rebase!", "Pull!", "Fork!"]

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
