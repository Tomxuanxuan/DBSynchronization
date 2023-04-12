#!/usr/bin/env python
# encoding: utf-8
"""
@author: tx
@file: table.py
@time: 2023/4/11 14:54
@desc:
"""
tables = [
    {
        "name": "RMS_Medicament",
        "key": [
            "MedicamentId",
            "VarietyId",
            "BarCode",
            "ClientId",
            "ClientCode",
            "CustomerId",
            "CASNumber",
            "Name",
            "EnglishName",
            "Speci",
            "SpeciUnit",
            "Unit",
            "Remain",
            "Manufacturer",
            "Distributor",
            "ProductionDate",
            "ExpirationDate",
            "ShelfLife",
            "ShelfLifeWarningValue",
            "UseDaysWarningValue",
            "IsWeigh",
            "WeighFlag",
            "Purity",
            "Price",
            "Place",
            "Status",
            "IsSupervise",
            "ByUserDate",
            "ByUserId",
            "ByUserName",
            "PutInDate",
            "PutInUserId",
            "PutInUserName",
            "Remark1",
            "Remark2",
            "Remark3",
            "Remark4",
            "Remark5",
            "Remark6",
            "Remark7",
            "Remark8",
            "Remark9",
            "Remark10",
            "IsAdd",
        ]
    },
    {
        "name": "RMS_MedicamentRecord",
        "key": [
            "RecordId",
            "ClientId",
            "ClientCode",
            "CustomerId",
            "VarietyId",
            "MedicamentId",
            "RecordType",
            "Price",
            "RecordRemain",
            "UseQuantity",
            "IsEmpty",
            "CreateDate",
            "CreateUserId",
            "CreateUserName",
            "IsAdd",
        ]}
]



