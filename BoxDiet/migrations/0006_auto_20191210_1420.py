# Generated by Django 2.2.6 on 2019-12-10 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("BoxDiet", "0005_reccomended"),
    ]

    operations = [
        migrations.RenameModel(old_name="Reccomended", new_name="Recommended", ),
        migrations.AlterModelOptions(
            name="meal", options={"ordering": ["-average_rank"]},
        ),
    ]
