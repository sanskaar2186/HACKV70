from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify, send_file
from models.database import (
    ProductionLine, WorkOrder, Inventory, Machine,
    WorkerShift, WorkerProductivity, KPIMetrics, Report
)
from datetime import datetime, timedelta
from functools import wraps

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user') or session['user']['role'] != 'admin':
            flash('Access denied', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@admin_required
def admin_dashboard():
    # Get all data
    work_orders = WorkOrder.get_all()
    machines = Machine.get_all()
    inventory = Inventory.get_all()
    low_stock = Inventory.get_low_stock()
    reports = Report.get_reports()
    
    # Calculate total revenue (assuming ₹1000 per completed order)
    total_revenue = sum(1000 for order in work_orders if order.get('status') == 'completed')
    
    # Calculate other metrics
    total_orders = len(work_orders)
    completed_orders = len([order for order in work_orders if order.get('status') == 'completed'])
    pending_orders = len([order for order in work_orders if order.get('status') == 'pending'])
    active_machines = len([machine for machine in machines if machine.get('status') == 'operational'])
    
    return render_template('admin/dashboard.html',
                         work_orders=work_orders,
                         machines=machines,
                         inventory=inventory,
                         low_stock=low_stock,
                         reports=reports,
                         total_revenue=total_revenue,
                         total_orders=total_orders,
                         completed_orders=completed_orders,
                         pending_orders=pending_orders,
                         active_machines=active_machines)

@admin.route('/work-orders')
@admin_required
def work_orders():
    work_orders = WorkOrder.get_all()
    return render_template('admin/work_orders.html', work_orders=work_orders)

@admin.route('/work-orders/create', methods=['GET', 'POST'])
@admin_required
def create_work_order():
    if request.method == 'POST':
        data = request.form.to_dict()
        WorkOrder.create(data)
        return redirect(url_for('admin.work_orders'))
    return render_template('admin/work_orders/create.html')

@admin.route('/work-orders/<int:order_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_work_order(order_id):
    order = WorkOrder.get_by_id(order_id)
    if request.method == 'POST':
        data = request.form.to_dict()
        WorkOrder.update(order_id, data)
        return redirect(url_for('admin.work_orders'))
    return render_template('admin/work_orders/edit.html', order=order)

@admin.route('/work-orders/<int:order_id>/delete', methods=['POST'])
@admin_required
def delete_work_order(order_id):
    WorkOrder.delete(order_id)
    return jsonify({'success': True})

@admin.route('/machines')
@admin_required
def machines():
    machines = Machine.get_all()
    return render_template('admin/machines.html', machines=machines)

@admin.route('/machines/create', methods=['GET', 'POST'])
@admin_required
def create_machine():
    if request.method == 'POST':
        data = request.form.to_dict()
        Machine.create(data)
        return redirect(url_for('admin.machines'))
    return render_template('admin/machines/create.html')

@admin.route('/machines/<int:machine_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_machine(machine_id):
    machine = Machine.get_by_id(machine_id)
    if request.method == 'POST':
        data = request.form.to_dict()
        Machine.update(machine_id, data)
        return redirect(url_for('admin.machines'))
    return render_template('admin/machines/edit.html', machine=machine)

@admin.route('/machines/<int:machine_id>/delete', methods=['POST'])
@admin_required
def delete_machine(machine_id):
    Machine.delete(machine_id)
    return jsonify({'success': True})

@admin.route('/machines/<int:machine_id>/maintenance', methods=['POST'])
@admin_required
def schedule_maintenance(machine_id):
    data = request.get_json()
    Machine.schedule_maintenance(machine_id, data['date'])
    return jsonify({'success': True})

@admin.route('/inventory')
@admin_required
def inventory():
    inventory = Inventory.get_all()
    low_stock = Inventory.get_low_stock()
    return render_template('admin/inventory.html', inventory=inventory, low_stock=low_stock)

@admin.route('/inventory/create', methods=['GET', 'POST'])
@admin_required
def create_inventory_item():
    if request.method == 'POST':
        data = request.form.to_dict()
        Inventory.create(data)
        return redirect(url_for('admin.inventory'))
    return render_template('admin/inventory/create.html')

@admin.route('/inventory/<int:item_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_inventory_item(item_id):
    item = Inventory.get_by_id(item_id)
    if request.method == 'POST':
        data = request.form.to_dict()
        Inventory.update(item_id, data)
        return redirect(url_for('admin.inventory'))
    return render_template('admin/inventory/edit.html', item=item)

@admin.route('/inventory/<int:item_id>/delete', methods=['POST'])
@admin_required
def delete_inventory_item(item_id):
    Inventory.delete(item_id)
    return jsonify({'success': True})

@admin.route('/inventory/<int:item_id>/update-stock', methods=['POST'])
@admin_required
def update_inventory_stock(item_id):
    data = request.get_json()
    Inventory.update_quantity(item_id, data['quantity'])
    return jsonify({'success': True})

@admin.route('/reports')
@admin_required
def reports():
    reports = Report.get_reports()
    return render_template('admin/reports.html', reports=reports)

@admin.route('/reports/generate', methods=['POST'])
@admin_required
def generate_report():
    data = request.get_json()
    report_data = {
        'type': data['type'],
        'generated_by': session.get('user_id'),
        'created_at': datetime.now().isoformat(),
        'status': 'completed'
    }
    Report.save_report(report_data)
    return jsonify({'success': True})

@admin.route('/reports/<int:report_id>/view')
@admin_required
def view_report(report_id):
    report = Report.get_by_id(report_id)
    return render_template('admin/reports/view.html', report=report)

@admin.route('/reports/<int:report_id>/download')
@admin_required
def download_report(report_id):
    report = Report.get_by_id(report_id)
    # Generate and return the report file
    return send_file(report.file_path, as_attachment=True)

@admin.route('/reports/<int:report_id>/delete', methods=['POST'])
@admin_required
def delete_report(report_id):
    Report.delete(report_id)
    return jsonify({'success': True})

# API endpoints for real-time updates
@admin.route('/api/production-status')
@admin_required
def production_status():
    lines = ProductionLine.get_all()
    orders = WorkOrder.get_all()
    return jsonify({
        'lines': lines,
        'orders': orders
    })

@admin.route('/api/inventory-status')
@admin_required
def inventory_status():
    items = Inventory.get_all()
    low_stock = Inventory.get_low_stock()
    return jsonify({
        'items': items,
        'low_stock': low_stock
    })

@admin.route('/api/machine-status')
@admin_required
def machine_status():
    machines = Machine.get_all()
    return jsonify({
        'machines': machines
    })

@admin.route('/api/worker-status')
@admin_required
def worker_status():
    shifts = WorkerShift.get_current_shifts()
    return jsonify({
        'shifts': shifts
    })