from io import BytesIO
import os
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import inspect
from app.extensions import admin_permission,db
from flask_principal import Permission,RoleNeed

from app.models.user import Role, User
# from flask_principal import Permission, RoleNeed
# Create a permission with a single Need, in this case a RoleNeed.
# admin_permission = Permission(RoleNeed('admin'))

bp = Blueprint('main', __name__)

admin_permission = Permission(RoleNeed('admin'))

@bp.route('/')
# @login_required
def index():
    return render_template('index.html')





@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@bp.route('/admin_page')
@login_required
@admin_permission.require(http_exception=401)
def admin_page():

    return "this is admin page"

@bp.route('/role_management',methods=["GET","POST"])
@login_required
@admin_permission.require(http_exception=401)
def role_management():
    
    users = User.query.all()
    if request.method =="POST":
        user_ids =request.form.getlist('user_id')
        admin_roles = request.form.getlist('admin_roles')
        staff_roles = request.form.getlist('staff_roles')
        print(user_ids)
        print(admin_roles)
        print(staff_roles)
        for id in user_ids:
            user = User.query.filter_by(id = int(id)).first()
            print('user: ',user.id)
            user_id = user.id
            user.roles.clear()
            if str(user_id) in admin_roles:
                role = Role.query.filter_by(id=1).first()
                user.roles.append(role)
                db.session.commit()

            if str(user_id) in staff_roles:
                role = Role.query.filter_by(id=2).first()
                user.roles.append(role)
                db.session.commit()
            
            

    return render_template('role_management.html',users = users)


from flask import send_file
from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode
# Sample monthly sales data (you can replace this with your actual sales data)

@bp.route('/generate_sales_pdf', methods=['GET'])
def generate_sales_pdf():
    # Instantiation of inherited class
    data = User.query.all()
    # Extract column names from the SQLAlchemy model
    columns = [column.key for column in inspect(User).c]
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("helvetica", size=16,style="B")
    pdf.cell(40, 10, "SALES REPORT",align='CENTER', center=True)
    pdf.ln()
    pdf.set_y(22)
    pdf.set_font("helvetica", size=8)
    pdf.cell(40, 10, "SALES PERSON")
    pdf.cell(40, 10, "DATE")
    pdf.set_y(27)
    pdf.cell(40, 10, "Zach Posey")
    pdf.cell(40, 10, "11/30/24")
    pdf.ln()

    pdf.set_xy(150,22)
    # pdf.set_y(10)
    pdf.cell(30, 10, "SALES AMOUNT")
    pdf.cell(10, 10, "RM 3750.00")
    pdf.ln()
    pdf.set_xy(150,27)
    pdf.cell(30, 10, "SALES TAX")
    pdf.cell(10, 10, "RM 227.00")
    pdf.line(150, 34.5,198,34.5)
    pdf.set_xy(150,34)
    pdf.cell(30, 8, "SALES TOTAL")
    pdf.cell(10, 8, "RM 4077.00")


    pdf.ln()
    pdf.cell(40, 10, "Payment Type")
    pdf.cell(40, 10, "Cash")

    pdf.ln()
    pdf.cell(40, 10, "ITEM DETAIL")
    pdf.ln()


    # Add table header
    pdf.set_fill_color(224, 235, 255)
    # for column_name in columns:
    #     pdf.cell(20, 10, column_name, border=1, fill=True)

    # Table Header
    pdf.cell(30, 7, 'BarCode', border=1, fill=True,align='CENTER')
    pdf.cell(50, 7, 'Nsme', border=1, fill=True,align='CENTER')
    pdf.cell(20, 7, 'Price', border=1, fill=True,align='CENTER')
    pdf.cell(20, 7, 'QTY', border=1, fill=True,align='CENTER')
    pdf.cell(20, 7, 'Amount', border=1, fill=True,align='CENTER')
    pdf.cell(20, 7, 'Tax', border=1, fill=True,align='CENTER')
    pdf.cell(23, 7, 'Total', border=1, fill=True,align='CENTER')
    pdf.ln()

    # Table data
    pdf.cell(30, 7, '120331234', border=1,align='CENTER')
    pdf.cell(50, 7, 'KitKat', border=1,)
    pdf.cell(20, 7, '2.00', border=1,align='CENTER')
    pdf.cell(20, 7, '3', border=1,align='CENTER')
    pdf.cell(20, 7, '6.00', border=1,align='CENTER')
    pdf.cell(20, 7, '00.00', border=1,align='CENTER')
    pdf.cell(23, 7, '06.00', border=1,align='CENTER')

    pdf.ln()
    pdf.ln()
    pdf.cell(80,10,'Note : This is an automatic generated document. No signature is required')
    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return send_file(pdf_bytes, as_attachment=False,download_name='sample1.pdf')

