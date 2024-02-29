from peewee import *

database = MySQLDatabase('testdatenbank', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': 'localhost', 'port': 3306, 'user': 'root', 'passwd': 'Local-Root-2106'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Department(BaseModel):
    department_id = AutoField(column_name='DepartmentID')
    department_name = CharField(column_name='DepartmentName', null=True, unique=True)

    class Meta:
        table_name = 'department'

class Employee(BaseModel):
    department_id = IntegerField(column_name='DepartmentID', index=True)
    email = CharField(column_name='Email', null=True)
    employee_id = AutoField(column_name='EmployeeID')
    first_name = CharField(column_name='FirstName', null=True)
    last_name = CharField(column_name='LastName', null=True)

    class Meta:
        table_name = 'employee'

class Requesttype(BaseModel):
    type_id = AutoField(column_name='TypeID')
    type_name = CharField(column_name='TypeName', constraints=[SQL("DEFAULT '0'")], unique=True)

    class Meta:
        table_name = 'requesttype'

class Status(BaseModel):
    status_id = AutoField(column_name='StatusID')
    status_name = CharField(column_name='StatusName', null=True, unique=True)

    class Meta:
        table_name = 'status'

class Leaverequest(BaseModel):
    begin_date = DateField(column_name='Begin_Date', null=True)
    employee = ForeignKeyField(column_name='EmployeeID', field='employee_id', model=Employee)
    end_date = DateField(column_name='End_Date', null=True)
    request_id = AutoField(column_name='RequestID')
    status = ForeignKeyField(column_name='Status_id', field='status_id', model=Status, null=True)
    type = ForeignKeyField(column_name='Type_id', field='type_id', model=Requesttype, null=True)

    class Meta:
        table_name = 'leaverequest'
