from table_generator.models import DynamicTable
from django.apps import apps
from .serializers import DynamicTableSerializer
from rest_framework.views import APIView


from rest_framework import status
from rest_framework.response import Response

def get_dynamic_table_and_model(id):
    dynamic_table = DynamicTable.objects.get(pk=id)
    table_name = "table_generator_" + dynamic_table.table_name
    found_model = None
    for model in apps.get_models():
        if model._meta.db_table == table_name:
            found_model = model
    return dynamic_table, found_model

    

class GenerateDynamicTable(APIView):
    def post(self, request):
        name_data = request.data.get('table_name')
        field_data = request.data.get('fields', [])
        module="table_generator"
        dynamic_table = DynamicTable.objects.create_model(module, name_data, field_data)
        apps.register_model(module, dynamic_table)
        serializer = DynamicTableSerializer(data = {"table_name":name_data, "model_fields":field_data})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateDynamicTable(APIView):
    def put(self, request, id):
        dynamic_table, model = get_dynamic_table_and_model(id)
        field_data = request.data.get('fields', [])
        field_types = [field.get('new_field').get('field_type') for field in field_data]
        field_titles = [field.get('new_field').get('field_name') for field in field_data]
        model_fields = {}
        for i, field_title in enumerate(field_titles):
            model_fields[field_title] = field_types[i]
        try:
            dynamic_table.update_model_fields(model,model_fields,field_data)
        except ValueError as e:
            return Response(f"The following error occured: {e}",status=status.HTTP_400_BAD_REQUEST)
        dynamic_table.model_fields = model_fields
        serializer = DynamicTableSerializer(dynamic_table)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)


class AddDynamicRow(APIView):
    def post(self, request, id):
        _, model = get_dynamic_table_and_model(id)
        for record in request.data['records']:
            m = model(**record)
            m.save()
        return Response(status=status.HTTP_201_CREATED)


class GetDynamicRows(APIView):
    def get(self, request, id):
        try:
            _, model = get_dynamic_table_and_model(id)
        except DynamicTable.DoesNotExist as e:
            return Response(f"The following error occured: {e}",status=status.HTTP_404_NOT_FOUND)
        rows = model.objects.all().values()
        return Response({'rows': list(rows)}, status=status.HTTP_200_OK)
            