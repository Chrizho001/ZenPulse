from rest_framework.throttling import SimpleRateThrottle

class BookingThrottle(SimpleRateThrottle):
    scope = 'booking'

    def get_cache_key(self, request, view):
        return self.get_ident(request)

