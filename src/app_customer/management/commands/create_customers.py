from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from app_customer.models import CustomerModel

import csv
import codecs


class Command(BaseCommand):
    help = "Command for Create All Customers"

    def handle(self, *args, **options):
        staffs_path = "customers.csv"
        with open(staffs_path, "rb") as staffs_file:
            customer_reader = csv.reader(codecs.iterdecode(staffs_file, "utf-8"))
            customer_header = next(customer_reader)
            for row in customer_reader:
                _object_dict = {key: value for key, value in zip(customer_header, row)}
                try:
                    customer_obj = CustomerModel.objects.create(
                        full_name=_object_dict["full_name"],
                        customer_code=_object_dict["customer_code"],
                    )
                except IntegrityError:
                    pass
