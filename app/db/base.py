# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.lead import Lead  # noqa
from app.models.message import Message  # noqa
from app.models.chat_session import ChatSession  # noqa
from app.models.chat_feedback import ChatFeedback  # noqa
from app.models.analytics_event import AnalyticsEvent  # noqa

