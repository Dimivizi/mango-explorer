# # ⚠ Warning
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# [🥭 Mango Markets](https://mango.markets/) support is available at:
#   [Docs](https://docs.mango.markets/)
#   [Discord](https://discord.gg/67jySBhxrg)
#   [Twitter](https://twitter.com/mangomarkets)
#   [Github](https://github.com/blockworks-foundation)
#   [Email](mailto:hello@blockworks.foundation)

from decimal import Decimal

from .token import Token


# # 🥭 LotSizeConverter class
#
class LotSizeConverter():
    def __init__(self, base: Token, base_lot_size: Decimal, quote: Token, quote_lot_size: Decimal):
        self.base: Token = base
        self.base_lot_size: Decimal = base_lot_size
        self.quote: Token = quote
        self.quote_lot_size: Decimal = quote_lot_size

    @property
    def tick_size(self) -> Decimal:
        return self.price_lots_to_value(Decimal(1))

    def price_lots_to_native(self, price_lots: Decimal) -> Decimal:
        return (price_lots * self.quote_lot_size) / self.base_lot_size

    def quantity_lots_to_native(self, quantity_lots: Decimal) -> Decimal:
        return self.base_lot_size * quantity_lots

    def price_lots_to_value(self, price_lots: Decimal) -> Decimal:
        native_to_ui: Decimal = 10 ** (self.base.decimals - self.quote.decimals)
        lots_to_native: Decimal = self.quote_lot_size / self.base_lot_size
        return (price_lots * lots_to_native) * native_to_ui

    def quantity_lots_to_value(self, quantity_lots: Decimal) -> Decimal:
        return (quantity_lots * self.base_lot_size) / (10 ** self.base.decimals)

    def round_base(self, quantity: Decimal) -> Decimal:
        base_factor: Decimal = 10 ** self.base.decimals
        rounded: int = round(quantity * base_factor)
        return Decimal(rounded) / base_factor

    def round_quote(self, price: Decimal) -> Decimal:
        quote_factor: Decimal = 10 ** self.base.decimals
        base_factor: Decimal = 10 ** self.base.decimals
        lots: Decimal = (price * quote_factor * self.base_lot_size) / (base_factor * self.quote_lot_size)
        rounded: int = round(lots)
        return Decimal(rounded) / self.quote_lot_size

    def __str__(self) -> str:
        return f"« 𝙻𝚘𝚝𝚂𝚒𝚣𝚎𝙲𝚘𝚗𝚟𝚎𝚛𝚝𝚎𝚛 [base lot size: {self.base_lot_size}, quote lot size: {self.quote_lot_size}] »"

    def __repr__(self) -> str:
        return f"{self}"


# # 🥭 NullLotSizeConverter class
#
class NullLotSizeConverter(LotSizeConverter):
    def __init__(self):
        super().__init__(None, Decimal(1), None, Decimal(1))

    def price_lots_to_native(self, price_lots: Decimal) -> Decimal:
        return price_lots

    def quantity_lots_to_native(self, quantity_lots: Decimal) -> Decimal:
        return quantity_lots

    def price_lots_to_value(self, price_lots: Decimal) -> Decimal:
        return price_lots

    def quantity_lots_to_value(self, quantity_lots: Decimal) -> Decimal:
        return quantity_lots

    def __str__(self) -> str:
        return "« 𝙽𝚞𝚕𝚕𝙻𝚘𝚝𝚂𝚒𝚣𝚎𝙲𝚘𝚗𝚟𝚎𝚛𝚝𝚎𝚛 »"


# # 🥭 RaisingLotSizeConverter class
#
class RaisingLotSizeConverter(LotSizeConverter):
    def __init__(self):
        super().__init__(None, Decimal(-1), None, Decimal(-1))

    def price_lots_to_native(self, price_lots: Decimal) -> Decimal:
        raise NotImplementedError(
            "RaisingLotSizeConverter.price_lots_to_native() is not implemented. RaisingLotSizeConverter is a stub used where no LotSizeConverter members should be called.")

    def quantity_lots_to_native(self, quantity_lots: Decimal) -> Decimal:
        raise NotImplementedError(
            "RaisingLotSizeConverter.quantity_lots_to_native() is not implemented. RaisingLotSizeConverter is a stub used where no LotSizeConverter members should be called.")

    def price_lots_to_value(self, price_lots: Decimal) -> Decimal:
        raise NotImplementedError(
            "RaisingLotSizeConverter.price_lots_to_value() is not implemented. RaisingLotSizeConverter is a stub used where no LotSizeConverter members should be called.")

    def quantity_lots_to_value(self, quantity_lots: Decimal) -> Decimal:
        raise NotImplementedError(
            "RaisingLotSizeConverter.quantity_lots_to_value() is not implemented. RaisingLotSizeConverter is a stub used where no LotSizeConverter members should be called.")

    def __str__(self) -> str:
        return "« 𝙽𝚞𝚕𝚕𝙻𝚘𝚝𝚂𝚒𝚣𝚎𝙲𝚘𝚗𝚟𝚎𝚛𝚝𝚎𝚛 »"
