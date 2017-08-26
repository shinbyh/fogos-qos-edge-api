from flask_restful import Resource, reqparse
from flask_api import status

class EdgeUtilApi(Resource):
    def get(self):
        # parse GET parameters
        parser = reqparse.RequestParser()
        parser.add_argument('service_type', type=str)
        args = parser.parse_args(strict=True)        
        service_type = args['service_type']

        # internal function for API
        
        # return values
        return {'result':service_type}, status.HTTP_200_OK

