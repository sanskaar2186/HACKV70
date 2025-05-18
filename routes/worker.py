from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from models.database import (
    WorkOrder, Machine, WorkerShift, WorkerProductivity,
    Shift, Task, TaskComment
)
from datetime import datetime, timedelta
from functools import wraps
import uuid

worker = Blueprint('worker', __name__, url_prefix='/worker')

def worker_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user') or session['user']['role'] != 'worker':
            flash('Access denied', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@worker.route('/dashboard')
@worker_required
def dashboard():
    try:
        worker_id = session['user']['id']
        
        # Get worker's active tasks
        active_tasks = Task.get_by_worker(worker_id)
        active_tasks = [task for task in active_tasks if task['status'] != 'completed']
        
        # Get worker's current shift
        current_shift = Shift.get_current_shift(worker_id)
        
        # Get worker's assigned machines
        assigned_machines = Machine.get_by_worker(worker_id)
        
        return render_template('worker/dashboard.html',
                             active_tasks=active_tasks,
                             current_shift=current_shift,
                             assigned_machines=assigned_machines)
    except (ValueError, KeyError) as e:
        flash('Error loading dashboard: Invalid worker ID', 'error')
        return redirect(url_for('auth.login'))

@worker.route('/start-shift', methods=['POST'])
@worker_required
def start_shift():
    try:
        worker_id = session['user']['id']
        current_shift = Shift.get_current_shift(worker_id)
        
        if not current_shift:
            return jsonify({'success': False, 'error': 'No shift scheduled'})
        
        if current_shift['status'] != 'scheduled':
            return jsonify({'success': False, 'error': 'Shift already started or completed'})
        
        Shift.update_status(current_shift['id'], 'in_progress')
        return jsonify({'success': True})
    except (ValueError, KeyError) as e:
        return jsonify({'success': False, 'error': 'Invalid worker ID'})

@worker.route('/end-shift', methods=['POST'])
@worker_required
def end_shift():
    try:
        worker_id = session['user']['id']
        current_shift = Shift.get_current_shift(worker_id)
        
        if not current_shift:
            return jsonify({'success': False, 'error': 'No active shift found'})
        
        if current_shift['status'] != 'in_progress':
            return jsonify({'success': False, 'error': 'Shift not in progress'})
        
        Shift.update_status(current_shift['id'], 'completed')
        return jsonify({'success': True})
    except (ValueError, KeyError) as e:
        return jsonify({'success': False, 'error': 'Invalid worker ID'})

@worker.route('/update-task-progress', methods=['POST'])
@worker_required
def update_task_progress():
    try:
        worker_id = session['user']['id']
        task_id = request.form.get('task_id')
        output_count = request.form.get('output_count')
        notes = request.form.get('notes')
        
        task = WorkOrder.get_by_id(task_id)
        if not task or task['assigned_worker_id'] != worker_id:
            flash('Task not found', 'error')
            return redirect(url_for('worker.dashboard'))
        
        # Update task progress
        WorkOrder.update(task_id, {
            'output_count': int(output_count),
            'notes': notes
        })
        
        # Create productivity record
        WorkerProductivity.create({
            'worker_id': worker_id,
            'task_id': task_id,
            'output_count': int(output_count),
            'notes': notes,
            'created_at': datetime.now().isoformat()
        })
        
        flash('Task progress updated', 'success')
        return redirect(url_for('worker.dashboard'))
    except (ValueError, KeyError) as e:
        flash('Error updating task: Invalid worker ID', 'error')
        return redirect(url_for('worker.dashboard'))

@worker.route('/tasks')
@worker_required
def tasks():
    try:
        worker_id = session['user']['id']
        tasks = Task.get_by_worker(worker_id)
        return render_template('worker/tasks.html', tasks=tasks)
    except (ValueError, KeyError) as e:
        flash('Error loading tasks: Invalid worker ID', 'error')
        return redirect(url_for('auth.login'))

@worker.route('/tasks/<task_id>')
@worker_required
def task_details(task_id):
    try:
        worker_id = session['user']['id']
        task = Task.get_by_id(task_id)
        if not task or task['assigned_worker_id'] != worker_id:
            flash('Task not found', 'error')
            return redirect(url_for('worker.tasks'))
        
        comments = TaskComment.get_by_task(task_id)
        return render_template('worker/task_details.html', task=task, comments=comments)
    except (ValueError, KeyError) as e:
        flash('Error loading task details: Invalid worker ID', 'error')
        return redirect(url_for('worker.tasks'))

@worker.route('/tasks/<task_id>/update-status', methods=['POST'])
@worker_required
def update_task_status(task_id):
    try:
        worker_id = session['user']['id']
        data = request.get_json()
        task = Task.get_by_id(task_id)
        
        if not task or task['assigned_worker_id'] != worker_id:
            return jsonify({'success': False, 'error': 'Task not found'})
        
        Task.update_status(task_id, data['status'])
        return jsonify({'success': True})
    except (ValueError, KeyError) as e:
        return jsonify({'success': False, 'error': 'Invalid worker ID'})

@worker.route('/tasks/<task_id>/add-comment', methods=['POST'])
@worker_required
def add_task_comment(task_id):
    try:
        worker_id = session['user']['id']
        comment_text = request.form.get('comment')
        
        task = Task.get_by_id(task_id)
        if not task or task['assigned_worker_id'] != worker_id:
            flash('Task not found', 'error')
            return redirect(url_for('worker.tasks'))
        
        TaskComment.create({
            'task_id': task_id,
            'user_id': worker_id,
            'comment': comment_text
        })
        
        flash('Comment added successfully', 'success')
        return redirect(url_for('worker.task_details', task_id=task_id))
    except (ValueError, KeyError) as e:
        flash('Error adding comment: Invalid worker ID', 'error')
        return redirect(url_for('worker.tasks'))

@worker.route('/machines')
@worker_required
def machines():
    try:
        worker_id = session['user']['id']
        machines = Machine.get_by_worker(worker_id)
        return render_template('worker/machines.html', machines=machines)
    except (ValueError, KeyError) as e:
        flash('Error loading machines: Invalid worker ID', 'error')
        return redirect(url_for('auth.login'))

@worker.route('/machines/<machine_id>')
@worker_required
def machine_details(machine_id):
    try:
        worker_id = session['user']['id']
        machine = Machine.get_by_id(machine_id)
        if not machine:
            flash('Machine not found', 'error')
            return redirect(url_for('worker.machines'))
        return render_template('worker/machine_details.html', machine=machine)
    except (ValueError, KeyError) as e:
        flash('Error loading machine details: Invalid worker ID', 'error')
        return redirect(url_for('worker.machines'))

@worker.route('/shifts')
@worker_required
def shifts():
    try:
        worker_id = session['user']['id']
        shifts = Shift.get_by_worker(worker_id)
        current_shift = Shift.get_current_shift(worker_id)
        return render_template('worker/shifts.html', shifts=shifts, current_shift=current_shift)
    except (ValueError, KeyError) as e:
        flash('Error loading shifts: Invalid worker ID', 'error')
        return redirect(url_for('auth.login'))

@worker.route('/reports')
@worker_required
def reports():
    try:
        worker_id = session['user']['id']
        # Get worker's productivity reports for the last 30 days
        productivity = WorkerProductivity.get_worker_stats(
            worker_id=worker_id,
            start_date=(datetime.now() - timedelta(days=30)).isoformat(),
            end_date=datetime.now().isoformat()
        )
        return render_template('worker/reports.html', productivity=productivity)
    except (ValueError, KeyError) as e:
        flash('Error loading reports: Invalid worker ID', 'error')
        return redirect(url_for('auth.login')) 

