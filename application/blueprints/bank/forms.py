from dataclasses import dataclass
from sqlalchemy import func
from application.extensions import db
from .models import Bank as Obj
from .models import UserBank as Preparer
from . import app_name


@dataclass
class Form:
    id: int = None
    bank_name: str = ""
    short_name: str = ""
    bank_code: str = ""
    priority: int = 0
    
    user_prepare_id: int = None
    user_prepare: str = ""

    errors = {}

    def _attributes(self):
        attributes = [x for x in dir(self) if (not x.startswith("_"))]
        for i in ("user_prepare_id", "user_prepare", "errors", "active"):
            try:
                attributes.remove(i)
            except ValueError:
                pass
        return attributes

    def _populate(self, object):
        for i in self._attributes():
            setattr(self, i, getattr(object, i))

        self.user_prepare = object.user_prepare

    def _save(self):
        if self.id is None:
            # Add a new record
            _dict = {}
            for i in self._attributes(): _dict[i] = getattr(self, i)

            record = Obj(**_dict)
            record.active = True

            db.session.add(record)
            db.session.commit()

            _dict = {
                f"{app_name}_id": record.id
            }
            preparer = Preparer(**_dict)
            preparer.user_id = self.user_prepare_id

            db.session.add(preparer)
            db.session.commit()

        else:
            # Update an existing record
            record = Obj.query.get_or_404(self.id)
            _dict = {
                f"{app_name}_id": record.id
            }
            preparer = Preparer.query.filter_by(**_dict).first()

            if record:
                for i in self._attributes():
                    setattr(record, i, getattr(self, i))
                preparer.user_id = self.user_prepare_id

            db.session.commit()

    def _post(self, request_form):
        self.id = request_form.get(f'{app_name}_id')
        for i in self._attributes():
            if i != "id":
                if i in ('priority',):
                    setattr(self, i, int(request_form.get(i)))
                else:
                    setattr(self, i, request_form.get(i))

    def _validate_on_submit(self):
        self.errors = {}

        if not self.bank_name:
            self.errors["bank_name"] = "Please type bank name."

        if not self.short_name:
            self.errors["short_name"] = "Please type short name."

        if not self.bank_code:
            self.errors["bank_code"] = "Please type bank code."

        if not self.priority:
            self.errors["priority"] = "Please type order number."

        if not self.errors:
            return True
        else:
            return False    
