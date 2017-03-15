# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('django_prbac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('salesforce_account_id', models.CharField(help_text=b'This is how we link to the salesforce account', max_length=80, null=True, db_index=True, blank=True)),
                ('created_by', models.CharField(max_length=80)),
                ('created_by_domain', models.CharField(max_length=256, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('dimagi_contact', models.CharField(max_length=80, null=True, blank=True)),
                ('is_auto_invoiceable', models.BooleanField(default=False)),
                ('date_confirmed_extra_charges', models.DateTimeField(null=True, blank=True)),
                ('account_type', models.CharField(default=b'CONTRACT', max_length=25, choices=[(b'CONTRACT', b'Created by contract'), (b'USER_CREATED', b'Created by user'), (b'GLOBAL_SERVICES', b'Created by Global Services'), (b'INVOICE_GENERATED', b'Generated by an invoice'), (b'TRIAL', b'Is trial account')])),
                ('is_active', models.BooleanField(default=True)),
                ('entry_point', models.CharField(default=b'NOT_SET', max_length=25, choices=[(b'CONTRACTED', b'Contracted'), (b'SELF_STARTED', b'Self-started'), (b'NOT_SET', b'Not Set')])),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BillingContactInfo',
            fields=[
                ('account', models.OneToOneField(primary_key=True, serialize=False, to='accounting.BillingAccount', on_delete=models.CASCADE)),
                ('first_name', models.CharField(max_length=50, null=True, verbose_name='First Name', blank=True)),
                ('last_name', models.CharField(max_length=50, null=True, verbose_name='Last Name', blank=True)),
                ('emails', models.CharField(help_text='We will email communications regarding your account to the emails specified here.', max_length=200, null=True, verbose_name='Contact Emails')),
                ('phone_number', models.CharField(max_length=20, null=True, verbose_name='Phone Number', blank=True)),
                ('company_name', models.CharField(max_length=50, null=True, verbose_name='Company / Organization', blank=True)),
                ('first_line', models.CharField(max_length=50, verbose_name='Address First Line')),
                ('second_line', models.CharField(max_length=50, null=True, verbose_name='Address Second Line', blank=True)),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('state_province_region', models.CharField(max_length=50, verbose_name='State / Province / Region')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Postal Code')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BillingRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('emailed_to', models.CharField(max_length=254, db_index=True)),
                ('skipped_email', models.BooleanField(default=False)),
                ('pdf_data_id', models.CharField(max_length=48)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CreditAdjustment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(default=b'MANUAL', max_length=25, choices=[(b'MANUAL', b'manual'), (b'SALESFORCE', b'via Salesforce'), (b'INVOICE', b'invoice generated'), (b'LINE_ITEM', b'line item generated'), (b'TRANSFER', b'transfer from another credit line'), (b'DIRECT_PAYMENT', b'payment from client received')])),
                ('note', models.TextField()),
                ('amount', models.DecimalField(default=Decimal('0.0000'), max_digits=10, decimal_places=4)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('web_user', models.CharField(max_length=80, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CreditLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_type', models.CharField(blank=True, max_length=25, null=True, choices=[(b'CommCare', b'CommCare'), (b'CommTrack', b'CommTrack'), (b'CommConnect', b'CommConnect')])),
                ('feature_type', models.CharField(blank=True, max_length=10, null=True, choices=[(b'User', b'User'), (b'SMS', b'SMS')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('balance', models.DecimalField(default=Decimal('0.0000'), max_digits=10, decimal_places=4)),
                ('is_active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(to='accounting.BillingAccount', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=3)),
                ('name', models.CharField(max_length=25, db_index=True)),
                ('symbol', models.CharField(max_length=10)),
                ('rate_to_default', models.DecimalField(default=Decimal('1.0'), max_digits=20, decimal_places=9)),
                ('date_updated', models.DateField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DefaultProductPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_type', models.CharField(max_length=25, choices=[(b'CommCare', b'CommCare'), (b'CommTrack', b'CommTrack'), (b'CommConnect', b'CommConnect')])),
                ('edition', models.CharField(default=b'Community', max_length=25, choices=[(b'Community', b'Community'), (b'Standard', b'Standard'), (b'Pro', b'Pro'), (b'Advanced', b'Advanced'), (b'Enterprise', b'Enterprise')])),
                ('is_trial', models.BooleanField(default=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('feature_type', models.CharField(db_index=True, max_length=10, choices=[(b'User', b'User'), (b'SMS', b'SMS')])),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeatureRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monthly_fee', models.DecimalField(default=Decimal('0.00'), verbose_name=b'Monthly Fee', max_digits=10, decimal_places=2)),
                ('monthly_limit', models.IntegerField(default=0, verbose_name=b'Monthly Included Limit', validators=[django.core.validators.MaxValueValidator(2147483647), django.core.validators.MinValueValidator(-2147483648)])),
                ('per_excess_fee', models.DecimalField(default=Decimal('0.00'), verbose_name=b'Fee Per Excess of Limit', max_digits=10, decimal_places=2)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('feature', models.ForeignKey(to='accounting.Feature', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_received', models.DateField(db_index=True, null=True, blank=True)),
                ('is_hidden', models.BooleanField(default=False)),
                ('tax_rate', models.DecimalField(default=Decimal('0.0000'), max_digits=10, decimal_places=4)),
                ('balance', models.DecimalField(default=Decimal('0.0000'), max_digits=10, decimal_places=4)),
                ('date_due', models.DateField(null=True, db_index=True)),
                ('date_paid', models.DateField(null=True, blank=True)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('is_hidden_to_ops', models.BooleanField(default=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_description', models.TextField(null=True, blank=True)),
                ('base_cost', models.DecimalField(default=Decimal('0.0000'), max_digits=10, decimal_places=4)),
                ('unit_description', models.TextField(null=True, blank=True)),
                ('unit_cost', models.DecimalField(default=Decimal('0.0000'), max_digits=10, decimal_places=4)),
                ('quantity', models.IntegerField(default=1)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('feature_rate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.FeatureRate', null=True)),
                ('invoice', models.ForeignKey(to='accounting.Invoice', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('web_user', models.CharField(max_length=80, null=True, db_index=True)),
                ('method_type', models.CharField(default=b'Stripe', max_length=50, db_index=True, choices=[(b'Stripe', b'Stripe')])),
                ('customer_id', models.CharField(max_length=255, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('transaction_id', models.CharField(max_length=255)),
                ('amount', models.DecimalField(default=Decimal('0.0000'), max_digits=10, decimal_places=4)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('payment_method', models.ForeignKey(to='accounting.PaymentMethod', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SoftwarePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
                ('description', models.TextField(help_text=b'If the visibility is INTERNAL, this description field will be used.', blank=True)),
                ('edition', models.CharField(default=b'Enterprise', max_length=25, choices=[(b'Community', b'Community'), (b'Standard', b'Standard'), (b'Pro', b'Pro'), (b'Advanced', b'Advanced'), (b'Enterprise', b'Enterprise')])),
                ('visibility', models.CharField(default=b'INTERNAL', max_length=10, choices=[(b'PUBLIC', b'Anyone can subscribe'), (b'INTERNAL', b'Dimagi must create subscription'), (b'TRIAL', b'This is a Trial Plan'), (b'TRIAL_INT', b'This is special Trial plan that Dimagi manages.')])),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SoftwarePlanVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('feature_rates', models.ManyToManyField(to='accounting.FeatureRate', blank=True)),
                ('plan', models.ForeignKey(to='accounting.SoftwarePlan', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SoftwareProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('product_type', models.CharField(db_index=True, max_length=25, choices=[(b'CommCare', b'CommCare'), (b'CommTrack', b'CommTrack'), (b'CommConnect', b'CommConnect')])),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SoftwareProductRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monthly_fee', models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(to='accounting.SoftwareProduct', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=256, null=True, db_index=True)),
                ('organization', models.CharField(max_length=256, null=True, db_index=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('salesforce_contract_id', models.CharField(max_length=80, null=True, blank=True)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField(null=True, blank=True)),
                ('date_delay_invoicing', models.DateField(null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('do_not_invoice', models.BooleanField(default=False)),
                ('auto_generate_credits', models.BooleanField(default=False)),
                ('is_trial', models.BooleanField(default=False)),
                ('service_type', models.CharField(default=b'NOT_SET', max_length=25, choices=[(b'CONTRACTED', b'Contracted'), (b'SELF_SERVICE', b'Self-service'), (b'NOT_SET', b'Not Set')])),
                ('pro_bono_status', models.CharField(default=b'NOT_SET', max_length=25, choices=[(b'YES', b'Yes'), (b'NO', b'No'), (b'DISCOUNTED', b'Discounted'), (b'NOT_SET', b'Not Set')])),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(to='accounting.BillingAccount', on_delete=django.db.models.deletion.PROTECT)),
                ('plan_version', models.ForeignKey(to='accounting.SoftwarePlanVersion', on_delete=django.db.models.deletion.PROTECT)),
                ('subscriber', models.ForeignKey(to='accounting.Subscriber', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubscriptionAdjustment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(default=b'CREATE', max_length=50, choices=[(b'CREATE', b'A new subscription created from scratch.'), (b'MODIFY', b'Some part of the subscription was modified...likely a date.'), (b'CANCEL', b'The subscription was cancelled with no followup subscription.'), (b'UPGRADE', b'The subscription was upgraded to the related subscription.'), (b'DOWNGRADE', b'The subscription was downgraded to the related subscription.'), (b'SWITCH', b'The plan was changed to the related subscription and was neither an upgrade or downgrade.'), (b'REACTIVATE', b'The subscription was reactivated.'), (b'RENEW', b'The subscription was renewed.')])),
                ('method', models.CharField(default=b'INTERNAL', max_length=50, choices=[(b'USER', b'User'), (b'INTERNAL', b'Ops'), (b'TASK', b'Task (Invoicing)'), (b'TRIAL', b'30 Day Trial'), (b'TRIAL_INT', b'Custom Trial Period')])),
                ('note', models.TextField(null=True)),
                ('web_user', models.CharField(max_length=80, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('new_date_start', models.DateField()),
                ('new_date_end', models.DateField(null=True, blank=True)),
                ('new_date_delay_invoicing', models.DateField(null=True, blank=True)),
                ('new_salesforce_contract_id', models.CharField(max_length=80, null=True, blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.Invoice', null=True)),
                ('related_subscription', models.ForeignKey(related_name='subscriptionadjustment_related', on_delete=django.db.models.deletion.PROTECT, to='accounting.Subscription', null=True)),
                ('subscription', models.ForeignKey(to='accounting.Subscription', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WireBillingRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('emailed_to', models.CharField(max_length=254, db_index=True)),
                ('skipped_email', models.BooleanField(default=False)),
                ('pdf_data_id', models.CharField(max_length=48)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WireInvoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_received', models.DateField(db_index=True, null=True, blank=True)),
                ('is_hidden', models.BooleanField(default=False)),
                ('tax_rate', models.DecimalField(default=Decimal('0.0000'), max_digits=10, decimal_places=4)),
                ('balance', models.DecimalField(default=Decimal('0.0000'), max_digits=10, decimal_places=4)),
                ('date_due', models.DateField(null=True, db_index=True)),
                ('date_paid', models.DateField(null=True, blank=True)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('is_hidden_to_ops', models.BooleanField(default=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('domain', models.CharField(max_length=80)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='wirebillingrecord',
            name='invoice',
            field=models.ForeignKey(to='accounting.WireInvoice', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='softwareplanversion',
            name='product_rates',
            field=models.ManyToManyField(to='accounting.SoftwareProductRate', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='softwareplanversion',
            name='role',
            field=models.ForeignKey(to='django_prbac.Role', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lineitem',
            name='product_rate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.SoftwareProductRate', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='subscription',
            field=models.ForeignKey(to='accounting.Subscription', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='defaultproductplan',
            name='plan',
            field=models.ForeignKey(to='accounting.SoftwarePlan', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='creditline',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='accounting.Subscription', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='creditadjustment',
            name='credit_line',
            field=models.ForeignKey(to='accounting.CreditLine', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='creditadjustment',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.Invoice', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='creditadjustment',
            name='line_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.LineItem', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='creditadjustment',
            name='payment_record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.PaymentRecord', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='creditadjustment',
            name='related_credit',
            field=models.ForeignKey(related_name='creditadjustment_related', on_delete=django.db.models.deletion.PROTECT, to='accounting.CreditLine', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='billingrecord',
            name='invoice',
            field=models.ForeignKey(to='accounting.Invoice', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='billingaccount',
            name='currency',
            field=models.ForeignKey(to='accounting.Currency', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='WirePrepaymentBillingRecord',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('accounting.wirebillingrecord',),
        ),
        migrations.CreateModel(
            name='WirePrepaymentInvoice',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('accounting.wireinvoice',),
        ),
    ]