"""
Trading-Technical-Indicators (tti) python library

File name: _fibonacci_retracement.py
    Implements the Fibonacci Retracement technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS


class FibonacciRetracement(TechnicalIndicator):
    """
    Fibonacci Retracement Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, fill_missing_values=True):

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
                It contains five columns, the resistance levels 'rl0', 'rl1',
                'rl2', 'rl3' and 'rl4'
        """

        total_max = input_data['Adj Close'].max()
        total_min = input_data['Adj Close'].min()

        max_min_difference = total_max - total_min

        retracement_levels = [total_max - c * max_min_difference for c in
                              [0.0, 0.236, 0.382, 0.618, 1.0]]

        fr = pd.DataFrame(index=input_data.index,
                          data=[[retracement_levels[i] for i in
                                 range(len(retracement_levels))]] * len(
                              input_data.index),
                          columns=['RL' + str(i) for i in
                                   range(len(retracement_levels))])

        return fr


        obv = pd.DataFrame(index=self._input_data.index, columns=['OBV'],
                           data=None, dtype='int64')

        obv.iat[0, 0] = 0
        for i in range(1, len(self._input_data.index)):

            # Today's close is greater than yesterday's close
            if self._input_data['close'].iat[i] > \
                    self._input_data['close'].iat[i - 1]:
                obv.iat[i, 0] = obv.iat[i - 1, 0] + \
                                self._input_data['volume'].iat[i]

            # Today's close is less than yesterday's close
            elif self._input_data['close'].iat[i] < \
                    self._input_data['close'].iat[i - 1]:
                obv.iat[i, 0] = obv.iat[i - 1, 0] - \
                                self._input_data['volume'].iat[i]

            # Today's close is equal the yesterday's close
            else:
                obv.iat[i, 0] = obv.iat[i - 1, 0]

        return obv

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

        # Moves from in RL to another in downward direction
        if self._input_data.iat[-2, 0] > self._ti_data.iat[-2, 3] and \
                self._input_data.iat[-1, 0] < self._ti_data.iat[-1, 3]:
            return ('Sell', TRADE_SIGNALS['Sell'])

        if self._input_data.iat[-2, 0] > self._ti_data.iat[-2, 2] and \
                self._input_data.iat[-1, 0] < self._ti_data.iat[-1, 2]:
            return ('Sell', TRADE_SIGNALS['Sell'])

        if self._input_data.iat[-2, 0] > self._ti_data.iat[-2, 1] and \
                self._input_data.iat[-1, 0] < self._ti_data.iat[-1, 1]:
            return ('Sell', TRADE_SIGNALS['Sell'])

        # Moves from in RL to another in the upward direction
        if self._input_data.iat[-2, 0] < self._ti_data.iat[-2, 3] and \
                self._input_data.iat[-1, 0] > self._ti_data.iat[-1, 3]:
            return ('Buy', TRADE_SIGNALS['Buy'])

        if self._input_data.iat[-2, 0] < self._ti_data.iat[-2, 2] and \
                self._input_data.iat[-1, 0] > self._ti_data.iat[-1, 2]:
            return ('Buy', TRADE_SIGNALS['Buy'])

        if self._input_data.iat[-2, 0] < self._ti_data.iat[-2, 1] and \
                self._input_data.iat[-1, 0] > self._ti_data.iat[-1, 1]:
            return ('Buy', TRADE_SIGNALS['Buy'])

        return ('Hold', TRADE_SIGNALS['Hold'])

        # Trading signals on warnings for breakout (upward or downward)
        # 3-days period is used for trend calculation

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 3:
            return TRADE_SIGNALS['hold']

        # Warning for a downward breakout
        if self._ti_data['OBV'].iat[-3] > self._ti_data['OBV'].iat[-2] > \
                self._ti_data['OBV'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Warning for a upward breakout
        elif self._ti_data['OBV'].iat[-3] < self._ti_data['OBV'].iat[-2] < \
                self._ti_data['OBV'].iat[-1]:
            return TRADE_SIGNALS['sell']

        else:
            return TRADE_SIGNALS['hold']
