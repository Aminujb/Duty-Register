# Generated by Django 3.1 on 2020-08-22 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UnitType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Unit type',
                'verbose_name_plural': 'Unit types',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('head_count', models.IntegerField(blank=True, null=True, verbose_name='Head count')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='register.unit')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='register.unittype')),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
                'ordering': ('name', 'type'),
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=50)),
                ('country', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='register.country')),
            ],
            options={
                'verbose_name': 'Nigerian State',
                'verbose_name_plural': 'Nigerian States',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('is_head', models.BooleanField(default=False, verbose_name='Unit head')),
                ('reports_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='register.rank')),
            ],
            options={
                'verbose_name': 'Rank',
                'verbose_name_plural': 'Ranks',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='LGA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='local_govt_areas', to='register.state')),
            ],
            options={
                'verbose_name': 'Nigerian Local Government Area',
                'verbose_name_plural': 'Nigerian Local Government Areas',
                'ordering': ['state', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=50, verbose_name='Surname')),
                ('first_name', models.CharField(max_length=50, verbose_name='First name')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Middle name')),
                ('marital_status', models.CharField(blank=True, choices=[('Single', 'Single'), ('Married', 'Married'), ('Widowed', 'Widowed'), ('Divorced', 'Divorced')], max_length=20, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'), ('Unknown', 'Unknown')], default='Female', max_length=10)),
                ('birth_date', models.DateField(blank=True, db_index=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='register/photos/%Y/%m/')),
                ('religion', models.CharField(blank=True, choices=[('Christianity', 'Christianity'), ('Islam', 'Islam'), ('Others', 'Others')], max_length=50, null=True)),
                ('blood_group', models.CharField(blank=True, choices=[('A', 'A'), ('AB', 'AB'), ('B', 'B'), ('O+', 'O+'), ('O-', 'O-')], max_length=2, null=True)),
                ('genotype', models.CharField(blank=True, choices=[('AA', 'AA'), ('AS', 'AS'), ('SS', 'SS')], max_length=2, null=True)),
                ('national_id_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='National ID Number')),
                ('passport_number', models.CharField(blank=True, max_length=20, null=True)),
                ('permanent_address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('last_pass', models.DateTimeField(verbose_name='date published')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country_of_residence', to='register.country')),
                ('lga', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='register.lga', verbose_name='LGA')),
                ('rank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='register.rank')),
                ('state_of_origin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees_origin', to='register.state')),
                ('state_of_residence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees_residence', to='register.state')),
                ('unit', models.ForeignKey(blank=True, help_text='The department or division this employee is being assigned to', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='register.unit')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'ordering': ('first_name', 'last_name'),
            },
        ),
    ]
