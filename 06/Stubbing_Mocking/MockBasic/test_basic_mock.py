from unittest.mock import MagicMock, patch

from MockBasic.alarm import Alarm

thing = Alarm()
thing.check = MagicMock(return_value=3)
print(thing.check(3, 4, 5, key='value'))

thing.check.assert_called_with(3, 4, 5, key='value')

