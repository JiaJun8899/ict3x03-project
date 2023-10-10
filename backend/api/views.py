from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services import OrganizerAdminService


class UpdateOrganizerStatus(APIView):
    def put(self, request):
        success = OrganizerAdminService.updateOrganizer(request.data["user"],request.data["validOrganisation"])
        if success:
            return Response({"status": "success", "message": "Organizer status updated successfully."})
        else:
            return Response({"status": "error", "message": "Failed to update organizer status."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllOrganizers(APIView):
    def get(self, request):
        organizers = OrganizerAdminService.getAllOrganizers()

        if organizers is not False:
            # Assuming that the returned organizers is a QuerySet or list of Organizer instances
            serializer = OrganizerSerializer(organizers, many=True)
            return Response({"status": status.HTTP_200_OK, "data": serializer.data})
        else:
            return Response({"status": "error", "message": "Failed to retrieve organizers."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

