from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from .models import FitnessBlog
from .serializers import FitnessBlogSerializer, SessionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .utils import send_booking_confirmation_email
from rest_framework import status
from .throttles import BookingThrottle


class FitnessBlogListView(ListAPIView):
    queryset = FitnessBlog.objects.order_by('pk')
    permission_classes = [IsAuthenticated]
    serializer_class = FitnessBlogSerializer

    def get_queryset(self):
        return FitnessBlog.objects.filter(status="PB").order_by("-created_at")


class FitnessBlogDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FitnessBlog.objects.filter(status="PB")
    serializer_class = FitnessBlogSerializer
    lookup_field = "slug"


class SessionCreateView(GenericAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [BookingThrottle]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            session = serializer.save()
            user = request.user
            send_booking_confirmation_email(user, session)
            return Response(
                {
                    "message": "Session successfully created. A confirmation email has been sent to you by our staff."
                },
                status=status.HTTP_201_CREATED,
            )
