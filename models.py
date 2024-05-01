from mongoengine import Document, StringField, ReferenceField


class Category(Document):
    name = StringField()


class Book(Document):
    title = StringField()
    category = ReferenceField(Category)
    