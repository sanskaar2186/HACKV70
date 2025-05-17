from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from functools import wraps
from models.database import ProductionLine, WorkOrder, WorkerShift, Machine, Inventory
from models.user import User
from datetime import datetime

supervisor = Blueprint('supervisor', __name__, url_prefix='/supervisor')

def supervisor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['role'] != 'supervisor':
            flash('You must be logged in as a supervisor to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@supervisor.route('/dashboard')
@supervisor_required
def supervisor_dashboard():
    try:
        # Get supervisor's production lines
        production_lines = ProductionLine.get_by_supervisor(session['user']['id'])
        
        # Get work orders for these lines
        work_orders = []
        for line in production_lines:
            orders = WorkOrder.get_by_line(line['id'])
            for order in orders:
                order['line_name'] = line['name']
                # Get assigned worker info
                if order.get('assigned_worker_id'):
                    worker = User.get_by_id(order['assigned_worker_id'])
                    if worker:
                        order['worker_name'] = worker['name']
            work_orders.extend(orders)
        
        # Get machines for these lines
        machines = []
        for line in production_lines:
            line_machines = Machine.get_by_line(line['id'])
            machines.extend(line_machines)
        
        # Get inventory items and convert to integers
        inventory = Inventory.get_all()
        for item in inventory:
            item['quantity'] = int(item['quantity'])
            item['reorder_level'] = int(item['reorder_level'])
        
        return render_template('supervisor/dashboard.html',
                             production_lines=production_lines,
                             work_orders=work_orders,
                             machines=machines,
                             inventory=inventory)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return redirect(url_for('auth.login'))

@supervisor.route('/work-orders')
@supervisor_required
def work_orders():
    try:
        # Get supervisor's production lines
        production_lines = ProductionLine.get_by_supervisor(session['user']['id'])
        
        # Get work orders for these lines
        work_orders = []
        for line in production_lines:
            orders = WorkOrder.get_by_line(line['id'])
            for order in orders:
                order['line_name'] = line['name']
                # Get assigned worker info
                if order.get('assigned_worker_id'):
                    worker = User.get_by_id(order['assigned_worker_id'])
                    if worker:
                        order['worker_name'] = worker['name']
            work_orders.extend(orders)
        
        return render_template('supervisor/work_orders.html', 
                             work_orders=work_orders,
                             production_lines=production_lines)
    except Exception as e:
        flash(f'Error loading work orders: {str(e)}', 'error')
        return redirect(url_for('supervisor.supervisor_dashboard'))

@supervisor.route('/update-order-status', methods=['POST'])
@supervisor_required
def update_order_status():
    try:
        data = request.get_json()
        order_id = data.get('orderId')
        new_status = data.get('status')
        
        # Verify the order belongs to supervisor's lines
        order = WorkOrder.get_by_id(order_id)
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'})
        
        line = ProductionLine.get_by_id(order['assigned_line_id'])
        if not line or line['supervisor_id'] != session['user']['id']:
            return jsonify({'success': False, 'message': 'Unauthorized'})
        
        # Update order status
        WorkOrder.update_status(order_id, new_status)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@supervisor.route('/assign-worker', methods=['POST'])
@supervisor_required
def assign_worker():
    try:
        data = request.get_json()
        order_id = data.get('orderId')
        worker_id = data.get('workerId')
        
        # Verify the order belongs to supervisor's lines
        order = WorkOrder.get_by_id(order_id)
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'})
        
        line = ProductionLine.get_by_id(order['assigned_line_id'])
        if not line or line['supervisor_id'] != session['user']['id']:
            return jsonify({'success': False, 'message': 'Unauthorized'})
        
        # Assign worker to order
        WorkOrder.assign_worker(order_id, worker_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@supervisor.route('/get-line-workers/<line_id>')
@supervisor_required
def get_line_workers(line_id):
    try:
        # Verify the line belongs to supervisor
        line = ProductionLine.get_by_id(line_id)
        if not line or line['supervisor_id'] != session['user']['id']:
            return jsonify({'success': False, 'message': 'Unauthorized'})
        
        # Get workers assigned to this line
        shifts = WorkerShift.get_by_line(line_id)
        workers = []
        for shift in shifts:
            worker = User.get_by_id(shift['worker_id'])
            if worker:
                workers.append({
                    'id': worker['id'],
                    'name': worker['name'],
                    'current_task': shift['current_task']
                })
        
        return jsonify({'success': True, 'workers': workers})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@supervisor.route('/workers')
@supervisor_required
def manage_workers():
    try:
        # Get supervisor's production lines
        production_lines = ProductionLine.get_by_supervisor(session['user']['id'])
        
        # Get worker shifts for these lines
        worker_shifts = []
        for line in production_lines:
            shifts = WorkerShift.get_by_line(line['id'])
            for shift in shifts:
                shift['line_name'] = line['name']
                # Get worker info
                worker = User.get_by_id(shift['worker_id'])
                if worker:
                    shift['worker_name'] = worker['name']
            worker_shifts.extend(shifts)
        
        return render_template('supervisor/workers.html',
                             production_lines=production_lines,
                             worker_shifts=worker_shifts)
    except Exception as e:
        flash(f'Error loading workers: {str(e)}', 'error')
        return redirect(url_for('supervisor.supervisor_dashboard'))

@supervisor.route('/tasks')
def manage_tasks():
    if not session.get('user') or session['user']['role'] != 'supervisor':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('supervisor/tasks.html')

@supervisor.route('/machines')
@supervisor_required
def manage_machines():
    try:
        # Get supervisor's production lines
        production_lines = ProductionLine.get_by_supervisor(session['user']['id'])
        
        # Get machines for these lines
        machines = []
        for line in production_lines:
            line_machines = Machine.get_by_line(line['id'])
            for machine in line_machines:
                machine['line_name'] = line['name']
            machines.extend(line_machines)
        
        return render_template('supervisor/machines.html',
                             machines=machines,
                             production_lines=production_lines)
    except Exception as e:
        flash(f'Error loading machines: {str(e)}', 'error')
        return redirect(url_for('supervisor.supervisor_dashboard'))

@supervisor.route('/inventory')
@supervisor_required
def manage_inventory():
    try:
        # Get all inventory items
        inventory = Inventory.get_all()
        
        # Get low stock items
        low_stock = Inventory.get_low_stock()
        
        return render_template('supervisor/inventory.html',
                             inventory=inventory,
                             low_stock=low_stock)
    except Exception as e:
        flash(f'Error loading inventory: {str(e)}', 'error')
        return redirect(url_for('supervisor.supervisor_dashboard')) 