from src.domain.products.use_cases.product_user_case import ProductServiceImpl
from src.domain.products.use_cases.api_data_loader import ApiDataLoaderService
from src.domain.products.use_cases.background_loader import BackgroundDataLoader
from src.infrastructure.database.engine import get_session
from src.infrastructure.database.repositories.product_repository import ProductRepositoryImpl
from src.infrastructure.database.repositories.category_repository import CategoryRepositoryImpl
from src.infrastructure.database.repositories.product_parameter_repository import ProductParameterRepositoryImpl
from src.infrastructure.database.repositories.product_image_repository import ProductImageRepositoryImpl
from src.settings import settings

# ------- repositories ---------
def get_product_repository(session=None) -> ProductRepositoryImpl:
    if session is None:
        session = next(get_session())
    return ProductRepositoryImpl(session)

def get_category_repository(session=None) -> CategoryRepositoryImpl:
    if session is None:
        session = next(get_session())
    return CategoryRepositoryImpl(session)

def get_product_parameter_repository(session=None) -> ProductParameterRepositoryImpl:
    if session is None:
        session = next(get_session())
    return ProductParameterRepositoryImpl(session)

def get_product_image_repository(session=None) -> ProductImageRepositoryImpl:
    if session is None:
        session = next(get_session())
    return ProductImageRepositoryImpl(session)

# ------- services ------
def get_product_service() -> ProductServiceImpl:
    session = next(get_session())
    product_repo = get_product_repository(session)
    category_repo = get_category_repository(session)
    return ProductServiceImpl(product_repo, category_repo)

def get_api_data_loader_service() -> ApiDataLoaderService:
    session = next(get_session())
    product_repo = get_product_repository(session)
    category_repo = get_category_repository(session)
    parameter_repo = get_product_parameter_repository(session)
    image_repo = get_product_image_repository(session)
    return ApiDataLoaderService(product_repo, category_repo, parameter_repo, image_repo)

def get_background_loader_service() -> BackgroundDataLoader:
    api_loader = get_api_data_loader_service()
    interval_minutes = settings.db.interval_upload
    return BackgroundDataLoader(api_loader, interval_minutes)

