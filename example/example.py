"""Продемонстрировать связь товаров и категорий в SQLAlchemy.

При выполнении или импорте модуль создаёт базу SQLite в памяти,
сохраняет демонстрационные записи и выводит их в консоль.
"""

from decimal import Decimal
from sqlalchemy import create_engine, String, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    """Базовый класс декларативных моделей демонстрационного примера."""

    pass


class Product(Base):
    """Товар с названием, ценой, признаком наличия и связанной категорией."""

    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped['Category'] = relationship(back_populates='products')

    def __str__(self) -> str:
        """Вернуть описание товара, его цены, наличия и идентификатора категории."""
        return (f'Product: name: {self.name}; price: {self.price};'
                f' availability: {self.in_stock}; category_id: {self.category_id}')
    def __repr__(self) -> str:
        """Вернуть диагностическое строковое представление товара."""
        return (f'Product: name: {self.name}; price: {self.price};'
                f' availability: {self.in_stock}; category_id: {self.category_id}')


class Category(Base):
    """Категория с названием, описанием и коллекцией товаров."""

    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    products: Mapped[list[Product]] = relationship(back_populates='category')

    def __str__(self) -> str:
        """Вернуть название и описание категории."""
        return f'Category: {self.name}; {self.description}'

    def __repr__(self) -> str:
        """Вернуть диагностическое строковое представление категории."""
        return f'Category: {self.name}; {self.description}'


engine = create_engine('sqlite://')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:

    new_category = Category(name='Toys', description='sports equipment, construction sets, soft toys')
    session.add(new_category)
    session.flush()

    new_products = [Product(name='Ball', price=Decimal('23.50'), in_stock=True, category_id=new_category.id
                           ), Product(name='Car', price=Decimal('10.98'), in_stock=True, category_id=new_category.id)]

    session.add_all(new_products)

    session.commit()

    categories = session.query(Category).all()
    print("\nTable 'categories':")
    for category in categories:
        print(category.id)
        print(category.name)
        print(category.description)
        for prod in category.products:
            print(prod)


    products = session.query(Product).all()
    print("\nTable 'products':")
    for product in products:
        print("\n", product.id)
        print(product.name)
        print(product.price)
        print(product.in_stock)
        print(product.category_id)
        print(product.category)








