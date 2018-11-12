import json

from main import INIT_ENVIRONMENT, build_strategy, load_from_file
from environment import Environment
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import unquote

TCPServer.allow_reuse_address = True

class MyRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        MOVE_PREFIX = '/move/'

        if self.path == '/init':
            environment = Environment(INIT_ENVIRONMENT)
            # return self.__send_json({'env' : environment.get(), 'actor' : environment.get_actor_state()})
            return self.__send_json(environment.get())

        elif self.path == '/':
            self.path = '/web/index.html'

        elif self.path.startswith(MOVE_PREFIX):
            env = json.loads(unquote(self.path[len(MOVE_PREFIX):]))
            env_text = '\n'.join(map(lambda r: ' '.join(r), env))
            environment = Environment(env_text)

            state = environment.get_actor_state()

            strategy = build_strategy()
            load_from_file(strategy)
            action = strategy.next_action(state, 0)
            environment.perform_action(action)

            response = {
                'env' : environment.get(),
                'terminal' : environment.actor_in_terminal_state,
                'stats' : {
                    'ε' : strategy.ε,
                    'scores' : strategy.scores,
                    'episode' : strategy.episode
                }
            }

            return self.__send_json(response)

        return SimpleHTTPRequestHandler.do_GET(self)

    def __send_json(self, obj):
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(obj), 'utf-8'))


Handler = MyRequestHandler
server = TCPServer(('0.0.0.0', 8080), Handler)

server.serve_forever()