from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        
        # check if there are any errors

        response_data = {
            'data': {},
            'status': 500,
            'errors': [],
            'message': '',

        }
        if data.get('errors', None) is not None:
            response_data['errors'] = data.get('errors')
            response_data['data'] = {}

        if data.get('message', None) is not None:
            response_data['message'] = data.get('message')

        if data.get('status', None) is not None:
            response_data['status'] = data.get('status')

        if data.get('data', None) is not None:
            response_data['data'] = data.get('data')

       # call super to render the response
        response = super(CustomJSONRenderer, self).render(
            response_data, accepted_media_type, renderer_context
        )
        
        return response