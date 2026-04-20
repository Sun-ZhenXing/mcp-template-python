from typing import Iterator

import pytest
from blockbuster import BlockBuster, blockbuster_ctx


@pytest.fixture(autouse=True)
def _no_blocking_in_async(
    request: pytest.FixtureRequest,
) -> Iterator[BlockBuster | None]:
    """Guard all async tests against accidental blocking I/O calls.

    Uses blockbuster to raise ``BlockingError`` whenever a known blocking
    function (e.g. ``open``, ``time.sleep``, socket I/O) is invoked inside
    an asyncio event loop, which would stall the loop and hide bugs.

    The guard is skipped for synchronous tests so as not to affect them.
    """
    if request.node.get_closest_marker("asyncio") is None:
        # Not an async test — nothing to guard.
        yield
        return

    with blockbuster_ctx():
        yield
