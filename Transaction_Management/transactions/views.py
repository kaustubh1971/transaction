from datetime import date
import json

from django.db.models import F
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.db import transaction

# Create your views here.
from .models import Transaction, ArticleMaster, TransactionLine,\
    BranchMaster, ColorMaster, ArticleMaster, DepartmentMaster, \
    CompanyLedgerMaster, Inventory
from .utils import required_field_difference,extra_fields_response, \
    missing_fields_response, JSONResponse
from .error_messages import Message
from .serializers import TransactionSerializer


@api_view(["POST"])
def create_new_transaction(request):
    try:
        required_fields = [
            'company_name', 'branch_name',
            'department_name', 'line_item_list'
        ]
        optional_fields = ['status','remark']
        data = request.body.decode("utf-8")
        import ast
        data = ast.literal_eval(data)
        # convert unicode to normal string
        post_params_key = map(str, data.keys())
        required, not_needed = required_field_difference(
            required_fields,
            optional_fields,
            post_params_key)
        # if extra fields is provided
        if not_needed:
            return extra_fields_response(not_needed)
        # if required field not provided
        if required:
            return missing_fields_response(required)
        company_name = data.get('company_name') 
        branch_name = data.get('branch_name')
        department_name = data.get('department_name')
        company_name = company_name.strip().upper()
        branch_name = branch_name.strip().upper()
        department_name = department_name.strip().upper()
        status = data.get('status') or None
        remark = data.get('remark') or None
        line_item_list = data.get('line_item_list')

        if status:
            status = status.strip().upper() 
            if status not in ["PENDING", "COMPLETED", "CLOSE"]:
                return JSONResponse({
                    'code': 0,
                    'response': {},
                    'message': Message.code(1).format("status")
                    })

        with transaction.atomic():
            company_object, created = CompanyLedgerMaster.objects.get_or_create(
                name = company_name
            )
            branch_object, created = BranchMaster.objects.get_or_create(
                name = branch_name
            )
            department_object, created = DepartmentMaster.objects.get_or_create(
                name = department_name
            )

            tran_object = Transaction.objects.create(
                company = company_object,
                branch = branch_object,
                department = department_object,
                status = status,
            )

            for item in line_item_list:
                rate_per_unit = item.get('rate_per_unit') or None
                unit = item.get('unit') or None
                quantity = item.get('quantity') or None
                article_name = item.get('article_name') or None
                color = item.get('color') or None

                color = color.strip().upper()
                article_name = article_name.strip().upper()

                if any([rate_per_unit, unit, quantity]):
                    if not all([rate_per_unit, unit, quantity]):
                        continue

                    try:
                        unit = unit.strip().upper()
                    except:
                        continue
                    if unit not in ["KG", "METER"]:
                        continue 
                    
                    try:
                        rate_per_unit = int(rate_per_unit)
                    except:
                        continue

                    try:
                        quantity = float(quantity)
                    except:
                        continue
                
                article_object, created = ArticleMaster.objects.get_or_create(
                    name = article_name
                )
                color_object, created = ColorMaster.objects.get_or_create(
                    name = color
                )

                tran_details = tran_object.tran_line.values_list("article__name","color__name")
                combination_present = False
                for k in tran_details:
                    if k[0] == article_name and k[1] == color:
                        combination_present = True
                        break
                
                if combination_present:
                    continue

                transaction_line = TransactionLine.objects.create(
                    article = article_object,
                    color = color_object
                )
                transaction_line.rate_per_unit = rate_per_unit
                transaction_line.unit = unit
                transaction_line.quantity = quantity
                transaction_line.article = article_object
                transaction_line.color = color_object
                transaction_line.save()
                tran_object.tran_line.add(transaction_line)
            
            if remark:
                tran_object.remark = remark
            tran_object.save()
            return JSONResponse({
                'code': 1,
                'response': {},
                'message': Message.code(102)
                })
    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': Message.code(10)
            })



