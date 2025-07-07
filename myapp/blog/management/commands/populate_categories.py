from blog.models import Category
from django.core.management.base import BaseCommand 
from typing import Any




class Command(BaseCommand):
    help =" This command inserts Category data"
    def handle(self, *args, **options):
        # Delete Exiting Data

        Category.objects.all().delete()

        categories=['Sports','Technology','Science','Art','Food']

        for category_name in categories:
            Category.objects.create(name= category_name )

        self.stdout.write(self.style.SUCCESS("completed inserting Data!!"))