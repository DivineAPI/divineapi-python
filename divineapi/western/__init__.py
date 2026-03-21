"""Western API - combines Natal, Synastry, Transit, Composite, PlanetReturns, Progressions, Prenatal."""

from ..client import BaseClient
from .composite import CompositeApi
from .natal import NatalApi
from .planet_returns import PlanetReturnsApi
from .prenatal import PrenatalApi
from .progressions import ProgressionsApi
from .synastry import SynastryApi
from .transit import TransitApi


class WesternApi:
    """Facade for all Western API sub-modules."""

    def __init__(self, client: BaseClient) -> None:
        self.natal = NatalApi(client)
        self.synastry = SynastryApi(client)
        self.transit = TransitApi(client)
        self.composite = CompositeApi(client)
        self.planet_returns = PlanetReturnsApi(client)
        self.progressions = ProgressionsApi(client)
        self.prenatal = PrenatalApi(client)
