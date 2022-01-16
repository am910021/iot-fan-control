import gc, json
from .share import BufferOverflowException


class Html:

    @staticmethod
    def response(template_name, params={}, status=200):
        gc.collect()
        f = open('/template/' + template_name, 'r')
        return status, 'text/html', (lambda stream: Html.stream_file(stream, f, params))

    @staticmethod
    def replace_template_params(line: str, params: dict) -> str:
        while True:
            bri = line.find('|}')
            if bri < 0:
                return line
            bli = line.find('{|', 0, bri)
            if bli < 0:
                return line
            name = line[bli + 2:bri]
            if name in params:
                line = line.replace('{|' + name + '|}', str(params[name]))
                continue
            else:
                line = line.replace('{|' + name + '|}', '')
                continue


    @staticmethod
    def stream_file(stream, f, params: dict):
        _BUFF_SIZE = 1024
        while True:
            line = f.readline(_BUFF_SIZE + 1)
            if len(line) > _BUFF_SIZE:
                raise BufferOverflowException('The read file buffer exceeds {}.'.format(_BUFF_SIZE))
            if '|}' in line and params:
                line = Html.replace_template_params(line, params)

            if line:
                stream.write(line)
            else:
                break

        f.close()


class Json:

    @staticmethod
    def response(data: dict, status=200):
        return status, 'application/json', lambda stream: stream.write(json.dumps(data).encode('UTF-8'))
