#!/usr/bin/env python

"""Download NBA statistics from: http://stats.nba.com/tracking/
"""

from collections import OrderedDict
import http.client as httplib
from contextlib import closing

try:
    # Python 3.0+
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib import urlencode


class DownloadError(Exception):
    pass


class Stats:
    """NBA Statistics

    Attributes:
       start (str): start date in the form `01/01/2016`
       end (str): end date in the form `01/01/2016`
       season (str): the season in the form `2015-16`
    """

    def __init__(self, start, end, season):
        self.start = start
        self.end = end
        self.season = season

    def download(self):
        """Download NBA statistics

        Returns:
            The requested statistics as JSON bytes
        """
        query_url = self.__build_query_url()
        try:
            with closing(self.__send_get_request(query_url)) as connection:
                return connection.getresponse().read().decode('utf-8')
        except httplib.HTTPException as e:
            raise DownloadError(e)

    def __send_get_request(self, query_url):
        """Send get request

        Returns:
            An HTTPConnection
        """
        connection = httplib.HTTPConnection('stats.nba.com')
        connection.request('GET', query_url)
        return connection

    def __build_query_url(self):
        """Format the query URl from parameters and a prefix

        Returns:
            The encoded URL
        """
        url_prefix = '/stats/leaguedashptstats?'
        params = OrderedDict([
            ('College', ''),
            ('Conference', ''),
            ('Country', ''),
            ('DateFrom', self.start),
            ('DateTo', self.end),
            ('Division', ''),
            ('DraftPick', ''),
            ('DraftYear', ''),
            ('GameScope', ''),
            ('Height', ''),
            ('LastNGames', '0'),
            ('LeagueID', '00'),
            ('Location', ''),
            ('Month', '0'),
            ('OpponentTeamID', '0'),
            ('Outcome', ''),
            ('PORound', '0'),
            ('PerMode', 'Totals'),
            ('PlayerExperience', ''),
            ('PlayerOrTeam', 'Player'),
            ('PlayerPosition', ''),
            ('PtMeasureType', 'SpeedDistance'),
            ('Season', self.season),
            ('SeasonSegment', ''),
            ('SeasonType', 'Regular Season'),
            ('StarterBench', ''),
            ('TeamID', '0'),
            ('VsConference', ''),
            ('VsDivision', ''),
            ('Weight', '')
        ])
        return url_prefix + urlencode(params)
