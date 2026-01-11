import plotly.express as px


def generate_expense_income_chart(total_expense, total_income):
    x_data = ["Ausgaben", "Einnahmen"]
    y_data = [total_expense, total_income]
    fig = px.bar(
        x=x_data,
        y=y_data,
        title="Einnahmen vs. Ausgaben",
        labels={"x": "Typ", "y": "Betrag"},
    )

    return fig


def generate_pie_income_chart(context):
    labels = []
    values = []

    for data in context.values():
        labels.append(data["kategorie"])
        values.append(float(data["income"]))

    fig = px.pie(
        names=labels,
        values=values,
        title="Einnahmen nach Kategorie",
    )

    return fig


def generate_pie_expense_chart(context):
    labels = []
    values = []

    for data in context.values():
        labels.append(data["kategorie"])
        values.append(float(data["expense"]))

    fig = px.pie(
        names=labels,
        values=values,
        title="Ausgaben nach Kategorie",
    )

    return fig
