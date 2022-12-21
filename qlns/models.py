from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from qlns import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


prod_tag = db.Table('prod_tag',
                    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
                    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))


class Product(BaseModel):
    name = Column(String(100), nullable=False)
    author = Column(String(100))
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
                        backref=backref('products', lazy=True))
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    image = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u = User(name='Taio', username='admin', password=password,
                 user_role=UserRole.ADMIN,
                 image='https://res.cloudinary.com/dkfnlesea/image/upload/v1671509611/adminnn_sbxqg3.jpg')
        db.session.add(u)
        db.session.commit()

        c1 = Category(name='Sách Bán Chạy')
        c2 = Category(name='Khoa Học/Học Thuật')
        c3 = Category(name='Tiểu Thuyết/Truyện')
        c4 = Category(name='Kỹ Năng Sống')

        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()

        p1 = Product(name="Đắc Nhân Tâm", author="Dale Carnegie", price=90000,
                     image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671507163/Dac-nhan-tam_epv70i.jpg",
                     category_id=1)
        p2 = Product(name="Atomic Habits - Thay Đổi Tí Hon, Hiệu Quả Bất Ngờ", author="James Clear", price=110000,
                     image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671507321/8932000131182_lqitam.jpg",
                     category_id=1)
        p3 = Product(name="21 Bài Học Cho Thế Kỷ 21", author="Yuval Noah Harari", price=120000,
                     image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671509309/21baihoc_x8cegj.jpg",
                     category_id=1)
        p4 = Product(name="Cẩm Nang Scrum Cho Người Mới Bắt Đầu", author="Học Viện Agile", price=89000,
                     image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671507475/camnangscrum_mg5ly1.jpg",
                     category_id=2)
        p5 = Product(name="Súng, Vi trùng và Thép", author="Jared Diamond", price=79000,
                     image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671509314/sungvitrungthep_uscelx.jpg",
                     category_id=2)
        p6 = Product(name="Lược sử thời gian", author="Stephen Hawking", price=130000,
                     image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671509448/luocsuthoigian_s4n1ah.jpg",
                     category_id=2)
        p7 = Product(name="Cây Cam Ngọt Của Tôi", author="José Mauro de Vasconcelos", price=99000,
                     image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671507810/caycamngot_of4lsr.jpg",
                     category_id=3)
        p8 = Product(name="Hai Số Phận", author="Jeffrey Archer", price=109000,
                     image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671507813/Hai-So-Phan_oebfap.jpg",
                     category_id=3)
        p9 = Product(name="Rừng Na Uy", author="Haruki Murakami", price=145000,
                     image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671507951/rungnauy_t57s68.jpg",
                     category_id=3)
        p10 = Product(name="Điểm Đến Của Cuộc Đời", author="Đặng Hoàng Giang", price=75000,
                      image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671507956/diemdencuocdoi_fuvyky.jpg",
                      category_id=4)
        p11 = Product(name="Đánh Thức Con Người Phi Thường Trong Bạn", author="Anthony Robbins", price=85000,
                      image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671509450/danhthucconng_rdfiv6.jpg",
                      category_id=4)
        p12 = Product(name="Giới Hạn Của Bạn Chỉ Là Xuất Phát Điểm Của Tôi", author="Mèo Maverick", price=95000,
                      image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671509453/gioihancuaban_zgdwi7.jpg",
                      category_id=4)
        p13 = Product(name="Nguyên lý 80/20", author="Richard Koch", price=65000,
                      image="https://res.cloudinary.com/dkfnlesea/image/upload/v1671508271/nguyen-ly-2080_w3ck5d.jpg",
                      category_id=4)

        db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13])
        db.session.commit()

        c1 = Comment(content='Cuốn sách tuyệt vời!', product_id=1, user_id=1)
        c2 = Comment(content='Hay cực.', product_id=1, user_id=1)
        db.session.add_all([c1, c2])
        db.session.commit()
