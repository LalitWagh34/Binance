"""
Input validation for trading bot CLI arguments.
Validates symbol, side, order type, quantity, and price.
"""

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


class ValidationError(Exception):
    """Raised when user input fails validation."""
    pass


def validate_symbol(symbol: str) -> str:
    """
    Symbol must be non-empty and uppercase (e.g. BTCUSDT).
    """
    if not symbol or not symbol.strip():
        raise ValidationError("Symbol cannot be empty.")
    symbol = symbol.strip().upper()
    if len(symbol) < 3:
        raise ValidationError(f"Invalid symbol: '{symbol}'. Example: BTCUSDT")
    return symbol


def validate_side(side: str) -> str:
    """
    Side must be BUY or SELL (case-insensitive).
    """
    if not side:
        raise ValidationError("Side cannot be empty.")
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(
            f"Invalid side: '{side}'. Must be one of: {', '.join(VALID_SIDES)}"
        )
    return side


def validate_order_type(order_type: str) -> str:
    """
    Order type must be MARKET, LIMIT, or STOP_MARKET.
    """
    if not order_type:
        raise ValidationError("Order type cannot be empty.")
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type: '{order_type}'. Must be one of: {', '.join(VALID_ORDER_TYPES)}"
        )
    return order_type


def validate_quantity(quantity: str) -> float:
    """
    Quantity must be a positive number.
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid quantity: '{quantity}'. Must be a number.")
    if qty <= 0:
        raise ValidationError(f"Quantity must be greater than 0. Got: {qty}")
    return qty


def validate_price(price: str) -> float:
    """
    Price must be a positive number.
    """
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid price: '{price}'. Must be a number.")
    if p <= 0:
        raise ValidationError(f"Price must be greater than 0. Got: {p}")
    return p


def validate_order_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str = None,
    stop_price: str = None,
) -> dict:
    """
    Validate all order inputs together.
    Returns a clean dict of validated values.
    """
    result = {
        "symbol":     validate_symbol(symbol),
        "side":       validate_side(side),
        "order_type": validate_order_type(order_type),
        "quantity":   validate_quantity(quantity),
    }

    # LIMIT requires a price
    if result["order_type"] == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        result["price"] = validate_price(price)

    # STOP_MARKET requires a stop price
    if result["order_type"] == "STOP_MARKET":
        if stop_price is None:
            raise ValidationError("Stop price (--stop-price) is required for STOP_MARKET orders.")
        result["stop_price"] = validate_price(stop_price)

    return result