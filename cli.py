"""
CLI entry point for the Binance Futures Testnet Trading Bot.
Usage: python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01
"""

import argparse
import os
import sys
from rich.console import Console
from rich.panel import Panel
console = Console()

from dotenv import load_dotenv

from bot.client import BinanceClient, BinanceAPIError
from bot.logging_config import setup_logging, get_logger
from bot.orders import (
    place_market_order,
    place_limit_order,
    place_stop_market_order,
    print_order_summary,
    print_order_response,
)
from bot.validators import validate_order_inputs, ValidationError

# Load .env file if present
load_dotenv()

# Setup logging
setup_logging()
logger = get_logger("cli")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  Market BUY:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01

  Limit SELL:
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.01 --price 95000

  Stop Market BUY:
    python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --qty 0.01 --stop-price 85000
        """,
    )

    parser.add_argument("--symbol",     required=True, help="Trading pair e.g. BTCUSDT")
    parser.add_argument("--side",       required=True, help="BUY or SELL")
    parser.add_argument("--type",       required=True, dest="order_type", help="MARKET, LIMIT, or STOP_MARKET")
    parser.add_argument("--qty",        required=True, dest="quantity", help="Order quantity")
    parser.add_argument("--price",      required=False, default=None, help="Limit price (required for LIMIT)")
    parser.add_argument("--stop-price", required=False, default=None, dest="stop_price", help="Stop price (required for STOP_MARKET)")

    return parser.parse_args()


def get_credentials() -> tuple:
    """Load API credentials from environment variables."""
    api_key    = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        print("\n❌ ERROR: API credentials not found.")
        print("   Set BINANCE_API_KEY and BINANCE_API_SECRET in a .env file or environment.\n")
        print("   Example .env file:")
        print("     BINANCE_API_KEY=your_api_key_here")
        print("     BINANCE_API_SECRET=your_api_secret_here\n")
        sys.exit(1)

    return api_key, api_secret


def main():
    args = parse_args()

    # ── 1. Validate inputs ──────────────────────────────────────────
    try:
        validated = validate_order_inputs(
            symbol     = args.symbol,
            side       = args.side,
            order_type = args.order_type,
            quantity   = args.quantity,
            price      = args.price,
            stop_price = args.stop_price,
        )
    except ValidationError as e:
        console.print(Panel(f"[bold red]❌ Validation Error:[/bold red] {e}", border_style="red"))
        logger.error("Validation error: %s", e)
        sys.exit(1)

    # ── 2. Print order summary ──────────────────────────────────────
    print_order_summary(
        symbol     = validated["symbol"],
        side       = validated["side"],
        order_type = validated["order_type"],
        quantity   = validated["quantity"],
        price      = validated.get("price"),
        stop_price = validated.get("stop_price"),
    )

    # ── 3. Load credentials and init client ────────────────────────
    api_key, api_secret = get_credentials()
    try:
        client = BinanceClient(api_key=api_key, api_secret=api_secret)
    except ValueError as e:
        print(f"\n❌ Client Error: {e}\n")
        sys.exit(1)

    # ── 4. Place order ──────────────────────────────────────────────
    try:
        order_type = validated["order_type"]

        if order_type == "MARKET":
            order = place_market_order(
                client   = client,
                symbol   = validated["symbol"],
                side     = validated["side"],
                quantity = validated["quantity"],
            )

        elif order_type == "LIMIT":
            order = place_limit_order(
                client   = client,
                symbol   = validated["symbol"],
                side     = validated["side"],
                quantity = validated["quantity"],
                price    = validated["price"],
            )

        elif order_type == "STOP_MARKET":
            order = place_stop_market_order(
                client     = client,
                symbol     = validated["symbol"],
                side       = validated["side"],
                quantity   = validated["quantity"],
                stop_price = validated["stop_price"],
            )

        # ── 5. Print response ───────────────────────────────────────
        print_order_response(order)
        console.print(Panel("[bold green]✅ Order placed successfully![/bold green]", border_style="green"))
        logger.info("Order placed successfully: orderId=%s", order.get("orderId"))

    except BinanceAPIError as e:
        console.print(Panel(f"[bold red]❌ Binance API Error [{e.code}]:[/bold red] {e.message}", border_style="red"))
        logger.error("Binance API error: %s", e)
        sys.exit(1)

    except ConnectionError as e:
        console.print(Panel(f"[bold red]❌ Network Error:[/bold red] Could not connect to Binance Testnet.\n{e}", border_style="red"))
        logger.error("Network error: %s", e)
        sys.exit(1)

    except Exception as e:
        console.print(Panel(f"[bold red]❌ Unexpected Error:[/bold red] {e}", border_style="red"))

        logger.exception("Unexpected error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()