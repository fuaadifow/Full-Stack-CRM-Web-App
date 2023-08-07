# Generated by Django 4.2.3 on 2023-07-26 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_alter_document_document_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(choices=[('invoice', 'Invoice'), ('certificate', 'Certificate'), ('sales_receipt', 'Sales Receipt'), ('contract', 'Contract'), ('others', 'Others')], default='invoice', max_length=20),
        ),
    ]
