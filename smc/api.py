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
        self._baseURL = '.'.join(['rest' if s=='auth' else s for s in baseURL.split('.')])
        self._authURL = baseURL
        self._auth = auth_data
        self._token = self._get_token()

    @property
    def client_id(self) -> str:
        return self._auth['client_id']

    def set_auth_data(self, auth_data: dict[str, str]):
        self._auth = auth_data

    def set_baseURL(self, baseURL: str):
        self._baseURL = baseURL

    def refresh_token(self):
        self._token = self._get_token()

    def _get_token(self) -> str:
        """Retrieves access token from API.

        :return str: access token
        """
        return requests.post(f'{self._authURL}/v2/token', data=self._auth).json()['access_token']

    def _generate_endpoint_url(self, endpoint: str) -> str:
        """Generates full endpoint url from endpoint

        :param str endpoint: endpoint string (e.g. v2/contacts)
        :return str: full URL with baseURL + endpoint
        """
        return f'{self._baseURL}/{endpoint.strip('/')}'

    def get(self, endpoint: str) -> dict:
        """Basic GET Request using given endpoint

        Endpoint can either be in the format: `"contacts/v2/contacts"`

        Or with the baseURL already in it.

        :param str endpoint: endpoint
        :return dict: dictionary response
        """
        headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json'
        }

        if endpoint[:len(self._baseURL)] != self._baseURL:
            endpoint = self._generate_endpoint_url(endpoint)

        response = requests.get(endpoint, headers=headers)
        return response
