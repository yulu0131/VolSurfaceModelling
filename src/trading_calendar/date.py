import datetime
from src.trading_calendar.china_holidays import _is_china_holidays

China_Holidays = _is_china_holidays


class Calendar:
    def __init__(self, holiday_rule=China_Holidays, other_holidays=None):
        """A class that provides methods for handling trading dates.

        Parameters
        ----------
        holiday_rule : callable
            A function that returns True if given a non-trading date.
            Default is CHINA_HOLIDAYS.
        other_holidays : list or None
            A list containing non-trading dates other than those
            determined by *holiday_rule*.
        """
        # holiday rule taken as is
        self._holiday_rule = holiday_rule
        if other_holidays is None:
            self.holiday_rule = holiday_rule
            self._other_holidays = []
        else:
            def _holiday_rule(date):
                return holiday_rule(date) or date in other_holidays
            self.holiday_rule = _holiday_rule
            self._other_holidays = other_holidays

    def is_trading(self, date: datetime.date):
        """Return if *date* trades.

        Parameters
        ----------
        date : datetime.date
        """
        return date.weekday() < 5 and not self.holiday_rule(date)

    def trading_days_between(self, start: datetime.date, end: datetime.date, endpoints: bool = True) -> list:
        """Return a list of trading days between *start* and *end*. Endpoints
        are counted only if they are trading.

        Parameters
        ----------
        start : datetime.date
        end : datetime.date
        endpoints : bool
            Whether to count *start* and *end* if they are trading dates.

        Returns
        -------
        list
            A list of trading dates.

        Note
        ----
        ``start`` and ``end`` are counted _only_ if they are trading dates.
        """
        if start > end:
            raise ValueError("start date must be prior to end date")
        if start == end:
            return [] if endpoints else [start]
        d_list = [start] if self.is_trading(start) and endpoints else []
        date = start
        while date < end + datetime.timedelta(days=-1 * (not endpoints)):
            date += datetime.timedelta(days=1)
            if self.is_trading(date):
                d_list.append(date)
        return d_list

    def num_trading_days_between(self, start: datetime.date, end: datetime.date, count_end: bool = True) -> int:
        """Return number of trading days between two dates. If these dates
        are identical, return 0. *count_end* controls whether to count the
        end date."""
        if start == end:
            return 0
        trading_dates = self.trading_days_between(start, end, True)
        return len(trading_dates) - count_end
