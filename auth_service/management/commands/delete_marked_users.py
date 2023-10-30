from logging import getLogger

from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Subquery

from auth_service.models import DeletedUsers

DELETE_AFTER_DAYS = 7


class Command(BaseCommand):
    help = 'Delete users after some days from their request'

    def handle(self, *args, **options):
        logger = getLogger('django')
        min_date_of_request = datetime.utcnow() - timedelta(days=DELETE_AFTER_DAYS)
        marked_users = DeletedUsers.objects.filter(dt_delete__le=min_date_of_request, step=DeletedUsers.STEP_MARKED)

        user_model = get_user_model()
        users = user_model.objects.filter(microservice_auth_id__in=Subquery(marked_users, 'microservice_auth_id__in'))
        count_delete_users = users.count()
        users.delete()
        marked_users.update(step=DeletedUsers.STEP_DELETED)
        logger.info(f'Deleted {count_delete_users} users.')
