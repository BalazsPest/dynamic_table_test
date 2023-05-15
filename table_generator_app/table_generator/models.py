from django.db import models
from django.db import connection

def field_generator(req_field):
    if req_field == "string":
        return models.CharField(max_length=255)
    elif req_field == "boolean":
        return models.BooleanField()
    elif req_field == "integer":
        return models.IntegerField()
    else:
        raise ValueError("Restricted field type: ", req_field)
    

def get_fields_from_req(fields):
    field_dict = {}
    for field in fields:
        field_dict.update({field['field_name']: field_generator(field['field_type'])})
    return field_dict


class DynamicTableManager(models.Manager):
    def create_model(self, module, table_name, fields):
        self.table_name = table_name
        self.model_fields = get_fields_from_req(fields)
        class Meta:
            pass
        attrs = {'__module__': module, 'Meta': Meta}

        if self.model_fields:
            attrs.update(self.model_fields)

        model_class = type(table_name, (models.Model,), attrs)

        self.model_fields = attrs
        
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model_class)

        return model_class

class DynamicTable(models.Model):
    table_name = models.CharField(max_length=255)
    model_fields = models.JSONField(default=dict)

    objects = DynamicTableManager()

    def update_model_fields(self, model, fields,field_data):
        self.model_fields = fields
        self.save()

        field_list = []
        for field in field_data:
            field_list.append({
                "new_field":{"name":field.get("new_field")['field_name'],"type": field_generator(field.get("new_field")['field_type'])},
                "old_field":field.get("old_field")['field_name']
                }) 
        with connection.schema_editor() as schema_editor:
            for field in field_list:
                if hasattr(model, field['old_field']):
                    delattr(model, field['old_field'])

                model.add_to_class(field.get("new_field")["name"], field.get("new_field")["type"])

                schema_editor.alter_field(model, model._meta.get_field(field.get("old_field")), field.get("new_field")['type'], strict=True)

