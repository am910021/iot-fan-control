import json
from ..share import BadRequestException, NotFoundException, get_relative_path
from yuri.logger import logger


class LogicProcess:
    def __init__(self, handlers):
        self._handlers = handlers

    def handle_request(self, http_request):
        relative_path = get_relative_path(http_request)
        path_part, url_params = self.extract_query(relative_path)
        components = path_part.strip('/').split('/')
        prefix, handler, context = self.find_handler(components)
        if handler:
            body = None
            headers = http_request['headers']
            if 'body' in http_request and 'content-type' in headers:
                if headers['content-type'] == "application/json":
                    try:
                        body = json.loads(http_request['body'])
                    except Exception as e:
                        raise BadRequestException("Failed to load JSON: {}".format(e))
                elif headers['content-type'] == "application/x-www-form-urlencoded":
                    a,body = self.extract_query('?'+http_request['body'].decode('utf8'))

            verb = http_request['verb']
            api_request = {
                'prefix': prefix,
                'context': context,
                'url_params': url_params,
                'body': body,
                'http': http_request
            }
            code, content_type, response, callback = 500, "text/html", None, None
            logger.info("ACCESS {} {}".format(http_request['remote'], http_request['path']))
            if verb == 'get':
                code, content_type, response, callback = handler.get(api_request)
            elif verb == 'put':
                code, content_type, response, callback = handler.put(api_request)
            elif verb == 'post':
                code, content_type, response, callback = handler.post(api_request)
            elif verb == 'delete':
                code, content_type, response, callback = handler.delete(api_request)
            else:
                # TODO add support for more verbs!
                error_message = "Unsupported verb: {}".format(verb)
                raise BadRequestException(error_message)
        else:
            error_message = "No handler found for components {}".format(components)
            raise NotFoundException(error_message)

        ret = {
            'code': code,
            'headers': {
                # 'content-length': len(data) if data else 0
                'content_type': content_type
            },
            'body': response,
            'callback': callback
        }
        return ret

    #
    # Internal operations
    #

    def find_handler(self, components):
        for prefix, handler in self._handlers:
            prefix_len = len(prefix)
            if prefix == components[:prefix_len]:
                return prefix, handler, components[prefix_len:]
        return None, None, None

    @staticmethod
    def extract_query(path):
        components = path.split("?")
        if len(components) == 1:
            return path, None
        elif len(components) > 2:
            raise BadRequestException("Malformed path: {}".format(path))
        path_part = components[0]
        query_part = components[1]
        qparam_components = query_part.split("&")
        url_params = {}
        for qparam_component in qparam_components:
            if qparam_component.strip() == '':
                continue
            qparam = qparam_component.split("=")
            if len(qparam) != 2 or not qparam[0]:
                raise BadRequestException("Invalid query parameter: {}".format(qparam_component))
            url_params[qparam[0]] = qparam[1]
        return path_part, url_params
