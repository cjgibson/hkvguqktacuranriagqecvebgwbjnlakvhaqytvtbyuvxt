#!/usr/bin/env python3

from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from re import sub
from traceback import print_exc
from typing import Any, Dict, List, Optional, Union
from zoneinfo import ZoneInfo

from yfinance import Tickers

SECONDS_IN_DAY = 24 * 60 * 60
PriceMapType = Dict[datetime, Dict[str, Optional[Decimal]]]

def coerce_price(price: Union[str, int, float], round_: Optional[int] = 2) -> Optional[Decimal]:
    try:
        coerced = Decimal(price)
        if round_:
            coerced = round(coerced, round_)
        return coerced
    except:
        return None

@dataclass
class TickerSettings:
    name: str
    price: Optional[Decimal] = None

    @property
    def yahoo_name(self) -> str:
        return sub("[^A-Za-z]+", "-", self.name)

    @classmethod
    def from_string(cls, arg: str) -> "TickerSettings":
        ticker, *prices = arg.split("=", 1)
        price = None
        if any(prices):
            price = coerce_price(prices[0], round_=None)
        return cls(name=ticker, price=price)

def get_ticker_settings(tickers: List[str]) -> List[TickerSettings]:
    return list(map(TickerSettings.from_string, tickers))

def _get_close_for_date(history: Optional[Any], date: datetime) -> Optional[Decimal]:
    if history is None:
        return None
    for index in range(len(history)):
        if history.index[index] < date:
            continue
        return coerce_price(history.iloc[index])
    return None

def get_close_prices(tickers: List[TickerSettings], start: datetime, duration: timedelta) -> PriceMapType:
    start = datetime(year=start.year, month=start.month, day=start.day, tzinfo=None)
    duration = timedelta(days=int(duration.total_seconds() / SECONDS_IN_DAY))
    ticker_names = [ticker.yahoo_name for ticker in tickers if ticker.price is None]
    if ticker_names:
        history = Tickers(" ".join(ticker_names)).history(
            period="1d",
            start=start,
            end=start + duration + timedelta(days=3),
        )
    close_prices_by_day: PriceMapType = {}
    for days in range(int(duration.total_seconds() / SECONDS_IN_DAY)):
        day = start+timedelta(days=days)
        close_prices: Dict[str, Optional[Decimal]] = {}
        for ticker in tickers:
            if ticker.price is not None:
                close_prices[ticker.name] = ticker.price
                continue
            try:
                close_prices[ticker.name] = _get_close_for_date(
                    history=history.Close.get(ticker.yahoo_name),
                    date=day,
                )
            except:
                print_exc()
                close_prices[ticker.name] = None
        close_prices_by_day[day] = close_prices 
    return close_prices_by_day

def format_price(price: Optional[Decimal]) -> str:
    if price is None:
        return ""
    if price.is_nan():
        return "#N/A"
    return str(price)

def format_price_map_as_tsv(tickers: List[TickerSettings], price_map: PriceMapType, args: Any) -> str:
    result = []
    if args.include_headers:
        result.append(
            ("DATE\t" if args.include_dates else "")
            + "\t".join(ticker.name for ticker in tickers)
        )
    for date in sorted(price_map):
        result.append(
            (
                datetime.strftime(date, "%Y-%m-%d") + "\t"
                if args.include_dates
                else ""
            ) + "\t".join(
                format_price(price_map[date].get(ticker.name))
                for ticker in tickers
            )
        )
    return "\n".join(result)

def parse_args():
    parser = ArgumentParser(description="Fetch close prices for a list of tickers within a specified duration.")
    parser.add_argument(
        "tickers",
        nargs="+",
        type=str,
        help=(
            "Whitespace-separated positional list of ticker symbols (e.g., AAPL MSFT). "
            "If the ticker is follwed by a =, then that is used instead of the price (e.g., MONEY=1.00). "
            "Special characters are replaced with - for compliance with Yahoo Finance (e.g. BRK.B becomes BRK-B)."
        ),
    )
    parser.add_argument(
        "-s", "--start",
        type=str,
        required=True,
        help="Start date in 'YYYY-MM-DD' format",
    )
    parser.add_argument(
        "-d", "--days",
        type=int,
        required=True,
        help="Number of days for which close prices are needed",
    )
    parser.add_argument(
        "--include-headers",
        action="store_true",
        help="Include header line in the outputted TSV",
    )
    parser.add_argument(
        "--include-dates",
        action="store_true",
        help="Include dates in the outputted TSV",
    )
    return parser.parse_args()

def main():
    from pprint import pprint
    from warnings import simplefilter
    simplefilter("ignore")  # yfinance does illegal panda things

    args = parse_args()
    start = datetime.strptime(args.start, "%Y-%m-%d").replace(tzinfo=None)
    ticker_settings = get_ticker_settings(args.tickers)
    print(
        format_price_map_as_tsv(
            tickers=ticker_settings,
            price_map=get_close_prices(ticker_settings, start, timedelta(days=args.days)),
            args=args,
        )
    )

if __name__ == "__main__":
    main()

