def Main():
    for i in range(2, 254):
        ip_route = "ip route host 192.168.0.i" + "gateway 172.17.254.5" + "\n"
        xsh.Screen.Send(ip_route)
        xsh.Screen.Send('\r')
        xsh.Session.Sleep(500)