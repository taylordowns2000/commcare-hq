from collections import OrderedDict, defaultdict
from datetime import datetime

from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule
from django.db.models.aggregates import Sum
from django.utils.translation import ugettext as _

from corehq.apps.locations.models import SQLLocation
from custom.icds_reports.const import LocationTypes
from custom.icds_reports.models import AggChildHealthMonthly
from custom.icds_reports.utils import apply_exclude

RED = '#de2d26'
ORANGE = '#fc9272'
BLUE = '#006fdf'
PINK = '#fee0d2'
GREY = '#9D9D9D'


def get_prevalence_of_severe_data_map(domain, config, loc_level, show_test=False):

    def get_data_for(filters):
        filters['month'] = datetime(*filters['month'])
        queryset = AggChildHealthMonthly.objects.filter(
            **filters
        ).values(
            '%s_name' % loc_level
        ).annotate(
            moderate=Sum('wasting_moderate'),
            severe=Sum('wasting_severe'),
            normal=Sum('wasting_normal'),
            valid=Sum('height_eligible'),
            total_measured=Sum('height_measured_in_month'),
        )

        if not show_test:
            queryset = apply_exclude(domain, queryset)
        return queryset

    map_data = {}

    severe_total = 0
    moderate_total = 0
    valid_total = 0

    for row in get_data_for(config):
        valid = row['valid']
        name = row['%s_name' % loc_level]

        severe = row['severe']
        moderate = row['moderate']
        normal = row['normal']
        total_measured = row['total_measured']

        severe_total += (severe or 0)
        moderate_total += (moderate or 0)
        valid_total += (valid or 0)

        value = ((moderate or 0) + (severe or 0)) * 100 / float(valid or 1)
        row_values = {
            'severe': severe or 0,
            'moderate': moderate or 0,
            'total': valid or 0,
            'normal': normal,
            'total_measured': total_measured or 0,
        }

        if value < 5:
            row_values.update({'fillKey': '0%-5%'})
        elif 5 <= value <= 7:
            row_values.update({'fillKey': '5%-7%'})
        elif value > 7:
            row_values.update({'fillKey': '7%-100%'})

        map_data.update({name: row_values})

    fills = OrderedDict()
    fills.update({'0%-5%': PINK})
    fills.update({'5%-7%': ORANGE})
    fills.update({'7%-100%': RED})
    fills.update({'defaultFill': GREY})

    return [
        {
            "slug": "severe",
            "label": "Percent of Children Wasted (6 - 60 months)",
            "fills": fills,
            "rightLegend": {
                "average": "%.2f" % (((severe_total + moderate_total) * 100) / float(valid_total or 1)),
                "info": _((
                    "Percentage of children between 6 - 60 months enrolled for ICDS services with "
                    "weight-for-height below -2 standard deviations of the WHO Child Growth Standards median. "
                    "<br/><br/>"
                    "Wasting in children is a symptom of acute undernutrition usually as a consequence "
                    "of insufficient food intake or a high incidence of infectious diseases. Severe Acute "
                    "Malnutrition (SAM) is nutritional status for a child who has severe wasting "
                    "(weight-for-height) below -3 Z and Moderate Acute Malnutrition (MAM) is nutritional "
                    "status for a child that has moderate wasting (weight-for-height) below -2Z."
                ))
            },
            "data": map_data,
        }
    ]


