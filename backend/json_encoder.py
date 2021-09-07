from datetime import date

from quart.json import JSONEncoder


class CustomEncoder(JSONEncoder):
    """
    Custom JSON encoder to handle things like date parsing
    """
    def default(self, o):
        # Return dates as ISO strings
        if isinstance(o, date):
            return o.isoformat()

        return super().default(o)
