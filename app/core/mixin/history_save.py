import json

from django.db import models

from core.middleware.get_request import get_request
from core.models.history import History


class SaveHistory(models.Model):

    class Meta:
        abstract = True

    @property
    def fields(self):
        return [ f.name for f in self._meta.fields + self._meta.many_to_many ]


    def save(self, *args, **kwargs):
        """ OverRides save for keeping model history.

        Not a Full-Override as this is just to add to existing.

        Before to fetch from DB to ensure the changed value is the actual changed value and the after
        is the data that was saved to the DB.
        """

        remove_keys = [
            '_state',
            'created',
            'modified'
        ]
        before = {}

        try:
            before = self.__class__.objects.get(pk=self.pk).__dict__.copy()
        except Exception:
            pass

        clean = {}
        for entry in before:

            if type(before[entry]) == type(int()):

                value = int(before[entry])

            elif type(before[entry]) == type(bool()):

                value = bool(before[entry])

            else:

                value = str(before[entry])


            if entry not in remove_keys:
                clean[entry] = value

        before_json = json.dumps(clean)

        # Process the save
        super().save(*args, **kwargs)

        after = self.__dict__.copy()

        clean = {}
        for entry in after:

            if type(after[entry]) == type(int()):

                value = int(after[entry])

            elif type(after[entry]) == type(bool()):

                value = bool(after[entry])

            else:

                value = str(after[entry])


            if entry not in remove_keys and str(before) != '{}':

                if after[entry] != before[entry]:
                    clean[entry] = value

            elif entry not in remove_keys:

                clean[entry] = value


        after = json.dumps(clean)

        item_parent_pk = None
        item_parent_class = None

        if self._meta.model_name == 'deviceoperatingsystem':

            item_parent_pk = self.device.pk
            item_parent_class = self.device._meta.model_name

        if self._meta.model_name == 'devicesoftware':

            item_parent_pk = self.device.pk
            item_parent_class = self.device._meta.model_name

        if self._meta.model_name == 'operatingsystemversion':

            item_parent_pk = self.operating_system_id
            item_parent_class = self.operating_system._meta.model_name


        if self._meta.model_name == 'softwareversion':

            item_parent_pk = self.software.pk
            item_parent_class = self.software._meta.model_name

        if self._meta.model_name == 'team':

            item_parent_pk = self.organization.pk
            item_parent_class = self.organization._meta.model_name

        if self._meta.model_name == 'teamusers':

            item_parent_pk = self.team.pk
            item_parent_class = self.team._meta.model_name


        if not before:

            action = History.Actions.ADD

        elif before != after:

            action = History.Actions.UPDATE

        elif not after:

            action = History.Actions.DELETE

        current_user = None
        if get_request() is not None:

            current_user = get_request().user


        if before != after and after != '{}':
            entry = History.objects.create(
                before = before_json,
                after = after,
                user = current_user,
                action = action,
                item_pk = self.pk,
                item_class = self._meta.model_name,
                item_parent_pk = item_parent_pk,
                item_parent_class = item_parent_class,
            )

            entry.save()
