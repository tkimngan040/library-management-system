from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Book, User, Category, BorrowRecord
from services.admin_service import (
    get_dashboard_statistics,
    get_all_books,
    get_book_by_id,
    create_book,
    update_book,
    delete_book,
    get_all_members,
    get_member_by_id,
    create_member,
    update_member,
    lock_member,
    unlock_member,
    delete_member,
    get_all_borrow_records,
    get_overdue_records,
    mark_as_returned
)

# Tạo blueprint cho admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorator để kiểm tra admin (tạm thời - sẽ dùng từ auth_service sau)
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'Admin':
            flash('Access denied - Admin only', 'error')
            return redirect(url_for('books.book_list'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================
# ADMIN DASHBOARD
# ============================================
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Hiển thị trang dashboard với thống kê tổng quan"""
    stats = get_dashboard_statistics()
    return render_template('admin/dashboard.html', stats=stats)


# ============================================
# MANAGE BOOKS
# ============================================
@admin_bp.route('/books')
@admin_required
def books_list():
    """Hiển thị danh sách tất cả sách"""
    books = get_all_books()
    return render_template('admin/books_list.html', books=books)


@admin_bp.route('/books/add', methods=['GET', 'POST'])
@admin_required
def books_add():
    """Form thêm sách mới"""
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        category_id = request.form.get('category_id')
        description = request.form.get('description')
        detailed_info = request.form.get('detailed_info')
        
        # Validate
        if not all([title, author, category_id]):
            flash('Title, Author and Category are required', 'error')
            categories = Category.query.all()
            return render_template('admin/book_form.html', 
                                   categories=categories, 
                                   mode='add')
        
        # Tạo sách mới
        success = create_book(title, author, category_id, description, detailed_info)
        if success:
            flash('Book added successfully', 'success')
            return redirect(url_for('admin.books_list'))
        else:
            flash('Failed to add book', 'error')
    
    # GET request - hiển thị form
    categories = Category.query.all()
    return render_template('admin/book_form.html', 
                           categories=categories, 
                           mode='add')


@admin_bp.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def books_edit(book_id):
    """Form sửa thông tin sách"""
    book = get_book_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('admin.books_list'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        category_id = request.form.get('category_id')
        description = request.form.get('description')
        detailed_info = request.form.get('detailed_info')
        
        # Validate
        if not all([title, author, category_id]):
            flash('Title, Author and Category are required', 'error')
            categories = Category.query.all()
            return render_template('admin/book_form.html', 
                                   book=book,
                                   categories=categories, 
                                   mode='edit')
        
        # Update sách
        success = update_book(book_id, title, author, category_id, description, detailed_info)
        if success:
            flash('Book updated successfully', 'success')
            return redirect(url_for('admin.books_list'))
        else:
            flash('Failed to update book', 'error')
    
    # GET request - hiển thị form với data cũ
    categories = Category.query.all()
    return render_template('admin/book_form.html', 
                           book=book,
                           categories=categories, 
                           mode='edit')


@admin_bp.route('/books/delete/<int:book_id>', methods=['POST'])
@admin_required
def books_delete(book_id):
    """Xóa sách"""
    success, message = delete_book(book_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('admin.books_list'))


# ============================================
# MANAGE MEMBERS
# ============================================
@admin_bp.route('/members')
@admin_required
def members_list():
    """Hiển thị danh sách tất cả members"""
    members = get_all_members()
    return render_template('admin/members_list.html', members=members)


@admin_bp.route('/members/add', methods=['GET', 'POST'])
@admin_required
def members_add():
    """Form thêm member mới"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Validate
        if not all([username, password, full_name]):
            flash('Username, Password and Full Name are required', 'error')
            return render_template('admin/member_form.html', mode='add')
        
        # Tạo member mới
        success, message = create_member(username, password, full_name, email, phone)
        if success:
            flash(message, 'success')
            return redirect(url_for('admin.members_list'))
        else:
            flash(message, 'error')
    
    # GET request - hiển thị form
    return render_template('admin/member_form.html', mode='add')


@admin_bp.route('/members/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def members_edit(user_id):
    """Form sửa thông tin member"""
    member = get_member_by_id(user_id)
    if not member:
        flash('Member not found', 'error')
        return redirect(url_for('admin.members_list'))
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Validate
        if not full_name:
            flash('Full Name is required', 'error')
            return render_template('admin/member_form.html', 
                                   member=member,
                                   mode='edit')
        
        # Update member
        success = update_member(user_id, full_name, email, phone)
        if success:
            flash('Member updated successfully', 'success')
            return redirect(url_for('admin.members_list'))
        else:
            flash('Failed to update member', 'error')
    
    # GET request - hiển thị form với data cũ
    return render_template('admin/member_form.html', 
                           member=member,
                           mode='edit')


@admin_bp.route('/members/lock/<int:user_id>', methods=['POST'])
@admin_required
def members_lock(user_id):
    """Khóa tài khoản member"""
    success = lock_member(user_id)
    if success:
        flash('Member account locked', 'success')
    else:
        flash('Failed to lock member account', 'error')
    return redirect(url_for('admin.members_list'))


@admin_bp.route('/members/unlock/<int:user_id>', methods=['POST'])
@admin_required
def members_unlock(user_id):
    """Mở khóa tài khoản member"""
    success = unlock_member(user_id)
    if success:
        flash('Member account unlocked', 'success')
    else:
        flash('Failed to unlock member account', 'error')
    return redirect(url_for('admin.members_list'))


@admin_bp.route('/members/delete/<int:user_id>', methods=['POST'])
@admin_required
def members_delete(user_id):
    """Xóa member"""
    success, message = delete_member(user_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('admin.members_list'))


# ============================================
# MANAGE BORROW RECORDS
# ============================================
@admin_bp.route('/borrows')
@admin_required
def borrows_list():
    """Hiển thị danh sách tất cả borrow records"""
    # Lấy filter params từ URL
    status = request.args.get('status')
    member_id = request.args.get('member_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Lấy records
    records = get_all_borrow_records(status, member_id, date_from, date_to)
    
    # Lấy danh sách members cho filter dropdown
    members = get_all_members()
    
    return render_template('admin/borrows_list.html', 
                           records=records,
                           members=members,
                           current_status=status,
                           current_member_id=member_id)


@admin_bp.route('/borrows/overdue')
@admin_required
def borrows_overdue():
    """Hiển thị danh sách sách quá hạn"""
    records = get_overdue_records()
    return render_template('admin/borrows_list.html', 
                           records=records,
                           show_overdue_only=True)


@admin_bp.route('/borrows/mark-returned/<int:borrow_id>', methods=['POST'])
@admin_required
def borrows_mark_returned(borrow_id):
    """Admin đánh dấu sách đã được trả"""
    success, message = mark_as_returned(borrow_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('admin.borrows_list'))
