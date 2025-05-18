from datetime import datetime
from supabase import create_client
import os
from config.supabase_config import supabase

# Initialize Supabase client

class ProductionLine:
    @staticmethod
    def get_all():
        response = supabase.table('production_lines').select('*').execute()
        return response.data

    @staticmethod
    def get_by_id(line_id):
        response = supabase.table('production_lines').select('*').eq('id', str(line_id)).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_supervisor(supervisor_id):
        response = supabase.table('production_lines').select('*').eq('supervisor_id', str(supervisor_id)).execute()
        return response.data

    @staticmethod
    def create(data):
        # Convert IDs to strings
        if 'supervisor_id' in data:
            data['supervisor_id'] = str(data['supervisor_id'])
            
        response = supabase.table('production_lines').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(line_id, data):
        # Convert IDs to strings
        if 'supervisor_id' in data:
            data['supervisor_id'] = str(data['supervisor_id'])
            
        response = supabase.table('production_lines').update(data).eq('id', str(line_id)).execute()
        return response.data[0] if response.data else None

class WorkOrder:
    @staticmethod
    def get_all():
        response = supabase.table('work_orders').select('*').execute()
        return response.data

    @staticmethod
    def get_by_id(order_id):
        response = supabase.table('work_orders').select('*').eq('id', str(order_id)).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_client(client_id):
        response = supabase.table('work_orders').select('*').eq('client_id', str(client_id)).execute()
        return response.data

    @staticmethod
    def get_by_line(line_id):
        response = supabase.table('work_orders').select('*').eq('assigned_line_id', str(line_id)).execute()
        return response.data

    @staticmethod
    def get_by_worker(worker_id):
        response = supabase.table('work_orders').select('*').eq('assigned_worker_id', str(worker_id)).execute()
        return response.data

    @staticmethod
    def create(data):
        # Ensure IDs are strings
        if 'client_id' in data:
            data['client_id'] = str(data['client_id'])
        if 'assigned_line_id' in data:
            data['assigned_line_id'] = str(data['assigned_line_id'])
        if 'assigned_worker_id' in data:
            data['assigned_worker_id'] = str(data['assigned_worker_id'])
            
        response = supabase.table('work_orders').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(order_id, data):
        # Ensure IDs are strings
        if 'client_id' in data:
            data['client_id'] = str(data['client_id'])
        if 'assigned_line_id' in data:
            data['assigned_line_id'] = str(data['assigned_line_id'])
        if 'assigned_worker_id' in data:
            data['assigned_worker_id'] = str(data['assigned_worker_id'])
            
        response = supabase.table('work_orders').update(data).eq('id', str(order_id)).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update_status(order_id, status):
        response = supabase.table('work_orders').update({'status': status}).eq('id', str(order_id)).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def assign_worker(order_id, worker_id):
        response = supabase.table('work_orders').update({'assigned_worker_id': str(worker_id)}).eq('id', str(order_id)).execute()
        return response.data[0] if response.data else None

