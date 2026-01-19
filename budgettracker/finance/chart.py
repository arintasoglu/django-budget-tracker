import plotly.express as px


def generate_expense_income_chart(total_expense, total_income):
    x_data = ["Einnahmen", "Ausgaben"]
    y_data = [total_income, total_expense]
    fig = px.bar(
        x=x_data,
        y=y_data,
        title="Einnahmen vs. Ausgaben",
        labels={"x": "Typ", "y": "Betrag"},
        color=x_data,
        color_discrete_map={
            "Einnahmen": "#2ecc71",
            "Ausgaben": "#e74c3c",
        },
    )
    fig.update_layout(legend_title_text="Typ")

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
