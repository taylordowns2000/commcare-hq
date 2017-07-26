from django.core.management import BaseCommand

from corehq.apps.locations.models import SQLLocation


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('domain')

    def handle(self, domain, **options):
        for loc in SQLLocation.active_objects.filter(
            domain=domain,
            location_type__code__in=['pac', 'pcc', 'pcp', 'plc'],
        ):
            location_id = loc.location_id
            print 'processing location %s' % location_id
            uatbc_tu_id = loc.metadata.get('uatbc_tu_id')
            loc.metadata['nikshay_tu_id'] = UATBC_TO_NIKSHAY_TUS.get(uatbc_tu_id, '')
            loc.save()

UATBC_TO_NIKSHAY_TUS = {
    '165': '1',
    '166': '2',
    '167': '3',
    '1704': '1',
    '1705': '10',
    '1706': '1',
    '1707': '4',
    '1708': '2',
    '1709': '7',
    '1710': '6',
    '1711': '5',
    '1712': '9',
    '1714': '1',
    '1715': '11',
    '1716': '2',
    '1717': '9',
    '1719': '10',
    '1720': '1',
    '1722': '11',
    '1723': '7',
    '1724': '7',
    '1725': '8',
    '1726': '3',
    '1727': '11',
    '1728': '7',
    '1729': '1',
    '1730': '5',
    '1731': '10',
    '1732': '16',
    '1733': '5',
    '1736': '6',
    '1737': '14',
    '1741': '2',
    '1742': '2',
    '1743': '1',
    '1744': '7',
    '1746': '9',
    '1748': '11',
    '1749': '1',
    '1751': '9',
    '1752': '3',
    '1754': '2',
    '1755': '11',
    '1758': '4',
    '1759': '3',
    '1760': '1',
    '1762': '1',
    '1763': '4',
    '1764': '11',
    '1770': '7',
    '1771': '2',
    '1772': '6',
    '1773': '11',
    '1775': '10',
    '1776': '7',
    '1777': '9',
    '1779': '5',
    '1780': '5',
    '1782': '12',
    '1783': '3',
    '1788': '12',
    '1790': '4',
    '1791': '2',
    '1792': '3',
    '1793': '10',
    '1794': '9',
    '1795': '4',
    '1796': '15',
    '1797': '8',
    '1798': '2',
    '1799': '6',
    '1800': '8',
    '1801': '5',
    '1802': '13',
    '1803': '9',
    '1804': '4',
    '1805': '6',
    '1806': '7',
    '1807': '1',
    '1808': '1',
    '1809': '10',
    '1813': '1',
    '1814': '1',
    '1816': '12',
    '1817': '7',
    '1818': '1',
    '1820': '3',
    '1821': '8',
    '1822': '1',
    '1823': '4',
    '1825': '3',
    '1826': '2',
    '1827': '5',
    '1830': '2',
    '1831': '6',
    '1832': '12',
    '1833': '3',
    '1834': '2',
    '1836': '1',
    '1838': '7',
    '1842': '5',
    '1843': '6',
    '1846': '2',
    '1848': '7',
    '1849': '10',
    '1850': '2',
    '1851': '2',
    '1857': '8',
    '1860': '1',
    '1861': '9',
    '1862': '10',
    '1865': '8',
    '1867': '3',
    '1869': '15',
    '1873': '10',
    '1874': '3',
    '1875': '15',
    '1876': '7',
    '1877': '4',
    '1878': '5',
    '1881': '8',
    '1882': '1',
    '1884': '4',
    '1886': '10',
    '1889': '4',
    '1890': '13',
    '1892': '9',
    '1895': '10',
    '1896': '5',
    '1898': '1',
    '1900': '12',
    '1901': '10',
    '1902': '10',
    '1903': '8',
    '1905': '1',
    '1907': '4',
    '1908': '6',
    '1910': '8',
    '1911': '1',
    '1913': '11',
    '1917': '9',
    '1918': '3',
    '1921': '11',
    '1924': '1',
    '1926': '7',
    '1927': '11',
    '1929': '12',
    '1931': '4',
    '1933': '7',
    '1934': '6',
    '1935': '7',
    '1936': '8',
    '1937': '14',
    '1941': '4',
    '1945': '4',
    '1947': '7',
    '1948': '8',
    '1949': '4',
    '1950': '13',
    '1952': '13',
    '1954': '12',
    '1955': '4',
    '1956': '8',
    '1957': '14',
    '1958': '4',
    '1960': '3',
    '1961': '7',
    '1963': '8',
    '1965': '1',
    '1966': '8',
    '1967': '10',
    '1968': '1',
    '1970': '2',
    '1971': '2',
    '1972': '1',
    '1974': '3',
    '1977': '11',
    '1978': '6',
    '1980': '3',
    '1981': '2',
    '1983': '6',
    '1984': '6',
    '1985': '3',
    '1986': '1',
    '1987': '13',
    '1988': '5',
    '1989': '5',
    '1990': '7',
    '1991': '5',
    '1992': '4',
    '1993': '3',
    '1995': '9',
    '1996': '6',
    '1997': '4',
    '1998': '7',
    '1999': '5',
    '2000': '1',
    '2001': '4',
    '2002': '6',
    '2003': '3',
    '2004': '5',
    '2005': '5',
    '2006': '4',
    '2007': '5',
    '2008': '5',
    '2010': '3',
    '2011': '5',
    '2012': '3',
    '2015': '13',
    '2018': '6',
    '2019': '5',
    '2020': '12',
    '2021': '6',
    '2022': '15',
    '2023': '2',
    '2025': '5',
    '2026': '6',
    '2027': '4',
    '2029': '1',
    '2030': '7',
    '2031': '6',
    '2032': '6',
    '2033': '7',
    '2034': '8',
    '2035': '4',
    '2038': '4',
    '2039': '2',
    '2042': '5',
    '2043': '2',
    '2045': '7',
    '2046': '6',
    '2047': '10',
    '2048': '12',
    '2049': '10',
    '2052': '5',
    '2053': '1',
    '2055': '2',
    '2056': '3',
    '2057': '14',
    '2058': '3',
    '2059': '13',
    '2062': '6',
    '2063': '4',
    '2064': '9',
    '2065': '5',
    '2066': '7',
    '2067': '3',
    '2070': '9',
    '2072': '11',
    '2073': '8',
    '2076': '6',
    '2077': '16',
    '2078': '5',
    '2079': '1',
    '2080': '9',
    '2082': '13',
    '2084': '4',
    '2085': '1',
    '2086': '3',
    '2089': '14',
    '2095': '5',
    '2096': '2',
    '2097': '3',
    '2098': '7',
    '2099': '9',
    '2101': '9',
    '2104': '6',
    '2105': '8',
    '2108': '4',
    '2109': '12',
    '2110': '8',
    '2111': '2',
    '2112': '11',
    '2113': '3',
    '2114': '1',
    '2115': '2',
    '2116': '12',
    '2117': '8',
    '2118': '2',
    '2121': '10',
    '2122': '14',
    '2123': '13',
    '2255': '3',
    '23310': '11',
    '538': '4',
    '539': '5',
    '540': '6',
    '541': '7',
    '542': '8',
    '543': '9',
    '544': '10',
    '547': '1',
    '548': '2',
    '549': '3',
    '550': '4',
    '551': '5',
    '552': '6',
    '553': '7',
    '554': '8',
    '555': '9',
    '556': '10',
    '557': '11',
}
