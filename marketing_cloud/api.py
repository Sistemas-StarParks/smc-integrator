from collections.abc import Generator
import requests

class MarketingCloud:
    """Salesforce Marketing Cloud basic API connector.

    Links to a single Business Unit Application.
    """

    def __init__(self, credentials: dict[str, str], baseURL: str,  data_extensions: list[str], table: str|None=None):
        """
        Authentication data may be in the following format:

        ```py
        {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        ```

        :param str table: name of the table in the SQL database, defaults to None
        :param dict[str, str] credentials: dictionary with authentication data
        :param str baseURL: base URL for API requests
        :param list[str] baseURL: list of data extension names
        """
        self._table = table
        self._baseURL = '.'.join(['rest' if s=='auth' else s for s in baseURL.split('.')])
        self._authURL = baseURL
        self._auth = credentials
        self._data_extensions = data_extensions
        self._token = self._get_token()

    @property
    def client_id(self) -> str:
        return self._auth['client_id']

    @property
    def data_extensions(self):
        for de in self._data_extensions:
            yield de

    def set_credentials(self, credentials: dict[str, str]):
        self._auth = credentials

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

    def _has_token_expired(self, response: dict[str, any]) -> bool:
        return 'message' in response and response['message'] == 'Not Authorized'

    def _get_customobject(self, object: str, page=1) -> dict[str, any]:
        return self.get(f'data/v1/customobjectdata/key/{object}/rowset?$page={page}').json()

    def customobject_generator(self, object: str) -> Generator[list[dict]]:
        """Generator that yields each item inthe  customobjectdata endpoint

        :param str object: object name
        :yield dict: item from response['items']
        """
        self.refresh_token()
        response = self._get_customobject(object)

        yield response['items']

        while 'next' in response['links']:
            while self._has_token_expired(response):
                self.refresh_token()
                response = self.get(response['next'])
            for item in response['items']:
                yield item
