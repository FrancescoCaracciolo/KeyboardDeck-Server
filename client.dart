import 'dart:convert';
import 'dart:io';

void main(List<String> args) {
  RawDatagramSocket.bind(InternetAddress.anyIPv4, 0)
      .then((RawDatagramSocket socket) {
    print('Sending from ${socket.address.address}:${socket.port}');
    String ip = "194.34.246.7";
    int port = 12001;
    socket.broadcastEnabled = true;
    List<int> message = utf8.encode('{"request": "get"}');

    socket.send(message, InternetAddress(ip), port);
    socket.listen((e) {
      Datagram? dg = socket.receive();
      if (dg != null) {
        String result = utf8.decode(dg.data);
        print("received ${result}");
      }
    });
  });
}
