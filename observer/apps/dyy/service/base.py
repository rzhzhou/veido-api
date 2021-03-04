from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group


def is_task_created(rule_id):

	queryset = ScrapyTasks.objects.using('yj').filter(rule_id=rule_id)

	if queryset.exists():
		return True
	else:
		return False
