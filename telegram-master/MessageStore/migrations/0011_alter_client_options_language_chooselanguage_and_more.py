# Generated by Django 4.0.5 on 2022-06-25 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0004_alter_whatsapp_options_alter_whatsapp_alertstatus_and_more'),
        ('MessageStore', '0010_client_lastmessage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Telegram User', 'verbose_name_plural': 'Telegram User'},
        ),
        migrations.AddField(
            model_name='language',
            name='chooseLanguage',
            field=models.CharField(default='Choose Language', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='chooseRequest',
            field=models.CharField(default='Choose Request', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='chooseSmav',
            field=models.CharField(default='Choose SMAV', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='request',
            field=models.CharField(default='Request', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='selectSmav',
            field=models.CharField(default='Select a SMAV', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='setAlarm',
            field=models.CharField(default='Set Alarm', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='smavList',
            field=models.CharField(default='SMAV List', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='wellcome',
            field=models.CharField(default='Welcome to SMAV', max_length=30),
        ),
        migrations.AlterField(
            model_name='client',
            name='alertStatus',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='lastmessage',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='device',
            name='clients',
            field=models.ManyToManyField(blank=True, to='MessageStore.client', verbose_name='Telegram Users'),
        ),
        migrations.AlterField(
            model_name='device',
            name='whatsapps',
            field=models.ManyToManyField(blank=True, to='webhooks.whatsapp', verbose_name='WhatsApp Users'),
        ),
        migrations.CreateModel(
            name='DeviceGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='SMAV Group Name')),
                ('devices', models.ManyToManyField(blank=True, to='MessageStore.device', verbose_name='Device Group')),
            ],
        ),
    ]
