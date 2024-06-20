# item/management/commands/create_groups_permissions.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from item.models import Item, Order, Category, ItemImage, Cart, CartItem
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates groups and assigns permissions for the application'

    def handle(self, *args, **kwargs):
        # Create groups if they do not exist
        customer_group, created = Group.objects.get_or_create(name='Customer')
        safe_group, created = Group.objects.get_or_create(name='Safe')
        staff_group, created = Group.objects.get_or_create(name='Staff')
        admin_group, created = Group.objects.get_or_create(name='Admin')

        # Define permissions for each model
        item_ct = ContentType.objects.get_for_model(Item)
        order_ct = ContentType.objects.get_for_model(Order)
        category_ct = ContentType.objects.get_for_model(Category)
        item_image_ct = ContentType.objects.get_for_model(ItemImage)
        cart_ct = ContentType.objects.get_for_model(Cart)
        cart_item_ct = ContentType.objects.get_for_model(CartItem)

        # Assign permissions to groups
        customer_group.permissions.set([
            Permission.objects.get(codename='view_order'),
            Permission.objects.get(codename='view_profile'),
            Permission.objects.get(codename='view_profile')
        ])

        safe_group.permissions.set([
            Permission.objects.get(codename='view_order'),
            Permission.objects.get(codename='view_profile'),
            Permission.objects.get(codename='view_item'),
            Permission.objects.get(codename='view_dashboard'),
        ])

        staff_group.permissions.set([
            Permission.objects.get(codename='view_item'),
            Permission.objects.get(codename='add_item'),
            Permission.objects.get(codename='view_dashboard'),
            Permission.objects.get(codename='view_profile'),
            Permission.objects.get(codename='view_order'),
            Permission.objects.get(codename='view_shipping'),
        ])

        admin_group.permissions.set([
            Permission.objects.get(codename='view_item'),
            Permission.objects.get(codename='add_item'),
            Permission.objects.get(codename='view_dashboard'),
            Permission.objects.get(codename='view_profile'),
            Permission.objects.get(codename='add_profile'),
            Permission.objects.get(codename='view_order'),
            Permission.objects.get(codename='add_order'),
            Permission.objects.get(codename='view_shipping'),
            Permission.objects.get(codename='add_shipping'),
        ])

        self.stdout.write(self.style.SUCCESS('Groups and permissions have been created successfully.'))
