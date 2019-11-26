# Generated by Django 2.2.4 on 2019-11-02 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20191019_1610'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Discussao',
        ),
        migrations.DeleteModel(
            name='Pergunta',
        ),
        migrations.AddField(
            model_name='postagem',
            name='tipo',
            field=models.CharField(choices=[('P', 'Pergunta'), ('D', 'Discussão')], default='D', max_length=1),
        ),
        migrations.AddField(
            model_name='postagem',
            name='titulo',
            field=models.CharField(default='', max_length=100),
        ),
    ]