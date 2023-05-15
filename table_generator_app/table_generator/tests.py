from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class DynamicTableTest(APITestCase):

    def createBaseModel(self,table_name):
        url = reverse('generate_dynamic_table')
        data = {
            "table_name": table_name,
                "fields": [
        {
            "field_name": "f_name",
            "field_type": "string"
        },
        {
            "field_name": "f_name_two",
            "field_type": "boolean"
        }]}
        return self.client.post(url, data, format='json')

    def test_create_dynamic_table(self):
        table_name = "t1"
        response = self.createBaseModel(table_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['table_name'], table_name)

    def test_update_dynamic_table(self):
        id = self.createBaseModel("t2").data["id"]
        url = reverse('update_dynamic_table', args=(id,))
        data = {
    "fields": [
        {
            "new_field": {
                "field_name": "new_f_name",
                "field_type": "string"
            },
            "old_field": {
                "field_name": "f_name",
                "field_type": "string"
            }
        },
        {
            "new_field": {
                "field_name": "new_b_name",
                "field_type": "string"
            },
            "old_field": {
                "field_name": "f_name_two",
                "field_type": "boolean"
            }
        }
    ]
}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_add_dynamic_rows(self):
        id = self.createBaseModel("t3").data["id"]
        url = reverse('add_dynamic_row', args=(id,))
        data = {
    "records": [
        {
            "f_name": "new_record",
            "f_name_two": True
        }
    ]
}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



    def test_get_records_of_dynamic_table(self):
        id = self.createBaseModel("t3").data["id"]
        url = reverse('get_dynamic_rows', args=(id,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
