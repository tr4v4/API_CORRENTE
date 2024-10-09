import requests

# Constants
REQUEST_URL = "https://core.corrente.playmoove.com/api/v1/fleet/search"
BOOKING_URL = "https://core.corrente.playmoove.com/api/v1/reservation/book"


class GetZoe:
    def __init__(self, lat, long, dist_tol, token):
        self.lat = lat
        self.long = long
        self.dist_tol = dist_tol
        self.token = token

    def _build_request(self):
        self.params = {"latitude": self.lat, "longitude": self.long}
        self.headers = {'Authorization': f"Bearer {self.token}"}
 
    def _send_request(self):
        self.vehicles = requests.get(REQUEST_URL,
                                    params=self.params,
                                    headers=self.headers)
    
    def get_zoes(self):
        self._build_request()
        self._send_request()
        zoes = []
        for vehicle in self.vehicles.json():
            id = vehicle["id"]
            model = vehicle["vehicle"]["model"]
            plate = vehicle["vehicle"]["plate"]
            distance = vehicle["distance"]
            address = vehicle["address"]
            position = vehicle["position"]
            range = vehicle["vehicle"]["range"]
            if model == "ZOE" and distance <= self.dist_tol:
                zoe = {"id": id,
                    "model": model,
                    "plate": plate,
                    "distance": distance,
                    "address": address,
                    "position": position,
                    "range": range}
                zoes.append(zoe)
        return zoes


class BookZoe:
    def __init__(self, plate, token):
        self.plate = plate
        self.token = token
    
    def _build_request(self):
        self.book = {
            "start": "",
            "end": "",
            "memo": "",
            "packet_id": None,
            "plate": self.plate
        }
        self.headers = {'Authorization': f"Bearer {self.token}"}
    
    def book_zoe(self):
        self._build_request()
        response = requests.post(BOOKING_URL,
                                json=self.book,
                                headers=self.headers)
        return response.status_code

