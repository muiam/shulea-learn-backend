# Generated by Django 5.1 on 2024-09-07 18:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapi', '0003_post_owner_alter_bid_tutor_alter_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_balance', models.IntegerField(default=0.0)),
                ('owner', models.ForeignKey(limit_choices_to={'type': 'Learner'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
