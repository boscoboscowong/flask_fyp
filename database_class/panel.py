class Panel:

    def __init__(self, pid, name, region, location, latitude, longitude,
                 height, width, airtime_rate, pedestrain_flow, cap, img_no, path, used):
        self.pid = pid
        self.name = name
        self.region = region
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.height = height
        self.width = width
        self.airtime_rate = airtime_rate
        self.pedestrain_flow = pedestrain_flow
        self.cap = cap
        self.img_no = img_no
        self.path = path
        self.used = used