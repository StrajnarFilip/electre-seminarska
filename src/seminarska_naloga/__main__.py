from flask import Flask, render_template, make_response, request, session, redirect
from os import urandom, environ
import numpy
from seminarska_naloga.calculate import electre_method

app = Flask(
    __name__,
    static_folder="static",
    static_url_path='/static',
)


@app.route("/")
def home():
    return render_template("index.html", name="Filip")


@app.route("/", methods=["POST"])
def number_of_criteria():
    session["alternatives"] = int(request.form["alternatives"])
    session["criteria"] = int(request.form["criteria"])
    return redirect("/criteria")


@app.route("/criteria")
def criteria_view():
    return render_template("criteria.html", number_of_weights=range(session["criteria"]))


@app.route("/criteria", methods=["POST"])
def criteria_submit():
    criteria = []

    for i in range(session["criteria"]):
        current_name = request.form[f"name_{i}"]
        current_value = request.form[f"value_{i}"]
        criteria.append((current_name, float(current_value)))

    session["criteria_values"] = criteria

    return redirect("/alternatives")


@app.route("/alternatives")
def alternatives_view():
    return render_template("alternatives.html", number_of_alternatives=range(session["alternatives"]))


@app.route("/alternatives", methods=["POST"])
def alternatives_submit():
    alternatives = []

    for i in range(session["alternatives"]):
        current_name = request.form[f"name_{i}"]
        alternatives.append(current_name)

    session["alternatives_values"] = alternatives
    return redirect("/values")


@app.route("/values")
def values_view():
    alternatives: list[str] = session["alternatives_values"]
    criteria = session["criteria_values"]

    full_alternatives = [(a, [(c[0], f"{i}_{j}") for j, c in enumerate(criteria)]) for i, a in enumerate(alternatives)]
    print(full_alternatives)
    return render_template("values.html", full_alternatives=full_alternatives)

@app.route("/values", methods=["POST"])
def values_submit():
    alternatives: list[str] = session["alternatives_values"]
    criteria = session["criteria_values"]
    data = numpy.array([[float(request.form[f"{i}_{j}"]) for j,_ in enumerate(criteria) ] for i,_ in enumerate(alternatives)])
    weights = [c[1] for c in criteria]
    print(data)
    print(weights)
    calculated = electre_method(weights,data)
    print(calculated)
    return calculated

app.config.update(SECRET_KEY=urandom(32).hex())

app.run("0.0.0.0", 5000)