@bp.route('/generate_inventory_pdf', methods=['GET'])
def generate_inventory_pdf():
    # Instantiation of inherited class
    data = User.query.all()
    # Extract column names from the SQLAlchemy model
    columns = [column.key for column in inspect(User).c]
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("helvetica", size=16,style="B")
    pdf.cell(40, 10, "INVENTORY HISTORY REPORT",align='CENTER', center=True)
    pdf.ln()
    pdf.set_y(22)
    pdf.set_font("helvetica", size=8)
    pdf.cell(40, 10, "Product")
    pdf.cell(40, 10, "DATE")
    pdf.set_y(27)
    pdf.cell(40, 10, "KitKAT")
    pdf.cell(40, 10, "1/1/2024 - 31/12/2024")
    pdf.ln()

    pdf.set_xy(150,22)
    # pdf.set_y(10)
    pdf.cell(30, 10, "COST AMOUNT")
    pdf.cell(10, 10, "RM 3750.00")
    pdf.ln()
    pdf.set_xy(150,27)
    pdf.cell(30, 10, "TAX")
    pdf.cell(10, 10, "RM 227.00")
    pdf.line(150, 34.5,198,34.5)
    pdf.set_xy(150,34)
    pdf.cell(30, 8, "COST TOTAL")
    pdf.cell(10, 8, "RM 4077.00")


    pdf.ln()
    pdf.cell(40, 10, "Supplier")
    pdf.cell(40, 10, "KK Company STD BHD")
    pdf.set_y(46)
    pdf.cell(40, 10, "Categories")
    pdf.cell(40, 10, "Snack Chocolate")

    pdf.ln()
    pdf.cell(40, 10, "INVENTORY DETAIL")
    pdf.ln()


    # Add table header
    pdf.set_fill_color(224, 235, 255)
    # for column_name in columns:
    #     pdf.cell(20, 10, column_name, border=1, fill=True)

    # Table Header
    pdf.cell(20, 7, 'No', border=1, fill=True,align='CENTER')
    # pdf.cell(50, 7, 'StockI', border=1, fill=True,align='CENTER')
    pdf.cell(40, 7, 'StockInDate', border=1, fill=True,align='CENTER')
    pdf.cell(40, 7, 'ExpiryDate', border=1, fill=True,align='CENTER')
    pdf.cell(20, 7, 'Init_QTY', border=1, fill=True,align='CENTER')
    pdf.cell(20, 7, 'CostPerItem', border=1, fill=True,align='CENTER')
    pdf.cell(20, 7, 'Retail Price', border=1, fill=True,align='CENTER')
    pdf.cell(27, 7, 'Cost Total', border=1, fill=True,align='CENTER')
    pdf.ln()

    # Table data
    for i in range(1,60):
        pdf.cell(20, 7, '1', border=1,align='CENTER')
        pdf.cell(40, 7, '2/1/2024', border=1,align='CENTER')
        pdf.cell(40, 7, '1/7/2024', border=1,align='CENTER')
        pdf.cell(20, 7, '50', border=1,align='CENTER')
        pdf.cell(20, 7, '1.50', border=1,align='CENTER')
        pdf.cell(20, 7, '2.00', border=1,align='CENTER')
        pdf.cell(27, 7, '75.00', border=1,align='CENTER')
        pdf.ln()

    pdf.ln()
    pdf.ln()
    pdf.cell(80,10,'Note : This is an automatic generated document. No signature is required')
    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return send_file(pdf_bytes, as_attachment=False,download_name='sample1.pdf')


