from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify, send_file
from models.database import WorkOrder, User
from datetime import datetime, timedelta
from functools import wraps
import pdfkit
import os

client = Blueprint('client', __name__, url_prefix='/client')

def client_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user') or session['user']['role'] != 'client':
            flash('Access denied', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@client.route('/dashboard')
@client_required
def dashboard():
    # Get client's orders
    orders = WorkOrder.get_by_client(session['user']['id'])
    
    # Calculate estimated dispatch dates
    for order in orders:
        if order['status'] != 'completed':
            # Add 2 business days to completion for dispatch
            estimated_completion = datetime.fromisoformat(order['start_time']) + timedelta(days=2)
            order['estimated_dispatch'] = estimated_completion.strftime('%Y-%m-%d')
        else:
            order['estimated_dispatch'] = 'Completed'
    
    return render_template('client/dashboard.html', orders=orders)

@client.route('/orders')
@client_required
def orders():
    orders = WorkOrder.get_by_client(session['user']['id'])
    return render_template('client/orders.html', orders=orders)

@client.route('/orders/<int:order_id>')
@client_required
def order_details(order_id):
    order = WorkOrder.get_by_id(order_id)
    if not order or order['client_id'] != session['user']['id']:
        flash('Order not found', 'error')
        return redirect(url_for('client.orders'))
    return render_template('client/order_details.html', order=order)

@client.route('/orders/<int:order_id>/invoice')
@client_required
def download_invoice(order_id):
    order = WorkOrder.get_by_id(order_id)
    if not order or order['client_id'] != session['user']['id']:
        flash('Order not found', 'error')
        return redirect(url_for('client.orders'))
    
    # Generate invoice HTML
    invoice_html = render_template('client/invoice.html', order=order)
    
    # Convert to PDF
    pdf = pdfkit.from_string(invoice_html, False)
    
    # Save temporarily
    temp_path = f'temp/invoice_{order_id}.pdf'
    os.makedirs('temp', exist_ok=True)
    with open(temp_path, 'wb') as f:
        f.write(pdf)
    
    return send_file(temp_path, 
                    as_attachment=True,
                    download_name=f'invoice_{order["order_number"]}.pdf')

@client.route('/orders/<int:order_id>/delivery-note')
@client_required
def download_delivery_note(order_id):
    order = WorkOrder.get_by_id(order_id)
    if not order or order['client_id'] != session['user']['id']:
        flash('Order not found', 'error')
        return redirect(url_for('client.orders'))
    
    # Generate delivery note HTML
    delivery_note_html = render_template('client/delivery_note.html', order=order)
    
    # Convert to PDF
    pdf = pdfkit.from_string(delivery_note_html, False)
    
    # Save temporarily
    temp_path = f'temp/delivery_note_{order_id}.pdf'
    os.makedirs('temp', exist_ok=True)
    with open(temp_path, 'wb') as f:
        f.write(pdf)
    
    return send_file(temp_path, 
                    as_attachment=True,
                    download_name=f'delivery_note_{order["order_number"]}.pdf')

@client.route('/support', methods=['GET', 'POST'])
@client_required
def support():
    if request.method == 'POST':
        message = request.form.get('message')
        subject = request.form.get('subject')
        
        # TODO: Implement message sending to support
        flash('Message sent to support', 'success')
        return redirect(url_for('client.support'))
    
    return render_template('client/support.html')

@client.route('/services')
def my_services():
    if not session.get('user') or session['user']['role'] != 'client':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('client/services.html')

@client.route('/profile')
def profile():
    if not session.get('user') or session['user']['role'] != 'client':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('client/profile.html') 