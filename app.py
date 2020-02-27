import local_data as sample_data
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link
from altair import Chart, X, Y, Axis, Data, DataFormat

# load a simple dataset as a pandas DataFrame
from vega_datasets import data

cars = data.cars()
electricity = data.iowa_electricity()
barley_yield = data.barley()


def create_app():
    app = Flask(__name__)

    # Extensions
    nav = Nav()
    nav.init_app(app)

    bs = Bootstrap()
    bs.init_app(app)

    @nav.navigation()
    def mynavbar():
        return Navbar(
            "Flasked Altair Demo",
            View("Home", "index"),
            View("Cars charts", "show_cars"),
            View("Electricity charts", "show_electricity"),
            Subgroup(
                "References",
                Link("Altair", "https://altair-viz.github.io/index.html"),
                Link("Vega-Lite", "https://vega.github.io/vega-lite/"),
                Link("D3", "http://d3js.org/"),
                Link("Flask", "http://flask.pocoo.org/"),
            ),
        )

    ##########################
    # Flask routes
    ##########################
    # render index.html home page
    @app.route("/")
    def index():
        return render_template("index.html")

    # render cars.html page
    @app.route("/cars")
    def show_cars():
        return render_template("cars.html")

    # render iowa electricity.html
    @app.route("/electricity")
    def show_electricity():
        return render_template("electricity.html")

    #########################
    # Altair Data Routes
    #########################

    WIDTH = 800
    HEIGHT = 300

    @app.route("/data/waterfall")
    def data_waterfall():
        chart = (
            Chart(data=sample_data.df_water, width=WIDTH,)
            .mark_bar(color="gray")
            .encode(
                X("Name", axis=Axis(title="Sample")),
                Y("Value", axis=Axis(title="Value")),
            )
            .interactive()
        )
        return chart.to_json()

    @app.route("/data/line")
    def data_line():
        chart = (
            Chart(data=sample_data.df_list, height=HEIGHT, width=WIDTH)
            .mark_line(color="green")
            .encode(
                X("name", axis=Axis(title="Sample")),
                Y("data", axis=Axis(title="Value")),
            )
            .interactive()
        )
        return chart.to_json()

    @app.route("/data/multiline")
    def data_multiline():
        chart = (
            Chart(data=sample_data.df_stocks, height=HEIGHT, width=WIDTH)
            .mark_line()
            .encode(color="symbol:N", x="date:T", y="price:Q",)
            .interactive()
        )
        return chart.to_json()

    @app.route("/data/stocks")
    def stocks():
        chart = (
            Chart(data=sample_data.df_stocks, height=HEIGHT, width=WIDTH)
            .mark_bar()
            .encode(color="symbol:N", x="date:T", y="price:Q",)
            .interactive()
        )
        return chart.to_json()

    @app.route("/data/scatter")
    def scatter():
        chart = (
            Chart(sample_data.df_0, height=HEIGHT, width=WIDTH)
            .mark_circle()
            .encode(x="name:N", y="y2:Q")
            .interactive()
        )
        return chart.to_json()

    @app.route("/data/bar")
    def data_bar():
        chart = (
            Chart(data=sample_data.df_list, height=HEIGHT, width=WIDTH)
            .mark_bar(color="yellow")
            .encode(
                X("name", axis=Axis(title="Sample")),
                Y("data", axis=Axis(title="Value")),
            )
            .interactive()
        )
        return chart.to_json()

    # Creates graph for cars
    @app.route("/data/cars")
    def cars_demo():

        chart = (
            Chart(data=cars, height=700, width=700)
            .mark_point()
            .encode(x="Horsepower", y="Miles_per_Gallon", color="Origin",)
            .interactive()
        )
        return chart.to_json()

    # Creates graph for IOWA electricity consumption
    @app.route("/data/electricity")
    def electricity_demo():

        chart = (
            Chart(data=electricity, height=700, width=700)
            .mark_area()
            .encode(x="year:T", y="net_generation:Q", color="source:N")
            .interactive()
        )
        return chart.to_json()

    # Creates graph for IOWA electricity consumption
    @app.route("/data/barley_yield")
    def barley_yield_demo():

        chart = (
            Chart(data=barley_yield, height=400, width=150)
            .mark_bar()
            .encode(x="year:O", y="sum(yield):Q", color="year:N", column="site:N")
            .interactive()
        )
        return chart.to_json()

    return app
