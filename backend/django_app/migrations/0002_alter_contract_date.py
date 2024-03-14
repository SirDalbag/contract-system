from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contract",
            name="date",
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
    ]
