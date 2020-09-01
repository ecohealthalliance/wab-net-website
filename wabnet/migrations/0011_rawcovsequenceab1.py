# Generated by Django 3.0.7 on 2020-08-14 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wabnet', '0010_georgia_barcoding_georgia_screening'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawCovSequenceAb1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airtable_id', models.TextField()),
                ('url', models.TextField()),
                ('filename', models.TextField()),
                ('size', models.PositiveIntegerField()),
                ('type', models.TextField()),
                ('screening_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wabnet.Georgia_screening')),
            ],
        ),
    ]