@bp.route('/generate_cashflow_pdf', methods=['GET'])
def generate_cashflow_pdf():
    # Instantiation of inherited class
    data = User.query.all()
    # Extract column names from the SQLAlchemy model
    columns = [column.key for column in inspect(User).c]
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("helvetica", size=16,style="B")
    pdf.cell(40, 10, "S-MART Cash Flow  REPORT",align='CENTER', center=True)
    pdf.ln()
    pdf.set_y(22)
    pdf.set_font("helvetica", size=8)
    pdf.cell(40, 10, "DATE")
    pdf.set_y(27)
    pdf.cell(40, 10, "1/1/2024 - 12/1/2024")
    pdf.ln()

    pdf.ln()


    # Add table header
    pdf.set_fill_color(224, 235, 255)
    # for column_name in columns:
    #     pdf.cell(20, 10, column_name, border=1, fill=True)

    # Table Header
    pdf.cell(40, 7, 'Date', border=1, fill=True,align='CENTER')
    # pdf.cell(50, 7, 'StockI', border=1, fill=True,align='CENTER')
    pdf.cell(60, 7, 'Particulars', border=1, fill=True,align='CENTER')
    pdf.cell(30, 7, 'Debit', border=1, fill=True,align='CENTER')
    pdf.cell(30, 7, 'Credit', border=1, fill=True,align='CENTER')
    pdf.cell(20, 7, 'Balance', border=1, fill=True,align='CENTER')
    pdf.ln()

    # Table data

    pdf.cell(40, 7, '2/1/2024', border=1,align='CENTER')
    pdf.cell(60, 7, 'CashIn', border=1)
    pdf.cell(30, 7, '120.00', border=1,align='CENTER')
    pdf.cell(30, 7, '0', border=1,align='CENTER')
    pdf.cell(20, 7, '120.00', border=1,align='CENTER')
    pdf.ln()
    pdf.cell(40, 7, '4/1/2024', border=1,align='CENTER')
    pdf.cell(60, 7, 'Sales (Cash)', border=1)
    pdf.cell(30, 7, '6.00', border=1,align='CENTER')
    pdf.cell(30, 7, '0', border=1,align='CENTER')
    pdf.cell(20, 7, '126.00', border=1,align='CENTER')
    pdf.ln()
    pdf.cell(40, 7, '5/1/2024', border=1,align='CENTER')
    pdf.cell(60, 7, 'StockIn (Cash)', border=1)
    pdf.cell(30, 7, '0', border=1,align='CENTER')
    pdf.cell(30, 7, '206.00', border=1,align='CENTER')
    pdf.cell(20, 7, '-120.00', border=1,align='CENTER')
    pdf.ln()
    pdf.ln()
    pdf.set_fill_color(200,200,200)
    pdf.cell(160, 7, 'Total Amount', border=1,align='CENTER', fill=True)
    pdf.cell(20, 7, '-120.00', border=1,align='CENTER')
    pdf.ln()
    pdf.ln()
    pdf.cell(80,10,'Note : This is an automatic generated document. No signature is required')
    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return send_file(pdf_bytes, as_attachment=False,download_name='sample1.pdf')



















# def samplepdftable():
# #    # Add table rows for sales data
#     with pdf.table(text_align='CENTER',cell_fill_color=200, cell_fill_mode="ROWS") as table:
#         for data_row in data:
#             row = table.row()
#             for col in columns:
#                 value = getattr(data_row, col)
#                 pdf.cell(20,10,str(value), border=1)
#             pdf.ln()
    
#     pdf_bytes = BytesIO()
#     pdf.output(pdf_bytes)
#     pdf_bytes.seek(0)
#     return send_file(pdf_bytes, as_attachment=False,download_name='sample1.pdf')


# def samplepdf():
#     pdf = FPDF(orientation="P", unit="mm", format="A4")
#     pdf.add_page()
#     pdf.set_font("helvetica", "B", 16)
#     pdf.cell(40, 10, "Hello World!")
#      # Create directory if it doesn't exist
#     save_dir = os.path.join(os.getcwd(), 'generated_pdfs')
#     # os.makedirs(save_dir, exist_ok=True)
    
#     # # Save the PDF to a file
#     pdf_file_path = os.path.join(save_dir, "sample.pdf")
#     # pdf.output(pdf_file_path)
    
#     # Send the PDF file as a response
#     return send_file(pdf_file_path, as_attachment=False,download_name='sample.pdf')


