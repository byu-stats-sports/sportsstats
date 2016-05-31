from datetime import datetime
from nba_py import league
import mysql.connector
import os.path
import logging
import sportsstats.utils

logger = logging.getLogger('sportsstats')


class Season:
    def __init__(self, start, end):
        self.start, self.end = self.determine_season(start, end)

    def determine_season(self, start, end):
        """Attempt to determine the season from `start` and `end`. Note: all we
        care about is the years.

        Args:
            start (datetime): The start date to initially base the season's
                              year off of.
            start (datetime): The season's end date.

        Returns:
            datetime: start: Any date in the starting year of the season
            datetime: end: The input end
        """
        if start.year == end.year:
            start = sportsstats.utils.add_years(start, -1)
        return (start, end)

    def __str__(self):
        return "{}-{}".format(self.start.strftime("%Y"),
                              self.end.strftime("%y"))


class DownloaderResult:
    def __init__(self, data, json, date_from, date_to):
        self.data = data
        self.json = json
        self.date_from = date_from
        self.date_to = date_to


class Downloader:
    """NBA Statistics HTTP Downloader.

    Attributes:
       start (datetime): The start date for the statistics to download.
       end (datetime): The end date for the statistics to download.
    """

    def __init__(self, start, end):
        # TODO bulletproof this...
        assert isinstance(start, datetime)
        self.start = start
        assert isinstance(end, datetime)
        self.end = end
        self.season = Season(start, end)

    def download(self, json=None):
        """Download NBA statistics from: http://stats.nba.com/tracking/.

        Returns:
            dict: The requested statistics
        """
        season = str(self.season)
        speed_stats = league.PlayerSpeedDistanceTracking(season=season,
                                                         date_from=self.start,
                                                         date_to=self.end)

        return DownloaderResult(data=speed_stats.overall(),
                                json=speed_stats.json,
                                date_from=self.start,
                                date_to=self.end)


class Database:
    def __init__(self, result):
        self.database = 'testJazz'
        self.table = 'nbaGameInjuries'
        self.config_files = [os.path.expanduser('~/.my.cnf')]

        self.connection, self.cursor = self._connect()

        self.data = result.data
        self.date = result.date_from

        # TODO: do not hardcode the table name
        self.create_table_stmt = """
            CREATE TABLE `nbaGameInjuries` (
              `first` varchar(45) NOT NULL,
              `last` varchar(45) NOT NULL,
              `abbr` varchar(45) DEFAULT NULL,
              `idno` varchar(2) NOT NULL,
              `season` year(4) DEFAULT NULL,
              `team` varchar(6) DEFAULT NULL,
              `ht` tinyint(4) DEFAULT NULL,
              `wt` smallint(6) DEFAULT NULL,
              `birthdate` date DEFAULT NULL,
              `pos` varchar(4) DEFAULT NULL,
              `date` date NOT NULL,
              `last_day_of_injury` date DEFAULT NULL,
              `mp` int(11) DEFAULT NULL,
              `season_mp_td` smallint(6) DEFAULT NULL,
              `season_g_td` tinyint(4) DEFAULT NULL,
              `mpg` int(11) DEFAULT NULL,
              `mp_since_pi` int(11) DEFAULT NULL,
              `g_since_pi` smallint(6) DEFAULT NULL,
              `age` decimal(4,2) DEFAULT NULL,
              `season_minutes` int(11) DEFAULT NULL,
              `g_missed` int(11) DEFAULT NULL,
              `m_missed` int(11) DEFAULT NULL,
              `main_body_part` varchar(45) DEFAULT NULL,
              `specific_body_part` varchar(45) DEFAULT NULL,
              `injury_type` varchar(45) DEFAULT NULL,
              `laterality` varchar(45) DEFAULT NULL,
              `days_out` smallint(6) DEFAULT NULL,
              `censor` varchar(45) DEFAULT NULL,
              `dist_miles` decimal(4,2) DEFAULT NULL,
              `avg_speed` decimal(3,2) DEFAULT NULL,
              `id` varchar(45) DEFAULT NULL,
              PRIMARY KEY (`first`,`last`,`idno`,`date`)
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
            """

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    # TODO: do not hardcode the columns to update
    def update(self):
        #  self._create_table()
        self._add_cols()
        # TODO: optimize this to reduce sql calls
        for player in self.data:
            #  print(player['PLAYER_NAME'])
            stmt = ("""UPDATE nbaGameInjuries
                         SET dist_miles = %s, avg_speed = %s
                        WHERE date = %s""")
            self._execute(stmt, (player['DIST_MILES'],
                                 player['AVG_SPEED'],
                                 self.date))

    # TODO: do not hardcode the columns to add
    def _add_cols(self):
        stmt = ("""ALTER TABLE nbaGameInjuries
                    ADD dist_miles decimal(4,2),
                    ADD avg_speed decimal(3,2)""")
        self._execute(stmt)

    def _create_table(self, stmt=None):
        if not stmt:
            stmt = self.create_table_stmt
        self._execute(stmt)

    def _connect(self, database=None, config_files=None):
        if not database:
            database = self.database
        if not config_files:
            config_files = self.config_files

        try:
            connection = mysql.connector.connect(option_files=config_files,
                                                 option_groups='client',
                                                 database=database)
            cursor = connection.cursor(dictionary=True)
            return (connection, cursor)
        except mysql.connector.Error as e:
            if e.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                logger.critical("Invalid user name or password")
            elif e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                logger.critical("Database does not exist")
            else:
                logger.exception(e)

    def _execute(self, stmt, **kwargs):
        try:
            logger.debug(stmt, **kwargs)
            self.cursor.execute(stmt, **kwargs)
        except mysql.connector.Error as e:
            if e.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
                logger.warning(e.msg)
            elif e.errno == mysql.connector.errorcode.ER_DUP_FIELDNAME:
                logger.warning(e.msg)
            else:
                logger.exception(e)
