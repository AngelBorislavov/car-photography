from django.db import migrations, models
import django.db.models.deletion


def link_existing_photographers(apps, schema_editor):
    CarPhoto = apps.get_model("photos", "CarPhoto")
    Photographer = apps.get_model("photographers", "Photographers")
    database = schema_editor.connection.alias
    photographer_ids = {
        photographer.name: photographer.pk
        for photographer in Photographer.objects.using(database).all()
    }

    for photo in CarPhoto.objects.using(database).all().iterator():
        photographer_id = photographer_ids.get(photo.photographer)
        if photographer_id is not None:
            photo.photographer_link_id = photographer_id
            photo.save(using=database, update_fields=["photographer_link"])


class Migration(migrations.Migration):

    dependencies = [
        ("photographers", "0001_initial"),
        ("photos", "0002_rename_author_carphoto_photographer"),
    ]

    operations = [
        migrations.AddField(
            model_name="carphoto",
            name="photographer_link",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="photos",
                to="photographers.photographers",
            ),
        ),
        migrations.RunPython(
            link_existing_photographers,
            migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name="carphoto",
            name="photographer",
        ),
        migrations.RenameField(
            model_name="carphoto",
            old_name="photographer_link",
            new_name="photographer",
        ),
    ]