
from django.dispatch import receiver

from core.models.ticket.ticket_linked_items import deleted_model, TicketLinkedItem



@receiver(deleted_model)
def signal_deleted_model(sender, item_id, item_type, **kwargs):
    """Clean up model TicketLinkedItems

    a model was deleted, remove its link to any tickets it had.
    """

    items = TicketLinkedItem.objects.filter(
        item_type = item_type,
        item = item_id
    )

    items.delete()
