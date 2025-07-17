from src.domain.products.use_cases.product_user_case import ProductServiceImpl
from src.domain.products.use_cases.api_data_loader import ApiDataLoaderService
from src.domain.products.use_cases.background_loader import BackgroundDataLoader
from src.infrastructure.database.engine import get_session
from src.infrastructure.database.repositories.product_repository import ProductRepositoryImpl
from src.infrastructure.database.repositories.category_repository import CategoryRepositoryImpl
from src.settings import settings


# ------- repositories ---------
def get_product_repository() -> ProductRepositoryImpl:
    session = next(get_session())
    return ProductRepositoryImpl(session)

def get_category_repository() -> CategoryRepositoryImpl:
    session = next(get_session())
    return CategoryRepositoryImpl(session)


# ------- services ------
def get_product_service() -> ProductServiceImpl:
    product_repo = get_product_repository()
    category_repo = get_category_repository()
    return ProductServiceImpl(product_repo, category_repo)

def get_api_data_loader_service() -> ApiDataLoaderService:
    product_repo = get_product_repository()
    category_repo = get_category_repository()
    return ApiDataLoaderService(product_repo, category_repo)

def get_background_loader_service() -> BackgroundDataLoader:
    api_loader = get_api_data_loader_service()
    interval_minutes = settings.db.interval_upload
    return BackgroundDataLoader(api_loader, interval_minutes)

