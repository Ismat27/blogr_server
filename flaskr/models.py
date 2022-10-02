from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base
from flask_migrate import Migrate
from decouple import config


database_user = config('DB_USER')
database_user_password = config('DB_PASSWORD')
database_name = config('DB_NAME')
database_host = config('DB_HOST')
database_port = config('DB_PORT')
database_path = "postgresql://{}:{}@{}:{}/{}".format(
    database_user, database_user_password, database_host, database_port, database_name
)
db = SQLAlchemy()
migrate = Migrate()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)


"""Post model"""

class Post(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='posts')
    title = Column(String)
    content = Column(Text)
    is_published = Column(Boolean, server_default='f')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, public_id, title, content, author, author_id):
        self.public_id =public_id
        self.title = title
        self.content = content
        self.author = author
        self.author_id = author_id
    
    def __repr__(self):
        return f'<Blog id: {self.id} author: {self.author}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        if self.updated_at:
            last_updated = self.updated_at
        else:
            last_updated = self.created_at
        if self.author:
            author = self.author.fullname()
        else: author=''
        return {
            'id': self.public_id,
            'author': author,
            'title': self.title,
            'content': self.content,
            'date_created': self.created_at,
            'last_updated': last_updated,
        }

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    first_name = Column(String(200))
    last_name = Column(String(200))
    email = Column(String(200))
    password = Column(Text)
    posts = relationship('Post', back_populates='author')
    is_admin = Column(Boolean, server_default='t')
    is_superuser = Column(Boolean, server_default='f')
    signup_date = Column(DateTime, server_default=func.now())
    last_seen = Column(DateTime, server_default=func.now())

    def __init__(self, is_admin=True, is_superuser=False, **kwargs):
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.public_id = kwargs['public_id']
        self.email = kwargs['email']
        self.password = kwargs['password']
        self.first_name = kwargs['first_name']
        self.is_admin = is_admin
        self.is_superuser = is_superuser

    def __repr__(self):
        return f'<User id: {self.id} name: {self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.public_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_superuser': self.is_superuser
        }




