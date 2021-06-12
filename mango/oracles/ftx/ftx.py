# # ⚠ Warning
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# [🥭 Mango Markets](https://markets/) support is available at:
#   [Docs](https://docs.markets/)
#   [Discord](https://discord.gg/67jySBhxrg)
#   [Twitter](https://twitter.com/mangomarkets)
#   [Github](https://github.com/blockworks-foundation)
#   [Email](mailto:hello@blockworks.foundation)


import requests
import typing

from datetime import datetime
from decimal import Decimal

from ...context import Context
from ...market import Market
from ...oracle import Oracle, OracleProvider, OracleSource, Price


# # 🥭 FTX
#
# This file contains code specific to the [Ftx Network](https://pyth.network/).
#

def _ftx_get_from_url(url: str) -> typing.Dict:
    response = requests.get(url)
    response_values = response.json()
    if ("success" not in response_values) or (not response_values["success"]):
        raise Exception(f"Failed to get from FTX URL: {url} - {response_values}")
    return response_values["result"]


# # 🥭 FtxOracle class
#
# Implements the `Oracle` abstract base class specialised to the Ftx Network.
#


class FtxOracle(Oracle):
    def __init__(self, market: Market):
        name = f"Ftx Oracle for {market.symbol}"
        super().__init__(name, market)
        self.market: Market = market
        self.source: OracleSource = OracleSource("FTX", name, market)

    def fetch_price(self, context: Context) -> Price:
        result = _ftx_get_from_url(f"https://ftx.com/api/markets/{self.market.symbol}")
        bid = Decimal(result["bid"])
        ask = Decimal(result["ask"])
        price = Decimal(result["price"])

        return Price(self.source, datetime.now(), self.market, bid, price, ask)


# # 🥭 FtxOracleProvider class
#
# Implements the `OracleProvider` abstract base class specialised to the Ftx Network.
#

class FtxOracleProvider(OracleProvider):
    def __init__(self) -> None:
        super().__init__("Ftx Oracle Factory")

    def oracle_for_market(self, context: Context, market: Market) -> typing.Optional[Oracle]:
        return FtxOracle(market)

    def all_available_symbols(self, context: Context) -> typing.List[str]:
        result = _ftx_get_from_url("https://ftx.com/api/markets")
        symbols: typing.List[str] = []
        for market in result:
            symbols += [market["name"]]

        return symbols