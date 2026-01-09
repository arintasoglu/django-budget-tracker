from import_export import resources, fields
from .models import Buchung, Kategorie
from import_export.widgets import ForeignKeyWidget


class BuchungResource(resources.ModelResource):
    kategorie = fields.Field(
        column_name="kategorie",
        attribute="kategorie",
        widget=ForeignKeyWidget(Kategorie, field="name"),
    )

    class Meta:
        model = Buchung
        fields = ("betrag", "type", "datum", "kategorie", "beschreibung")
        export_order = ("betrag", "type", "datum", "kategorie", "beschreibung")
