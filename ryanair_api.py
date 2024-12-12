import requests
from datetime import datetime
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        self.base_url = "https://services-api.ryanair.com/farfnd/3/oneWayFares"
        # Настройка прокси для PythonAnywhere
        self.session.proxies = {
            'http': 'http://proxy.server:3128',
            'https': 'http://proxy.server:3128'
        }
        # Добавление необходимых заголовков
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.ryanair.com',
            'Referer': 'https://www.ryanair.com/',
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
            # Новый формат URL и параметров
            url = f"{self.base_url}"
            params = {
                "departureAirportIataCode": airport,
                "arrivalAirportIataCode": destination_airport,
                "outboundDepartureDateFrom": date_from,
                "outboundDepartureDateTo": date_to,
                "currency": "EUR"
            }
            
            logger.info(f"Sending request to {url} with params: {params}")
            response = self.session.get(url, params=params)
            logger.info(f"Response status code: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"Error response: {response.text}")
                return []
                
            data = response.json()
            logger.info(f"Received data: {data}")

            flights = []
            for fare in data.get('fares', []):
                price = fare.get('price', {}).get('value', 0)
                if price <= max_price:
                    flight = Flight(
                        flightNumber=fare.get('flightNumber', ''),
                        originFull=fare.get('outbound', {}).get('departureAirport', {}).get('name', ''),
                        destinationFull=fare.get('outbound', {}).get('arrivalAirport', {}).get('name', ''),
                        departureTime=fare.get('outbound', {}).get('departureTime', ''),
                        price=price,
                        currency='EUR'
                    )
                    flights.append(flight)

            logger.info(f"Found {len(flights)} flights within price range")
            return flights
        except Exception as e:
            logger.error(f"Error fetching flights: {e}", exc_info=True)
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
            # URL для поиска туда-обратно
            url = f"{self.base_url}/roundTripFares"
            params = {
                "departureAirportIataCode": source_airport,
                "arrivalAirportIataCode": destination_airport,
                "outboundDepartureDateFrom": date_from,
                "outboundDepartureDateTo": date_to,
                "inboundDepartureDateFrom": return_date_from,
                "inboundDepartureDateTo": return_date_to,
                "currency": "EUR"
            }
            
            logger.info(f"Sending return flight request to {url} with params: {params}")
            response = self.session.get(url, params=params)
            logger.info(f"Response status code: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"Error response: {response.text}")
                return []
                
            data = response.json()
            logger.info(f"Received return flight data: {data}")

            return_flights = []
            for fare in data.get('fares', []):
                outbound = fare.get('outbound', {})
                inbound = fare.get('inbound', {})
                total_price = (outbound.get('price', {}).get('value', 0) + 
                             inbound.get('price', {}).get('value', 0))

                if total_price <= max_price:
                    return_flight = ReturnFlight(
                        outbound=Flight(
                            flightNumber=outbound.get('flightNumber', ''),
                            originFull=outbound.get('departureAirport', {}).get('name', ''),
                            destinationFull=outbound.get('arrivalAirport', {}).get('name', ''),
                            departureTime=outbound.get('departureTime', ''),
                            price=outbound.get('price', {}).get('value', 0),
                            currency='EUR'
                        ),
                        inbound=Flight(
                            flightNumber=inbound.get('flightNumber', ''),
                            originFull=inbound.get('departureAirport', {}).get('name', ''),
                            destinationFull=inbound.get('arrivalAirport', {}).get('name', ''),
                            departureTime=inbound.get('departureTime', ''),
                            price=inbound.get('price', {}).get('value', 0),
                            currency='EUR'
                        )
                    )
                    return_flights.append(return_flight)

            logger.info(f"Found {len(return_flights)} return flights within price range")
            return return_flights
        except Exception as e:
            logger.error(f"Error fetching return flights: {e}", exc_info=True)
            return []