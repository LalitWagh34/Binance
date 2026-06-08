"""
Binance Futures Testnet API client.
Handles authentication, request signing, and HTTP communication.
"""

import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests

from bot.logging_config import get_logger

logger = get_logger("client")

BASE_URL = "https://testnet.binancefuture.com"
TIMEOUT = 10  # seconds


class BinanceAPIError(Exception):
    """Raised when Binance API returns an error response."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Binance API Error {code}: {message}")


class BinanceClient:
    """
    Lightweight Binance Futures Testnet REST client.
    Supports signed (private) and unsigned (public) endpoints.
    """

    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise ValueError("API key and secret must not be empty.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })
        logger.info("BinanceClient initialized (testnet)")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sign(self, params: dict) -> dict:
        """Add timestamp and HMAC-SHA256 signature to params."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _handle_response(self, response: requests.Response) -> dict:
        """Parse response, raise BinanceAPIError on non-2xx or error body."""
        logger.debug("Response status: %s | body: %s", response.status_code, response.text[:500])
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            return {}

        if isinstance(data, dict) and "code" in data and data["code"] != 200:
            raise BinanceAPIError(code=data["code"], message=data.get("msg", "Unknown error"))

        response.raise_for_status()
        return data

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def get(self, endpoint: str, params: dict = None, signed: bool = False) -> dict:
        """Send a GET request."""
        params = params or {}
        if signed:
            params = self._sign(params)
        url = f"{BASE_URL}{endpoint}"
        logger.info("GET %s | params: %s", url, {k: v for k, v in params.items() if k != "signature"})
        try:
            response = self.session.get(url, params=params, timeout=TIMEOUT)
            return self._handle_response(response)
        except requests.exceptions.ConnectionError as e:
            logger.error("Network error on GET %s: %s", url, e)
            raise
        except requests.exceptions.Timeout:
            logger.error("Timeout on GET %s", url)
            raise

    def post(self, endpoint: str, params: dict = None, signed: bool = True) -> dict:
        """Send a POST request."""
        params = params or {}
        if signed:
            params = self._sign(params)
        url = f"{BASE_URL}{endpoint}"
        logger.info(
            "POST %s | params: %s",
            url,
            {k: v for k, v in params.items() if k != "signature"},
        )
        try:
            response = self.session.post(url, data=params, timeout=TIMEOUT)
            return self._handle_response(response)
        except requests.exceptions.ConnectionError as e:
            logger.error("Network error on POST %s: %s", url, e)
            raise
        except requests.exceptions.Timeout:
            logger.error("Timeout on POST %s", url)
            raise

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------

    def get_server_time(self) -> dict:
        """Fetch Binance server time (useful for connectivity check)."""
        return self.get("/fapi/v1/time")

    def get_exchange_info(self) -> dict:
        """Fetch exchange trading rules and symbol information."""
        return self.get("/fapi/v1/exchangeInfo")

    def get_account(self) -> dict:
        """Fetch account information (signed)."""
        return self.get("/fapi/v2/account", signed=True)