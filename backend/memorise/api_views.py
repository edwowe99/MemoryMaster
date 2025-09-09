from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from .models import Work, Section, Unit, UserWorkProgress, UserUnitProgress, UserHistory, User
from .serializers import WorkDetailSerializer, WorkListSerializer, SectionSerializer, UnitSerializer, PracticeResultSerializer

class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return WorkListSerializer
        else:
            return WorkDetailSerializer


class SectionViewSet(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class UnitViewSet(ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class PracticeResultView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PracticeResultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        
        # 🔹 DEV ONLY: Hardcode a fallback user
        try:
            user = User.objects.get(username="admin")
        except User.DoesNotExist:
            # Create the dev user automatically if missing
            user = User.objects.create_user(username="admin", password="admin")

        try:
            work = Work.objects.get(id=data["work_id"])
        except Work.DoesNotExist:
            return Response({"error": "Work not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user_work_progress, _ = UserWorkProgress.objects.get_or_create(
            user=user,
            work=work
        )

        # Pre create UserUnitProgress for *all* units in the work
        all_units = Unit.objects.filter(work=work)
        existing_unit_ids = set(
            UserUnitProgress.objects.filter(user=user, unit__work=work).values_list("unit_id", flat=True)
        )
        missing_units = [u for u in all_units if u.id not in existing_unit_ids]

        UserUnitProgress.objects.bulk_create([
            UserUnitProgress(user=user, unit=unit, mastery_score=0.0)
            for unit in missing_units
        ])

        total_score = 0
        total_cap = 0
        total_units = len(data["units"])

        max_delta_mapping={"repetition": 5, "test": 10, "practice": 5}
        max_delta = max_delta_mapping.get(data['mode'])

        for unit_data in data["units"]:
            try:
                unit = Unit.objects.get(id=unit_data["unit_id"])
            except Unit.DoesNotExist:
                continue # skip missing units

            demonstrated_ability = unit_data['score'] * unit_data['cap']

            uup, _ = UserUnitProgress.objects.get_or_create(
                user=user,
                unit=unit,
                defaults={"mastery_score": 0.0}
            )

            delta = demonstrated_ability - uup.mastery_score
            bounded_delta = max(-max_delta, min(max_delta, delta))
            uup.mastery_score = max(0, min(1, uup.mastery_score + bounded_delta))

            uup.last_practiced_at = now()
            uup.times_practiced += 1
            uup.save()

            total_score += unit_data["score"]
            total_cap += unit_data["cap"]

        session_score = total_score / total_units if total_units > 0 else 0
        session_cap = total_cap / total_units if total_units > 0 else 0

        UserHistory.objects.create(
            user=user,
            work=work,
            mode=data["mode"],
            timestamp = now(),
            score=session_score,
            cap=session_cap
        )

        all_unit_progress = UserUnitProgress.objects.filter(user=user, unit__work=work)
        if all_unit_progress.exists():
            work_mastery = sum(u.mastery_score for u in all_unit_progress) / all_unit_progress.count()
        else:
            work_mastery = 0.0

        user_work_progress.mastery_score = work_mastery
        user_work_progress.last_practiced_at = now()
        user_work_progress.save()

        return Response({
            "message": "Practice results saved",
            "session_score": session_score,
            "work_mastery": work_mastery
        }, status=status.HTTP_200_OK)