class Inventory:
    @staticmethod
    def get_all():
        response = supabase.table('inventory').select('*').execute()
        # Convert quantity and reorder_level to integers
        for item in response.data:
            item['quantity'] = int(item['quantity'])
            item['reorder_level'] = int(item['reorder_level'])
        return response.data

    @staticmethod
    def get_by_id(item_id):
        response = supabase.table('inventory').select('*').eq('id', item_id).execute()
        if response.data:
            item = response.data[0]
            item['quantity'] = int(item['quantity'])
            item['reorder_level'] = int(item['reorder_level'])
            return item
        return None

    @staticmethod
    def get_low_stock():
        # First get all inventory items
        response = supabase.table('inventory').select('*').execute()
        # Convert quantity and reorder_level to integers and filter
        return [item for item in response.data 
                if int(item['quantity']) < int(item['reorder_level'])]

    @staticmethod
    def create(data):
        # Convert quantity and reorder_level to integers
        data['quantity'] = int(data['quantity'])
        data['reorder_level'] = int(data['reorder_level'])
        response = supabase.table('inventory').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(item_id, data):
        # Convert quantity and reorder_level to integers if present
        if 'quantity' in data:
            data['quantity'] = int(data['quantity'])
        if 'reorder_level' in data:
            data['reorder_level'] = int(data['reorder_level'])
        response = supabase.table('inventory').update(data).eq('id', item_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update_quantity(item_id, quantity):
        response = supabase.table('inventory').update({'quantity': int(quantity)}).eq('id', item_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def delete(item_id):
        response = supabase.table('inventory').delete().eq('id', item_id).execute()
        return response.data[0] if response.data else None

class Machine:
    @staticmethod
    def get_all():
        response = supabase.table('machines').select('*').execute()
        return response.data

    @staticmethod
    def get_by_id(machine_id):
        response = supabase.table('machines').select('*').eq('id', machine_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_line(line_id):
        response = supabase.table('machines').select('*').eq('line_id', line_id).execute()
        return response.data

    @staticmethod
    def get_by_worker(worker_id):
        response = supabase.table('machines').select('*').eq('assigned_worker_id', worker_id).execute()
        return response.data

    @staticmethod
    def create(data):
        # Handle empty datetime fields
        if 'last_maintenance_date' in data and not data['last_maintenance_date']:
            data['last_maintenance_date'] = None
        if 'next_maintenance_date' in data and not data['next_maintenance_date']:
            data['next_maintenance_date'] = None
            
        response = supabase.table('machines').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(machine_id, data):
        # Handle empty datetime fields
        if 'last_maintenance_date' in data and not data['last_maintenance_date']:
            data['last_maintenance_date'] = None
        if 'next_maintenance_date' in data and not data['next_maintenance_date']:
            data['next_maintenance_date'] = None
            
        response = supabase.table('machines').update(data).eq('id', machine_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update_status(machine_id, status):
        response = supabase.table('machines').update({'status': status}).eq('id', machine_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def delete(machine_id):
        response = supabase.table('machines').delete().eq('id', machine_id).execute()
        return response.data[0] if response.data else None

class WorkerShift:
    @staticmethod
    def get_all():
        response = supabase.table('worker_shifts').select('*').execute()
        return response.data

    @staticmethod
    def get_by_id(shift_id):
        response = supabase.table('worker_shifts').select('*').eq('id', shift_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_line(line_id):
        response = supabase.table('worker_shifts').select('*').eq('line_id', line_id).execute()
        return response.data

    @staticmethod
    def get_by_worker(worker_id):
        response = supabase.table('worker_shifts').select('*').eq('worker_id', worker_id).execute()
        return response.data

    @staticmethod
    def get_current_shift(worker_id):
        now = datetime.now().isoformat()
        response = supabase.table('worker_shifts').select('*').eq('worker_id', worker_id).lte('start_time', now).gte('end_time', now).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def create(data):
        response = supabase.table('worker_shifts').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(shift_id, data):
        response = supabase.table('worker_shifts').update(data).eq('id', shift_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update_status(shift_id, status):
        response = supabase.table('worker_shifts').update({'status': status}).eq('id', shift_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def assign_task(shift_id, task):
        response = supabase.table('worker_shifts').update({'current_task': task}).eq('id', shift_id).execute()
        return response.data[0] if response.data else None

class WorkerProductivity:
    @staticmethod
    def get_worker_stats(worker_id=None, start_date=None, end_date=None):
        query = supabase.table('worker_productivity').select('*')
        if worker_id:
            query = query.eq('worker_id', worker_id)
        if start_date:
            query = query.gte('created_at', start_date)
        if end_date:
            query = query.lte('created_at', end_date)
        response = query.execute()
        return response.data

    @staticmethod
    def create(data):
        response = supabase.table('worker_productivity').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(record_id, data):
        response = supabase.table('worker_productivity').update(data).eq('id', record_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_worker(worker_id):
        response = supabase.table('worker_productivity').select('*').eq('worker_id', worker_id).execute()
        return response.data

    @staticmethod
    def get_by_task(task_id):
        response = supabase.table('worker_productivity').select('*').eq('task_id', task_id).execute()
        return response.data

class KPIMetrics:
    @staticmethod
    def get_metrics(start_date, end_date):
        response = supabase.table('kpi_metrics').select('*').gte('metric_date', start_date).lte('metric_date', end_date).execute()
        return response.data

class Report:
    @staticmethod
    def get_all():
        response = supabase.table('reports').select('*').order('created_at', desc=True).execute()
        return response.data

    @staticmethod
    def get_reports(start_date=None, end_date=None, report_type=None):
        query = supabase.table('reports').select('*')
        
        if start_date:
            query = query.gte('created_at', start_date)
        if end_date:
            query = query.lte('created_at', end_date)
        if report_type:
            query = query.eq('type', report_type)
            
        response = query.order('created_at', desc=True).execute()
        return response.data

    @staticmethod
    def get_by_id(report_id):
        response = supabase.table('reports').select('*').eq('id', report_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def create(data):
        # Ensure all required fields are present
        report_data = {
            'type': data.get('type'),
            'start_date': data.get('start_date'),
            'end_date': data.get('end_date'),
            'status': 'completed',
            'created_at': datetime.now().isoformat()
        }
        response = supabase.table('reports').insert(report_data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(report_id, data):
        response = supabase.table('reports').update(data).eq('id', report_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def delete(report_id):
        response = supabase.table('reports').delete().eq('id', report_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def generate_report(report_type, start_date=None, end_date=None):
        # Validate report type
        if report_type not in ['production', 'inventory', 'machines']:
            return None

        # Create report record
        report_data = {
            'type': report_type,
            'start_date': start_date,
            'end_date': end_date,
            'status': 'completed',
            'created_at': datetime.now().isoformat()
        }
        
        return Report.create(report_data)

class User:
    @staticmethod
    def get_all():
        response = supabase.table('users').select('*').execute()
        return response.data

    @staticmethod
    def get_by_id(user_id):
        response = supabase.table('users').select('*').eq('uid', user_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_email(email):
        response = supabase.table('users').select('*').eq('email', email).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_role(role):
        response = supabase.table('users').select('*').eq('role', role).execute()
        return response.data

    @staticmethod
    def create(data):
        response = supabase.table('users').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(user_id, data):
        response = supabase.table('users').update(data).eq('uid', user_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update_status(user_id, status):
        response = supabase.table('users').update({'status': status}).eq('uid', user_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def delete(user_id):
        response = supabase.table('users').delete().eq('uid', user_id).execute()
        return response.data[0] if response.data else None

class Shift:
    @staticmethod
    def get_all():
        response = supabase.table('shifts').select('*').execute()
        return response.data

    @staticmethod
    def get_by_id(shift_id):
        response = supabase.table('shifts').select('*').eq('id', shift_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_worker(worker_id):
        response = supabase.table('shifts').select('*').eq('worker_id', worker_id).execute()
        return response.data

    @staticmethod
    def get_current_shift(worker_id):
        now = datetime.now().isoformat()
        response = supabase.table('shifts').select('*').eq('worker_id', worker_id).lte('start_time', now).gte('end_time', now).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def create(data):
        response = supabase.table('shifts').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(shift_id, data):
        response = supabase.table('shifts').update(data).eq('id', shift_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update_status(shift_id, status):
        response = supabase.table('shifts').update({'status': status}).eq('id', shift_id).execute()
        return response.data[0] if response.data else None

class Task:
    @staticmethod
    def get_all():
        response = supabase.table('tasks').select('*').execute()
        return response.data

    @staticmethod
    def get_by_id(task_id):
        response = supabase.table('tasks').select('*').eq('id', task_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_worker(worker_id):
        response = supabase.table('tasks').select('*').eq('assigned_worker_id', worker_id).execute()
        return response.data

    @staticmethod
    def get_by_shift(shift_id):
        response = supabase.table('tasks').select('*').eq('shift_id', shift_id).execute()
        return response.data

    @staticmethod
    def create(data):
        response = supabase.table('tasks').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(task_id, data):
        response = supabase.table('tasks').update(data).eq('id', task_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update_status(task_id, status):
        response = supabase.table('tasks').update({'status': status}).eq('id', task_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def assign_worker(task_id, worker_id):
        response = supabase.table('tasks').update({'assigned_worker_id': worker_id}).eq('id', task_id).execute()
        return response.data[0] if response.data else None

class TaskComment:
    @staticmethod
    def get_by_task(task_id):
        response = supabase.table('task_comments').select('*').eq('task_id', task_id).execute()
        return response.data

    @staticmethod
    def create(data):
        response = supabase.table('task_comments').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def delete(comment_id):
        response = supabase.table('task_comments').delete().eq('id', comment_id).execute()
        return response.data[0] if response.data else None 