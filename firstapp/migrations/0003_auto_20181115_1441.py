# Generated by Django 2.1.3 on 2018-11-15 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0002_auto_20181115_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testanswer',
            name='candidate_answer',
        ),
        migrations.AddField(
            model_name='candidateanswer',
            name='candidate_answer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Candidate'),
            preserve_default=False,
        ),
    ]
