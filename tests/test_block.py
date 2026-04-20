import time

import pytest
from blockbuster import BlockingError


async def test_time_sleep() -> None:
    with pytest.raises(BlockingError):
        time.sleep(0.1)  # This should raise a BlockingError
