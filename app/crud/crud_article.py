from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate

class CRUDArticle(CRUDBase[Article, ArticleCreate, ArticleUpdate]):
    pass

article = CRUDArticle(Article)
