import requests
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class Flight:
    flightNumber: str
    originFull: str
    destinationFull: str
    departureTime: str
    price: float
    currency: str

@dataclass
class ReturnFlight:
    outbound: Flight
    inbound: Flight

class RyanairAPI:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.ryanair.com/api/booking/v4"
        # Настройка прокси для PythonAnywhere
        self.session.proxies = {
            'http': 'http://proxy.server:3128',
            'https': 'http://proxy.server:3128'
        }
        # Добавление необходимых заголовков
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        })

    def _format_date(self, date_str: str) -> str:
        """Convert YYYY-MM-DD to YYYY-MM"""
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m")

    def get_cheapest_flights(
        self,
        airport: str,
        destination_airport: str,
        date_from: str,
        date_to: str,
        max_price: float
    ) -> List[Flight]:
        """Search for one-way flights"""
        try:
            url = f"{self.base_url}/Availability"
            params = {
                "ADT": 1,  # 1 взрослый
                "CHD": 0,  # без детей
                "DateIn": "",  # только в одну сторону
                "DateOut": date_from,
                "Origin": airport,
                "Destination": destination_airport,
                "FlexDaysIn": 0,
                "FlexDaysOut": 0,
                "RoundTrip": "false",
                "ToUs": "AGREED"
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            flights = []
            for flight_data in data.get('flights', []):
                for fare in flight_data.get('fares', []):
                    price = fare.get('amount', 0)
                    if price <= max_price:
                        flight = Flight(
                            flightNumber=flight_data.get('flightNumber', ''),
                            originFull=flight_data.get('origin', ''),
                            destinationFull=flight_data.get('destination', ''),
                            departureTime=flight_data.get('time', [{}])[0].get('departure', ''),
                            price=price,
                            currency=fare.get('currency', 'EUR')
                        )
                        flights.append(flight)

            return flights
        except Exception as e:
            print(f"Error fetching flights: {e}")
            return []

    def get_cheapest_return_flights(
        self,
        source_airport: str,
        destination_airport: str,
        date_from: str,
        date_to: str,
        return_date_from: str,
        return_date_to: str,
        max_price: float
    ) -> List[ReturnFlight]:
        """Search for return flights"""
        try:
            url = f"{self.base_url}/Availability"
            params = {
                "ADT": 1,
                "CHD": 0,
                "DateIn": return_date_from,
                "DateOut": date_from,
                "Origin": source_airport,
                "Destination": destination_airport,
                "FlexDaysIn": 0,
                "FlexDaysOut": 0,
                "RoundTrip": "true",
                "ToUs": "AGREED"
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            return_flights = []
            outbound_flights = data.get('outbound', {}).get('flights', [])
            inbound_flights = data.get('inbound', {}).get('flights', [])

            for outbound in outbound_flights:
                for inbound in inbound_flights:
                    out_price = outbound.get('price', {}).get('amount', 0)
                    in_price = inbound.get('price', {}).get('amount', 0)
                    total_price = out_price + in_price

                    if total_price <= max_price:
                        return_flight = ReturnFlight(
                            outbound=Flight(
                                flightNumber=outbound.get('flightNumber', ''),
                                originFull=outbound.get('origin', ''),
                                destinationFull=outbound.get('destination', ''),
                                departureTime=outbound.get('time', [{}])[0].get('departure', ''),
                                price=out_price,
                                currency=outbound.get('price', {}).get('currency', 'EUR')
                            ),
                            inbound=Flight(
                                flightNumber=inbound.get('flightNumber', ''),
                                originFull=inbound.get('origin', ''),
                                destinationFull=inbound.get('destination', ''),
                                departureTime=inbound.get('time', [{}])[0].get('departure', ''),
                                price=in_price,
                                currency=inbound.get('price', {}).get('currency', 'EUR')
                            )
                        )
                        return_flights.append(return_flight)

            return return_flights
        except Exception as e:
            print(f"Error fetching return flights: {e}")
            return []