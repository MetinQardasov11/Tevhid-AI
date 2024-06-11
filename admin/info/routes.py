from . import info_bp
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_ckeditor import CKEditor
from models import db, Info
from .forms import InfoForm
from helpers import *

@info_bp.route('/', methods=['GET', 'POST'])
def index():
    infos = Info.query.all()
    return render_template('admin/info/index.html', infos=infos)


@info_bp.route('/add', methods=['GET', 'POST'])
def add():
    infoForm = InfoForm()
    if request.method == 'POST':
        image = request.files['image']
        file_size = request.content_length
        extension = get_file_extension(image.filename)
        allowed_ext = ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']
        
        if extension in allowed_ext and file_size < 1024*1024*5:
            img_name = random_filename_for_info(image.filename)
            save_file(image, 'app/static/uploads', img_name)
        else:
            return redirect(url_for('admin.info.add'))
        
        info = Info(
            content = infoForm.content.data,
            image = img_name,
        )
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('admin.info.index'))
    return render_template('admin/info/add.html', infoForm=infoForm)


@info_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    info = Info.query.get(id)
    get_name_for_delete = info.image
    if request.method == 'POST':
        image = request.files['image']
        new_name = random_filename_for_info(image.filename)
        save_file(image, 'app/static/uploads', new_name)
        info.image = new_name
        info.content = request.form['content']
        db.session.commit()
        delete_file_from_folder(get_name_for_delete, 'app/static/uploads')
        return redirect(url_for('admin.info.index'))
    return render_template('admin/info/update.html', info=info)

@info_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    info = Info.query.get(id)
    file_name_for_delete= info.image
    delete_file_from_folder(file_name_for_delete, 'app/static/uploads')
    db.session.delete(info)
    db.session.commit()
    return redirect(url_for('admin.info.index'))