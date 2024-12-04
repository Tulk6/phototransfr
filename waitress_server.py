from waitress import serve
import phototransfr, socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(socket.gethostname())
print(hostname, ip_address)

serve(phototransfr.app, host=hostname, port=4664)