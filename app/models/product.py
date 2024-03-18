from app.extensions import db
from flask_authorize import PermissionsMixin
class Product(db.Model,PermissionsMixin):
    __permissions__ = dict(
        admin=['read', 'update', 'delete', 'revoke'],
        staff=['read', 'update']
    )

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    BarCode = db.Column(db.BigInteger,nullable=False)
    Name = db.Column(db.String, nullable=False)
    Safety_quantity = db.Column(db.Integer,nullable=False)
    Status = db.Column(db.String, nullable=False) # "NotAvailable","OutOfStock","InStock"

    