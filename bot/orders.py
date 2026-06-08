"""
Order placement logic for Binance Futures Testnet.
Supports MARKET, LIMIT, and STOP_MARKET orders.
"""

from bot.client import BinanceClient
from bot.logging_config import get_logger
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()
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
    """Print a rich styled order request summary."""
    table = Table(box=box.ROUNDED, show_header=False, border_style="cyan")
    table.add_column("Field", style="cyan bold", width=15)
    table.add_column("Value", style="white bold")

    table.add_row("Symbol",     f"[yellow]{symbol}[/yellow]")
    table.add_row("Side",       f"[green]{side}[/green]" if side == "BUY" else f"[red]{side}[/red]")
    table.add_row("Type",       f"[magenta]{order_type}[/magenta]")
    table.add_row("Quantity",   f"[white]{quantity}[/white]")
    if price:
        table.add_row("Price", f"[white]{price}[/white]")
    if stop_price:
        table.add_row("Stop Price", f"[white]{stop_price}[/white]")

    console.print()
    console.print(Panel(table, title="[bold cyan]📋 ORDER REQUEST SUMMARY[/bold cyan]", border_style="cyan"))


def print_order_response(order: dict):
    """Print a rich styled order response."""
    status = order.get('status', '')
    status_color = "green" if status == "FILLED" else "yellow"

    table = Table(box=box.ROUNDED, show_header=False, border_style="green")
    table.add_column("Field", style="cyan bold", width=15)
    table.add_column("Value", style="white bold")

    table.add_row("Order ID",     f"[white]{order.get('orderId')}[/white]")
    table.add_row("Symbol",       f"[yellow]{order.get('symbol')}[/yellow]")
    table.add_row("Side",         f"[green]{order.get('side')}[/green]" if order.get('side') == "BUY" else f"[red]{order.get('side')}[/red]")
    table.add_row("Type",         f"[magenta]{order.get('type')}[/magenta]")
    table.add_row("Status",       f"[{status_color}]{status}[/{status_color}]")
    table.add_row("Price",        f"[white]{order.get('price')}[/white]")
    table.add_row("Avg Price",    f"[white]{order.get('avgPrice')}[/white]")
    table.add_row("Quantity",     f"[white]{order.get('origQty')}[/white]")
    table.add_row("Executed Qty", f"[white]{order.get('executedQty')}[/white]")
