import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objs as go

from shiny import reactive, render, ui, App
from shinywidgets import output_widget, render_widget


df = pd.read_csv(Path(__file__).parent / "survey_results_public.csv")
colnames = df.columns.to_list()

def tabulate(var, data=df):
    return data[var].str.split(";").explode().value_counts()

def get_unique_values(var, data=df):
    return data[var].str.split(";").explode().drop_duplicates().to_list()

def make_filter(var, vals):
    """
    Return a bool Series where any of `vals` are found
    in the ;-separated list column `var`
    """
    print(var)
    print(vals)
    setvals = set(vals)
    return df[var].fillna("").str.split(";").apply(lambda x: len(setvals.intersection(x)) > 0)

def find_differences(var, filter1, filter2):
    print(sum(filter1))
    left = 100 * tabulate(var, df[filter1]) / sum(filter1)
    right = 100 * tabulate(var, df[filter2]) / sum(filter2)
    print(left)
    print(right)

    result = left.to_frame("left").join(right.to_frame("right"), how = "outer")
    return result.assign(diff = result['left'] - result['right']).sort_values('diff')


app_ui = ui.page_fluid(
    ui.row(
        ui.column(6,
            ui.input_text("left_label", label = "", value = "Left"),
            ui.div({"class": "filter-selector"},
                ui.input_selectize(
                    "left_var", label="Variable",
                    choices=colnames,
                    selected="Employment"
                ),
                ui.output_ui("left_val_selector"),
            ),
            ui.div(
                "N: ",
                ui.output_text("left_n", inline=True),
            )
        ),
        ui.column(6,
            ui.input_text("right_label", label = "", value = "Right"),
            ui.div(
                ui.input_selectize(
                    "right_var", label="Variable",
                    choices=colnames,
                    selected="Employment"
                ),
                ui.output_ui("right_val_selector")
            ),
            ui.div(
                "N: ",
                ui.output_text("right_n", inline=True),
            )
        )
    ),
    ui.row(
        ui.column(12,
            ui.input_selectize(
                "main_var", label="Variable",
                choices=colnames,
                selected="Employment"
            ),
            # ui.output_table("my_widget"),
            output_widget("my_widget")
        )
    )
)

def server(input, output, session):

    @reactive.Calc
    def left_filter():
        return make_filter(input.left_var(), input.left_vals())

    @output
    @render.text
    def left_n():
        return sum(left_filter())

    @reactive.Calc
    def right_filter():
        return make_filter(input.right_var(), input.right_vals())

    @output
    @render.text
    def right_n():
        return sum(right_filter())

    @output
    @render.ui
    def left_val_selector():
        return ui.input_selectize(
            "left_vals", label="Values",
            choices=get_unique_values(input.left_var()),
            selected=[],
            multiple=True
        )

    @output
    @render.ui
    def right_val_selector():
        return ui.input_selectize(
            "right_vals", label="Values",
            choices=get_unique_values(input.right_var()),
            selected=[],
            multiple=True
        )
    
    @output
    @render_widget
    # @render.table
    def my_widget():
        result = find_differences(input.main_var(), left_filter(), right_filter())
        # return result
        plot_data = result[["left", "right"]].rename(columns={
            "left": input.left_label(),
            "right": input.right_label()
        })
        fig = px.bar(plot_data, barmode="group", orientation="h")
        return fig


app = App(app_ui, server)
