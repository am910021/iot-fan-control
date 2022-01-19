import gc, json
from yuri.http.share import BufferOverflowException, BUFFER_SIZE


class Html:

    @staticmethod
    def response(template_name, data={}, status=200, callback=None):
        gc.collect()
        return status, 'text/html', (lambda stream: Html.stream_file(stream, template_name, data)), callback

    @staticmethod
    def replace_template_params(line: str, data: dict) -> str:
        while True:
            bri = line.find('|}')
            if bri < 0:
                return line
            bli = line.find('{|', 0, bri)
            if bli < 0:
                return line
            name = line[bli + 2:bri]
            if data and name in data:
                line = line.replace('{|' + name + '|}', str(data[name]))
                continue
            else:
                line = line.replace('{|' + name + '|}', '')
                continue

    @staticmethod
    def stream_file(stream, file, data: dict):
        with open('/template/' + file, 'r') as f:
            while True:
                gc.collect()
                #print(gc.mem_free())
                line = f.readline(BUFFER_SIZE + 1)
                if len(line) > BUFFER_SIZE:
                    raise BufferOverflowException('The file single-line string exceeds {}.'.format(BUFFER_SIZE))
                if '|}' in line:
                    line = Html.replace_template_params(line, data)

                if line:
                    stream.write(line)
                else:
                    break


class Json:

    @staticmethod
    def response(data: dict, status=200, callback=None):
        return status, 'application/json', lambda stream: stream.write(json.dumps(data).encode('UTF-8')), callback
