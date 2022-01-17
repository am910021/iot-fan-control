import gc, json
from .share import BufferOverflowException


class Html:

    @staticmethod
    def response(template_name, params={}, status=200):
        gc.collect()
        return status, 'text/html', (lambda stream: Html.stream_file(stream, template_name, params))

    @staticmethod
    def replace_template_params(line: str, params: dict) -> str:
        while True:
            gc.collect()
            print(gc.mem_free())
            bri = line.find('|}')
            if bri < 0:
                return line
            bli = line.find('{|', 0, bri)
            if bli < 0:
                return line
            name = line[bli + 2:bri]
            if params and name in params:
                line = line.replace('{|' + name + '|}', str(params[name]))
                continue
            else:
                line = line.replace('{|' + name + '|}', '')
                continue


    @staticmethod
    def stream_file(stream, file, params: dict):
        print(gc.mem_free())
        _BUFF_SIZE = 256
        with open('/template/' + file, 'r') as f:
            while True:
                print(gc.mem_free())
                line = f.readline(_BUFF_SIZE + 1)
                if len(line) > _BUFF_SIZE:
                    raise BufferOverflowException('The read file buffer exceeds {}.'.format(_BUFF_SIZE))
                if '|}' in line:
                    line = Html.replace_template_params(line, params)

                if line:
                    stream.write(line)
                else:
                    break

class Json:

    @staticmethod
    def response(data: dict, status=200):
        return status, 'application/json', lambda stream: stream.write(json.dumps(data).encode('UTF-8'))
