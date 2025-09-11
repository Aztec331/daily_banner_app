from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('mediafiles', '0001_initial'),  # replace with your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='user',
            field=models.ForeignKey(
                default=1,  # assign all existing media to admin user
                on_delete=models.CASCADE,
                related_name='mediafiles',
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
