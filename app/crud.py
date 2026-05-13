from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Category, Product, Order, User
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.order import OrderCreate, OrderUpdate

async def get_category(db: AsyncSession, category_id: int) -> Category | None:
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()

async def get_categories(db: AsyncSession) -> list[Category]:
    result = await db.execute(select(Category))
    return result.scalars().all()

async def create_category(db: AsyncSession, category_in: CategoryCreate) -> Category:
    category = Category(name=category_in.name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

async def update_category(db: AsyncSession, category_id: int, category_in: CategoryUpdate) -> Category | None:
    category = await get_category(db, category_id)
    if category is None:
        return None
    category.name = category_in.name
    await db.commit()
    await db.refresh(category)
    return category

async def delete_category(db: AsyncSession, category_id: int) -> bool:
    category = await get_category(db, category_id)
    if category is None:
        return False
    await db.delete(category)
    await db.commit()
    return True

async def get_product(db: AsyncSession, product_id: int) -> Product | None:
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()

async def get_products(db: AsyncSession) -> list[Product]:
    result = await db.execute(select(Product))
    return result.scalars().all()

async def create_product(db: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(
        title=product_in.title,
        price=product_in.price,
        category_id=product_in.category_id,
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

async def update_product(db: AsyncSession, product_id: int, product_in: ProductUpdate) -> Product | None:
    product = await get_product(db, product_id)
    if product is None:
        return None
    product.title = product_in.title
    product.price = product_in.price
    product.category_id = product_in.category_id
    await db.commit()
    await db.refresh(product)
    return product

async def delete_product(db: AsyncSession, product_id: int) -> bool:
    product = await get_product(db, product_id)
    if product is None:
        return False
    await db.delete(product)
    await db.commit()
    return True

async def get_order(db: AsyncSession, order_id: int) -> Order | None:
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()

async def get_orders(db: AsyncSession) -> list[Order]:
    result = await db.execute(select(Order))
    return result.scalars().all()

async def get_user(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)

async def create_order(db: AsyncSession, order_in: OrderCreate) -> Order | None:
    user = await get_user(db, order_in.user_id)
    if user is None:
        return None
    order = Order(item_name=order_in.item_name, user_id=order_in.user_id)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

async def update_order(db: AsyncSession, order_id: int, order_in: OrderUpdate) -> Order | None:
    order = await get_order(db, order_id)
    if order is None:
        return None
    order.item_name = order_in.item_name
    order.user_id = order_in.user_id
    await db.commit()
    await db.refresh(order)
    return order

async def delete_order(db: AsyncSession, order_id: int) -> bool:
    order = await get_order(db, order_id)
    if order is None:
        return False
    await db.delete(order)
    await db.commit()
    return True
