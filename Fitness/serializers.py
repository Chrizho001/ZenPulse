from rest_framework import serializers
from .models import FitnessBlog, Session
from django.utils import timezone
from django.utils.text import slugify


class FitnessBlogSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)

    class Meta:
        model = FitnessBlog
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "image",
            "created_at",
            "author_name",
        ]
        read_only_fields = ["id", "author_name", "created_at"]

    def validate_image(self, value):
        if value:
            if not value.name.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                raise serializers.ValidationError(
                    "Only PNG, JPG, JPEG, and GIF files are allowed."
                )
            if value.size > 5 * 1024 * 1024:  # 5MB limit
                raise serializers.ValidationError("Image file too large (max 5MB).")
        return value

    def create(self, validated_data):
        # Set the author to the logged-in user (superuser)
        request = self.context.get("request")
        validated_data["author"] = request.user

        # Auto-generate slug if not provided
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data["title"])
        return super().create(validated_data)


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["description", "start_date", "start_time"]

    def validate(self, attrs):
        user = self.context["request"].user
        start_date = attrs.get("start_date")
        start_time = attrs.get("start_time")

        # Combine date and time for comparison
        start_datetime = timezone.datetime.combine(start_date, start_time)

        # Ensure the combined datetime is timezone-aware
        start_datetime = timezone.make_aware(
            start_datetime, timezone.get_current_timezone()
        )

        # Prevent double bookings
        user_overlap = Session.objects.filter(
            user=user, start_date=start_date, start_time=start_time
        ).exists()

        if user_overlap:
            raise serializers.ValidationError(
                "You have already booked a session at this time"
            )

        # Prevent past bookings
        if start_datetime < timezone.now():
            raise serializers.ValidationError("You cannot book a session in the past.")

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        validated_data["user"] = user
        return super().create(validated_data)