def get_prevalence_of_severe_data_chart(domain, config, loc_level, show_test=False):
    month = datetime(*config['month'])
    three_before = datetime(*config['month']) - relativedelta(months=3)

    config['month__range'] = (three_before, month)
    del config['month']

    chart_data = AggChildHealthMonthly.objects.filter(
        **config
    ).values(
        'month', '%s_name' % loc_level
    ).annotate(
        moderate=Sum('wasting_moderate'),
        severe=Sum('wasting_severe'),
        normal=Sum('wasting_normal'),
        valid=Sum('height_eligible'),
    ).order_by('month')

    if not show_test:
        chart_data = apply_exclude(domain, chart_data)

    data = {
        'red': OrderedDict(),
        'orange': OrderedDict(),
        'peach': OrderedDict()
    }

    dates = [dt for dt in rrule(MONTHLY, dtstart=three_before, until=month)]

    for date in dates:
        miliseconds = int(date.strftime("%s")) * 1000
        data['red'][miliseconds] = {'y': 0, 'all': 0}
        data['orange'][miliseconds] = {'y': 0, 'all': 0}
        data['peach'][miliseconds] = {'y': 0, 'all': 0}

    best_worst = {}
    for row in chart_data:
        date = row['month']
        valid = row['valid']
        location = row['%s_name' % loc_level]
        severe = row['severe']
        moderate = row['moderate']
        normal = row['normal']

        underweight = (moderate or 0) + (severe or 0)

        best_worst[location] = underweight * 100 / float(valid or 1)

        date_in_miliseconds = int(date.strftime("%s")) * 1000

        data['peach'][date_in_miliseconds]['y'] += normal
        data['peach'][date_in_miliseconds]['all'] += valid
        data['orange'][date_in_miliseconds]['y'] += moderate
        data['orange'][date_in_miliseconds]['all'] += valid
        data['red'][date_in_miliseconds]['y'] += severe
        data['red'][date_in_miliseconds]['all'] += valid

    top_locations = sorted(
        [dict(loc_name=key, percent=value) for key, value in best_worst.iteritems()],
        key=lambda x: x['percent']
    )

    return {
        "chart_data": [
            {
                "values": [
                    {
                        'x': key,
                        'y': value['y'] / float(value['all'] or 1),
                        'all': value['all']
                    } for key, value in data['peach'].iteritems()
                ],
                "key": "% normal",
                "strokeWidth": 2,
                "classed": "dashed",
                "color": PINK
            },
            {
                "values": [
                    {
                        'x': key,
                        'y': value['y'] / float(value['all'] or 1),
                        'all': value['all']
                    } for key, value in data['orange'].iteritems()
                ],
                "key": "% moderately wasted (moderate acute malnutrition)",
                "strokeWidth": 2,
                "classed": "dashed",
                "color": ORANGE
            },
            {
                "values": [
                    {
                        'x': key,
                        'y': value['y'] / float(value['all'] or 1),
                        'all': value['all']
                    } for key, value in data['red'].iteritems()
                ],
                "key": "% severely wasted (severe acute malnutrition)",
                "strokeWidth": 2,
                "classed": "dashed",
                "color": RED
            }
        ],
        "all_locations": top_locations,
        "top_five": top_locations[:5],
        "bottom_five": top_locations[-5:],
        "location_type": loc_level.title() if loc_level != LocationTypes.SUPERVISOR else 'Sector'
    }


def get_prevalence_of_severe_sector_data(domain, config, loc_level, location_id, show_test=False):
    group_by = ['%s_name' % loc_level]

    config['month'] = datetime(*config['month'])
    data = AggChildHealthMonthly.objects.filter(
        **config
    ).values(
        *group_by
    ).annotate(
        moderate=Sum('wasting_moderate'),
        severe=Sum('wasting_severe'),
        valid=Sum('height_eligible'),
        normal=Sum('wasting_normal'),
        total_measured=Sum('height_measured_in_month'),
    ).order_by('%s_name' % loc_level)

    if not show_test:
        data = apply_exclude(domain, data)

    chart_data = {
        'blue': [],
    }

    tooltips_data = defaultdict(lambda: {
        'severe': 0,
        'moderate': 0,
        'total': 0,
        'normal': 0,
        'total_measured': 0
    })

    loc_children = SQLLocation.objects.get(location_id=location_id).get_children()
    result_set = set()

    for row in data:
        valid = row['valid']
        name = row['%s_name' % loc_level]
        result_set.add(name)

        severe = row['severe']
        moderate = row['moderate']
        normal = row['normal']
        total_measured = row['total_measured']

        tooltips_data[name]['severe'] += (severe or 0)
        tooltips_data[name]['moderate'] += (moderate or 0)
        tooltips_data[name]['total'] += (valid or 0)
        tooltips_data[name]['normal'] += normal
        tooltips_data[name]['total_measured'] += total_measured

        value = ((moderate or 0) + (severe or 0)) / float(valid or 1)
        chart_data['blue'].append([
            name, value
        ])

    for sql_location in loc_children:
        if sql_location.name not in result_set:
            chart_data['blue'].append([sql_location.name, 0])

    chart_data['blue'] = sorted(chart_data['blue'])

    return {
        "tooltips_data": tooltips_data,
        "info": _((
            "Percentage of children between 6 - 60 months enrolled for ICDS services with "
            "weight-for-height below -3 standard deviations of the WHO Child Growth Standards median."
            "<br/><br/>"
            "Severe Acute Malnutrition (SAM) or wasting in children is a symptom of acute "
            "undernutrition usually as a consequence of insufficient food intake or a high "
            "incidence of infectious diseases."
        )),
        "chart_data": [
            {
                "values": chart_data['blue'],
                "key": "",
                "strokeWidth": 2,
                "classed": "dashed",
                "color": BLUE
            },
        ]
    }
