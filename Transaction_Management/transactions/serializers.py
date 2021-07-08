from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name")
    branch_name = serializers.CharField(source="branch.name")
    department_name = serializers.CharField(source="department.name")
    tran_line_details = serializers.SerializerMethodField()

    def get_tran_line_details(self, instance):
        return instance.tran_line.values(
            "id",
            "inventory__id",
            "inventory__company__name",
            "inventory__article__name",
            "inventory__color__name",
            "inventory__gross_quantity",
            "inventory__net_quantity",
            "inventory__unit",
            "article__name",
            "color__name",
            "required_on_date",
            "quantity",
            "rate_per_unit",
            "unit"
        )

    class Meta:
        model = Transaction
        fields = [
            'company_name', 'branch_name', 'department_name', 
            'tran_line_details', 'status', 'remark', 'tran_number',
            ]