from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_alter_carphoto_photographer'),
    ]

    operations = [
        migrations.AddField(
            model_name='carphoto',
            name='title',
            field=models.CharField(default='Untitled', max_length=100),
            preserve_default=False,
        ),
    ]