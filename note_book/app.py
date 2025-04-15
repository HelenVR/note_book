import os
from flask import Flask, render_template, request, make_response, send_file
import csv
import re

from .db import DbWorker
from .configs.config import load_config
from .exceptions import DuplicateContactError, ContactNotFoundError

app = Flask(__name__)
app.db_config = load_config()
app.db_worker = DbWorker(app.db_config)


@app.before_request
def setup():
    app.db_worker.init_db()


@app.route('/')
def menu():
    return render_template('menu.html')


@app.route('/contacts')
def show_contacts():
    contacts = app.db_worker.get_all_contacts()
    return render_template('contacts.html', contacts=contacts)


@app.route('/create_contact', methods=['GET', 'POST'])
def create_contact_view():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        try:
            app.db_worker.find_contact(name, surname, exists=False)
        except DuplicateContactError:
            error_message = f'Контакт {name} {surname} уже есть в телефонной книге.'
            response = make_response(render_template('create_contact.html', error_message=error_message), 422)
            return response
        phone_number = request.form['phone_number']
        phone_pattern = r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$'
        if not re.match(phone_pattern, phone_number):
            error_message = 'Неправильный формат номера телефона.'
            response = make_response(render_template('create_contact.html', error_message=error_message), 422)
            return response
        comment = request.form['comment']
        app.db_worker.create_contact(name, surname, phone_number, comment)
        message = f'Контакт {name} {surname} успешно добавлен.'
        return render_template('create_contact.html', message=message)
    return render_template('create_contact.html')


@app.route('/find_contact', methods=['GET', 'POST'])
def find_contact_view():
    contact = None
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        try:
            contact = app.db_worker.find_contact(name, surname)
        except ContactNotFoundError:
            error_message = f'Контакт {name} {surname} не найден'
            response = make_response(render_template('find_contact.html', contact=contact, error_message=error_message),
                                     400)
            return response
    return render_template('find_contact.html', contact=contact)


@app.route('/update_contact', methods=['GET', 'POST'])
def update_contact_view():
    contact = None

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        try:
            contact = app.db_worker.find_contact(name, surname)
        except ContactNotFoundError:
            error_message = f'Контакт {name} {surname} не найден'
            response = make_response(render_template('update_contact.html', contact=contact, error_message=error_message),
                                     400)
            return response
        contact_id = contact[0]
        if request.form.get('phone_number'):
            phone_number = request.form['phone_number']
            phone_pattern = r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$'
            if not re.match(phone_pattern, phone_number):
                error_message = 'Неправильный формат номера телефона.'
                response = make_response(render_template('update_contact.html', contact=contact, error_message=error_message), 422)
                return response

        phone_number = phone_number if request.form.get('phone_number') else contact[3]
        comment = request.form.get('comment') if request.form.get('comment') else contact[-1]

        app.db_worker.update_contact(contact_id, name, surname, phone_number, comment)
        message = f'Контакт {name} {surname} обновлён'
        contact = app.db_worker.find_contact(name, surname)
        return render_template('update_contact.html', contact=contact, message=message)

    return render_template('update_contact.html', contact=contact)


@app.route('/delete_contact', methods=['GET', 'POST'])
def delete_contact_view():
    contact = None
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        try:
            contact = app.db_worker.find_contact(name, surname)
        except ContactNotFoundError:
            error_message = f'Контакт {name} {surname} не найден'
            response = make_response(render_template('delete_contact.html', contact=contact, error_message=error_message), 400)
            return response
        app.db_worker.delete_contact(contact[1], contact[2])
        message = f'Контакт {name} {surname} удалён'
        return render_template('delete_contact.html', contact=contact, message=message)
    return render_template('delete_contact.html', contact=contact)


@app.route('/download')
def download():
    contacts = app.db_worker.get_all_contacts()
    if not contacts:
        return render_template('contacts.html', error_message="Список контактов пуст")
    csv_file = 'contacts.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Имя', 'Фамилия', 'Номер телефона', 'Комментарий'])
        for contact in contacts:
            writer.writerow([contact[1], contact[2], contact[3], contact[-1]])

    return send_file(csv_file, as_attachment=True)


@app.route('/shutdown')
def shutdown():
    app.db_worker.close_connection()
    return "Database connection closed."


if __name__ == '__main__':
    app.run(host=os.getenv("APP_HOST", "0.0.0.0"), port=int(os.getenv("APP_PORT", "7001")), debug=True)