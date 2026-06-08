"""
Order placement logic for Binance Futures Testnet.
Supports MARKET, LIMIT, and STOP_MARKET orders.
"""

from bot.client import BinanceClient
from bot.logging_config import get_logger

logger = get_logger("orders")

ORDER_ENDPOINT = "/api/v3/order"


def _parse_order_response(response: dict) -> dict:
    """
    Extract the most useful fields from a raw order response.
    """
    return {
        "orderId":      response.get("orderId"),
        "symbol":       response.get("symbol"),
        "side":         response.get("side"),
        "type":         response.get("type"),
        "status":       response.get("status"),
        "price":        response.get("price"),
        "avgPrice":     response.get("avgPrice"),
        "origQty":      response.get("origQty"),
        "executedQty":  response.get("executedQty"),
        "timeInForce":  response.get("timeInForce"),
        "updateTime":   response.get("updateTime"),
    }


def place_market_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: float,
) -> dict:
    """
    Place a MARKET order on Binance Futures Testnet.

    Args:
        client:   Authenticated BinanceClient instance.
        symbol:   Trading pair e.g. BTCUSDT.
        side:     BUY or SELL.
        quantity: Amount to trade.

    Returns:
        Parsed order response dict.
    """
    params = {
        "symbol":   symbol,
        "side":     side,
        "type":     "MARKET",
        "quantity": quantity,
    }
    logger.info("Placing MARKET order: %s", params)
    try:
        response = client.post(ORDER_ENDPOINT, params=params)
        parsed = _parse_order_response(response)
        logger.info("MARKET order success: %s", parsed)
        return parsed
    except Exception as e:
        logger.error("MARKET order failed: %s", e)
        raise


def place_limit_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    time_in_force: str = "GTC",
) -> dict:
    """
    Place a LIMIT order on Binance Futures Testnet.

    Args:
        client:        Authenticated BinanceClient instance.
        symbol:        Trading pair e.g. BTCUSDT.
        side:          BUY or SELL.
        quantity:      Amount to trade.
        price:         Limit price.
        time_in_force: GTC (default), IOC, or FOK.

    Returns:
        Parsed order response dict.
    """
    params = {
        "symbol":      symbol,
        "side":        side,
        "type":        "LIMIT",
        "quantity":    quantity,
        "price":       price,
        "timeInForce": time_in_force,
    }
    logger.info("Placing LIMIT order: %s", params)
    try:
        response = client.post(ORDER_ENDPOINT, params=params)
        parsed = _parse_order_response(response)
        logger.info("LIMIT order success: %s", parsed)
        return parsed
    except Exception as e:
        logger.error("LIMIT order failed: %s", e)
        raise


def place_stop_market_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: float,
    stop_price: float,
) -> dict:
    """
    Place a STOP_MARKET order on Binance Futures Testnet.

    Args:
        client:     Authenticated BinanceClient instance.
        symbol:     Trading pair e.g. BTCUSDT.
        side:       BUY or SELL.
        quantity:   Amount to trade.
        stop_price: Trigger price for the stop order.

    Returns:
        Parsed order response dict.
    """
    params = {
        "symbol":    symbol,
        "side":      side,
        "type":      "STOP_LOSS_LIMIT",
        "quantity":  quantity,
        "stopPrice": stop_price,
        "price":       stop_price,  # limit price = stop price
        "timeInForce": "GTC",
    }
    logger.info("Placing STOP_LOSS_LIMIT order: %s", params)
    try:
        response = client.post(ORDER_ENDPOINT, params=params)
        parsed = _parse_order_response(response)
        logger.info("STOP_LOSS_LIMIT order success : %s", parsed)
        return parsed
    except Exception as e:
        logger.error("STOP_LOSS_LIMIT order failed: %s", e)
        raise


def print_order_summary(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    """Print a clean order request summary to the console."""
    print("\n" + "=" * 50)
    print("         ORDER REQUEST SUMMARY")
    print("=" * 50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    if stop_price:
        print(f"  Stop Price : {stop_price}")
    print("=" * 50)


def print_order_response(order: dict):
    """Print a clean order response to the console."""
    print("\n" + "=" * 50)
    print("         ORDER RESPONSE")
    print("=" * 50)
    print(f"  Order ID     : {order.get('orderId')}")
    print(f"  Symbol       : {order.get('symbol')}")
    print(f"  Side         : {order.get('side')}")
    print(f"  Type         : {order.get('type')}")
    print(f"  Status       : {order.get('status')}")
    print(f"  Price        : {order.get('price')}")
    print(f"  Avg Price    : {order.get('avgPrice')}")
    print(f"  Quantity     : {order.get('origQty')}")
    print(f"  Executed Qty : {order.get('executedQty')}")
    print("=" * 50)