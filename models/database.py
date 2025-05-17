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
        response = supabase.table('production_lines').select('*').eq('id', line_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_supervisor(supervisor_id):
        response = supabase.table('production_lines').select('*').eq('supervisor_id', supervisor_id).execute()
        return response.data

    @staticmethod
    def create(data):
        response = supabase.table('production_lines').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(line_id, data):
        response = supabase.table('production_lines').update(data).eq('id', line_id).execute()
        return response.data[0] if response.data else None

class WorkOrder:
    @staticmethod
    def get_all():
        response = supabase.table('work_orders').select('*').execute()
        return response.data

    @staticmethod
    def get_by_id(order_id):
        response = supabase.table('work_orders').select('*').eq('id', order_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_line(line_id):
        response = supabase.table('work_orders').select('*').eq('assigned_line_id', line_id).execute()
        return response.data

    @staticmethod
    def create(data):
        response = supabase.table('work_orders').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(order_id, data):
        response = supabase.table('work_orders').update(data).eq('id', order_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update_status(order_id, status):
        response = supabase.table('work_orders').update({'status': status}).eq('id', order_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def assign_worker(order_id, worker_id):
        response = supabase.table('work_orders').update({'assigned_worker_id': worker_id}).eq('id', order_id).execute()
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
    def get_low_stock():
        # First get all inventory items
        response = supabase.table('inventory').select('*').execute()
        # Convert quantity and reorder_level to integers and filter
        return [item for item in response.data 
                if int(item['quantity']) < int(item['reorder_level'])]

    @staticmethod
    def update_quantity(item_id, quantity):
        response = supabase.table('inventory').update({'quantity': quantity}).eq('id', item_id).execute()
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
    def update_status(machine_id, status):
        response = supabase.table('machines').update({'status': status}).eq('id', machine_id).execute()
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
            query = query.gte('date', start_date)
        if end_date:
            query = query.lte('date', end_date)
        response = query.execute()
        return response.data

class KPIMetrics:
    @staticmethod
    def get_metrics(start_date, end_date):
        response = supabase.table('kpi_metrics').select('*').gte('metric_date', start_date).lte('metric_date', end_date).execute()
        return response.data

class Report:
    @staticmethod
    def get_reports():
        response = supabase.table('reports').select('*').order('created_at', desc=True).execute()
        return response.data

    @staticmethod
    def save_report(data):
        response = supabase.table('reports').insert(data).execute()
        return response.data[0] if response.data else None 