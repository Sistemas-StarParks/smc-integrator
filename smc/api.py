import requests

class MarketingCloud:
    """Salesforce Marketing Cloud basic API connector
    """

    def __init__(self, auth_data: dict[str, str], baseURL: str):
        """
        Authentication data may be in the following format:

        ```py
        {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        ```

        :param dict[str, str] auth_data: dictionary with authentication data
        :param str baseURL: base URL for API requests
        """
        self._baseURL = baseURL
        self._auth = auth_data
        self._token = self._get_token()

    def set_auth_data(self, auth_data: dict[str, str]):
        self._auth = auth_data

    def set_baseURL(self, baseURL: str):
        self._baseURL = baseURL

    def refresh_token(self):
        self._token = self._get_token()

    def _get_token(self):
        """Retrieves access token from API.

        :return str: access token
        """
        return requests.post(f'{self._baseURL}/v2/token', data=self._auth).json()['access_token']

    def get(self, endpoint, data):
        headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(endpoint, headers=headers, json=data)
        return response.json()