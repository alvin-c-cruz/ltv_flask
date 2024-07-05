app_name = "bank"
app_label = "Bank"
menu_label = (app_name, f"/{app_name}", app_label)


from .views import bp
from .models import Bank

