"""
Trading-Technical-Indicators (tti) python library

File name: _double_exponential_moving_average.py
    Implements the Double Exponential Moving Average technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class DoubleExponentialMovingAverage(TechnicalIndicator):
    """
    Double Exponential Moving Average Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 5): The past periods to be used for the
            calculation of the indicator.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=5, fill_missing_values=True):

        # Validate and store if needed, the input parameters
        if isinstance(period, int):
            if period > 0:
                self._period = period
            else:
                raise WrongValueForInputParameter(
                    period, 'period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(period), 'period', 'int')

        # Control is passing to the parent class
        super().__init__(calling_instance=self.__class__.__name__,
                         input_data=input_data,
                         fill_missing_values=fill_missing_values)

    def _calculateTi(self):
        """
        Calculates the technical indicator for the given input data. The input
        data are taken from an attribute of the parent class.

        Parameters:
            -

        Raises:
            -

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
                It contains one column, the 'dema'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Double Exponential Moving Average',
                                     self._period, len(self._input_data.index))

        dema = pd.DataFrame(index=self._input_data.index, columns=['dema'],
                            data=0, dtype='float64')

        # Exponential moving average of prices
        ema = self._input_data.ewm(
                span=self._period, min_periods=self._period, adjust=False,
                axis=0).mean()

        # Exponential moving average of the exponential moving average
        ema_of_ema = ema.ewm(
            span=self._period, min_periods=self._period, adjust=False,
            axis=0).mean()

        dema['dema'] = (2 * ema) - ema_of_ema

        return dema.round(4)

    def getTiSignal(self):
        """
        Calculates and returns the signal of the technical indicator. The
        Technical Indicator data are taken from an attribute of the parent
        class.

        Parameters:
            -

        Raises:
            -

        Returns:
            tuple (string, integer): The Trading signal. Possible values are
                ('hold', 0), ('buy', -1), ('sell', 1). See TRADE_SIGNALS
                constant in the tti.utils package, constants.py module.
        """

        # Close price is below Moving Average
        if self._input_data['close'].iat[-1] < self._ti_data['dema'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Close price is above Moving Average
        if self._input_data['close'].iat[-1] > self._ti_data['dema'].iat[-1]:
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']