@api_view(["POST"])
def add_multiple_inventory_items(request):
    try:
        required_fields = [
            'invetory_list', 'timeline_id'
        ]
        optional_fields = []
        data = request.body.decode("utf-8")
        import ast
        data = ast.literal_eval(data)
        # convert unicode to normal string
        post_params_key = map(str, data.keys())
        required, not_needed = required_field_difference(
            required_fields,
            optional_fields,
            post_params_key)
        # if extra fields is provided
        if not_needed:
            return extra_fields_response(not_needed)
        # if required field not provided
        if required:
            return missing_fields_response(required)
        # data = request.data
        timeline_id = data.get('timeline_id')
        invetory_list = data.get('invetory_list')

        try:
            tran_line_object = TransactionLine.objects.get(
                id=timeline_id
            )
        except:
            return JSONResponse({
                'code': 0,
                'response': {},
                'message': Message.code(1).format("timeline_id")
                })

        with transaction.atomic():

            for item in invetory_list:
                gross_quantity = item.get('gross_quantity') or None
                unit = item.get('unit') or None
                company_name = item.get('company_name') or None
                article_name = item.get('article_name') or None
                color = item.get('color') or None
                net_quantity = item.get('net_quantity') or None


                if not all([
                    company_name,
                    article_name,
                    color
                    ]):
                    continue
                
                try: 
                    company_name = company_name.strip().upper()       
                    company_object = CompanyLedgerMaster.objects.get(
                        name = company_name
                    )
                except:
                    continue

                try:
                    article_name = article_name.strip().upper()
                    article_object = ArticleMaster.objects.get(
                        name = article_name
                    )
                except:
                    continue
                
                try:
                    color = color.strip().upper()
                    color_object = ColorMaster.objects.get(
                        name = color
                    )
                except:
                    continue
                
                if any([unit, gross_quantity, net_quantity]):
                    if not all([unit, gross_quantity, net_quantity]):
                        continue

                    try:
                        unit = unit.strip().upper()
                    except:
                        continue
                    if unit not in ["KG", "METER"]:
                        continue 
                   
                    try:
                        gross_quantity = float(gross_quantity)
                    except:
                        continue

                    try:
                        net_quantity = float(net_quantity)
                    except:
                        continue
                
                inventory_object = Inventory.objects.create(
                    company = company_object,
                    article = article_object,
                    color = color_object,
                )
                if any([unit, gross_quantity, net_quantity]):
                    inventory_object.gross_quantity = gross_quantity
                    inventory_object.net_quantity = net_quantity
                    inventory_object.unit = unit
                inventory_object.save()
                tran_line_object.inventory.add(inventory_object)
                tran_line_object.save()

            return JSONResponse({
                'code': 1,
                'response': {},
                'message': Message.code(102)
                })
    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': Message.code(10)
            })


@api_view(["DELETE"])
def delete_transaction(request):
    try:
        tran_id = request.GET.get("tran_id")
        if not tran_id:
            return missing_fields_response(["tran_id"])

        try:
            tran_object = Transaction.objects.get(
                id=tran_id
            )
        except:
            return JSONResponse({
                'code': 0,
                'response': {},
                'message': Message.code(1).format("tran_id")
                })

        line_object = tran_object.tran_line
        if line_object:
            list_data = line_object.values_list("inventory", flat=True)
            inventory_exists = False
            for i in list_data:
                if i != None:
                    inventory_exists = True
                    break
            if inventory_exists:
                return JSONResponse({
                    'code': 0,
                    'response': {},
                    'message': Message.code(2)
                    })

        tran_object.delete()
        return JSONResponse({
            'code': 1,
            'response': {},
            'message': Message.code(103)
            })

    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': Message.code(10)
            })


@api_view(["GET"])
def get_transaction_details(request):
    try:
        tran_id = request.GET.get("tran_id")
        if not tran_id:
            return missing_fields_response(["tran_id"])

        try:
            tran_object = Transaction.objects.get(
                id=tran_id
            )
        except:
            return JSONResponse({
                'code': 0,
                'response': {},
                'message': Message.code(1).format("tran_id")
                })

        tran_details = TransactionSerializer(tran_object)

        return JSONResponse({
            'code': 1,
            'response': tran_details.data,
            'message': Message.code(101)
            })

    except Exception as e:
        return JSONResponse({
            'code': -1,
            'response': {},
            'message': Message.code(10)
            })