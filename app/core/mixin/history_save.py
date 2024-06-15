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

    def save_history(self, before: dict, after: dict):
        """ Save a Models Changes

        Args:
            before (dict): model before saving (model.objects.get().__dict__)
            after (dict): model after saving and refetched from DB (model.objects.get().__dict__)
        """

        remove_keys = [
            '_state',
            'created',
            'modified'
        ]

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


        after_json = json.dumps(clean)

        item_parent_pk = None
        item_parent_class = None


        if hasattr(self, 'parent_object'):

            if self.parent_object:

                item_parent_pk = self.parent_object.pk
                item_parent_class = self.parent_object._meta.model_name


        item_pk = self.pk

        if not before:

            action = History.Actions.ADD

        elif before_json != after_json and self.pk:

            action = History.Actions.UPDATE

        elif self.pk is None:

            action = History.Actions.DELETE
            item_pk = before['id']
            after_json = None


        current_user = None
        if get_request() is not None:

            current_user = get_request().user

            if current_user.is_anonymous:
                current_user = None


        # if before != after_json and after_json != '{}':
        if before_json != after_json:
            entry = History.objects.create(
                before = before_json,
                after = after_json,
                user = current_user,
                action = action,
                item_pk = item_pk,
                item_class = self._meta.model_name,
                item_parent_pk = item_parent_pk,
                item_parent_class = item_parent_class,
            )

            entry.save()


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """ OverRides save for keeping model history.

        Not a Full-Override as this is just to add to existing.

        Before to fetch from DB to ensure the changed value is the actual changed value and the after
        is the data that was saved to the DB.
        """

        before = {}

        try:
            before = self.__class__.objects.get(pk=self.pk).__dict__.copy()
        except Exception:
            pass

        # Process the save
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        after = self.__dict__.copy()

        self.save_history(before, after)


    def delete_history(self, item_pk, item_class):
        """ Delete the objects history

        When an object is no longer in the database, delete the objects history and
        that of the child objects. Only caveat is that if the history has a parent_pk
        the object history is not to be deleted.

        Args:
            item_pk (int): Primary key of the object to be deleted
            item_class (str): Object class of the object to be deleted
        """

        object_history = History.objects.filter(
            item_pk = item_pk,
            item_class = item_class,
            item_parent_pk = None,
        )

        if object_history.exists():

            object_history.delete()

        child_object_history = History.objects.filter(
            item_parent_pk = item_pk,
            item_parent_class = item_class,
        )

        if child_object_history.exists():

            child_object_history.delete()


    def delete(self, using=None, keep_parents=False):
        """ OverRides delete for keeping model history and on parent object ONLY!.

        Not a Full-Override as this is just to add to existing.
        """

        before = {}
        item_pk = self.pk
        item_class = self._meta.model_name

        try:

            before = self.__class__.objects.get(pk=self.pk).__dict__.copy()

        except Exception:

            pass

        # Process the delete
        super().delete(using=using, keep_parents=keep_parents)

        after = self.__dict__.copy()

        if hasattr(self, 'parent_object'):

            self.save_history(before, after)

        else:

            self.delete_history(item_pk, item_class)
