from . import technologies_bp
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_ckeditor import CKEditor
from models import db, Technologies
from .forms import TechnologiesForm
from helpers import *

@technologies_bp.route('/', methods=['GET', 'POST'])
def index():
    technologies = Technologies.query.all()
    return render_template('admin/technologies/index.html', technologies=technologies)


@technologies_bp.route('/add', methods=['GET', 'POST'])
def add():
    technologyForm = TechnologiesForm()
    if request.method == 'POST':
        image = request.files['image']
        file_size = request.content_length
        extension = get_file_extension(image.filename)
        allowed_ext = ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']
        
        if extension in allowed_ext and file_size < 1024*1024*5:
            img_name = random_filename_for_technology(image.filename)
            save_file(image, 'app/static/uploads', img_name)
        else:
            return redirect(url_for('admin.technologies.add'))
        
        technology = Technologies(
            title = technologyForm.title.data,
            image = img_name,
            content = technologyForm.content.data
        )
        db.session.add(technology)
        db.session.commit()
        return redirect(url_for('admin.technologies.index'))
    return render_template('admin/technologies/add.html', technologyForm=technologyForm)


@technologies_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    technology = Technologies.query.get(id)
    get_name_for_delete = technology.image
    if request.method == 'POST':
        image = request.files['image']
        new_name = random_filename_for_technology(image.filename)
        save_file(image, 'app/static/uploads', new_name)
        technology.title = request.form['title']
        technology.image = new_name
        technology.content = request.form['content']
        db.session.commit()
        delete_file_from_folder(get_name_for_delete, 'app/static/uploads')
        return redirect(url_for('admin.technologies.index'))
    return render_template('admin/technologies/update.html', technology=technology)

@technologies_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    technology = Technologies.query.get(id)
    file_name_for_delete= technology.image
    delete_file_from_folder(file_name_for_delete, 'app/static/uploads')
    db.session.delete(technology)
    db.session.commit()
    return redirect(url_for('admin.technologies.index'))