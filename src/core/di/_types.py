from collections.abc import Iterable
from typing import Any, TypeAlias

import aioinject

Providers: TypeAlias = Iterable[aioinject.Provider[Any]]
