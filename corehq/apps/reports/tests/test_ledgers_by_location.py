import datetime
import mock
from uuid import uuid4

from django.db.models.signals import post_save
from django.test import TestCase

from corehq.apps.commtrack.models import StockState, update_domain_mapping
from corehq.apps.commtrack.tests.util import make_loc
from corehq.apps.locations.models import LocationType
from corehq.apps.locations.tests.util import delete_all_locations
from corehq.apps.products.models import SQLProduct

from corehq.apps.reports.commtrack import LedgersByLocationDataSource


class TestLedgersByLocation(TestCase):
    @classmethod
    def setUpClass(cls):
        def make_stock_state(location, product, soh):
            return StockState.objects.create(
                section_id='stock',
                sql_location=location,
                case_id=uuid4().hex,
                sql_product=product,
                product_id=product.product_id,
                stock_on_hand=soh,
                last_modified_date=datetime.datetime.now(),
            )

        def make_product(name):
            return SQLProduct.objects.create(domain='test', name=name,
                                             product_id=uuid4().hex)

        def make_location(name):
            return make_loc(name, domain='test').sql_location

        # turn off the StockState post_save signal handler
        post_save.disconnect(update_domain_mapping, StockState)

        cls.aspirin = make_product(name="Aspirin")
        cls.bandaids = make_product(name="Bandaids")

        cls.boston = make_location("Boston")
        make_stock_state(cls.boston, cls.aspirin, 135)
        make_stock_state(cls.boston, cls.bandaids, 43)

        cls.cambridge = make_location("Cambridge")
        make_stock_state(cls.cambridge, cls.aspirin, 414)
        make_stock_state(cls.cambridge, cls.bandaids, 107)

        cls.allston = make_location(name="Allston")

    @classmethod
    def tearDownClass(cls):
        delete_all_locations()

    def test_show_all_rows_ordered(self):
        report = LedgersByLocationDataSource(
            'test',
            params={'ledger_section': 'stock'},
        )
        self.assertEqual(
            [row.location.name for row in report.rows],
            [self.allston.name, self.boston.name, self.cambridge.name]
        )

    def test_one_row(self):
        report = LedgersByLocationDataSource(
            'test',
            params={'ledger_section': 'stock'},
        )
        boston = [row for row in report.rows if row.location.name == "Boston"][0]
        self.assertEqual(boston.stock[self.aspirin.product_id], 135)
        self.assertEqual(boston.stock[self.bandaids.product_id], 43)

    def test_another_ledger_section(self):
        self.fail()
