from flask_restful import Resource, reqparse
from flask_api import status

class EdgeConfigApi(Resource):
    def get(self):
        # Parse GET parameters
        parser = reqparse.RequestParser()
        parser.add_argument('iface', type=str)
        args = parser.parse_args(strict=True)
        iface = args['iface']

        # Internal function for the API request

        # return values
        return {'ifname':iface}, status.HTTP_200_OK

