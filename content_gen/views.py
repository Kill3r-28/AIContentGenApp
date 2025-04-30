from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import status
from .serializers import PromptSerializer


class BusinessLogicView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected business logic endpoint"})


class PromptView(APIView):
    permission_classes = [IsAuthenticated]


    def get_prompt(self, request_type):

        file_name = {
            "mcq": "temp.txt",
            "ca_mcq": "ca_prompt_txt",
        }

        with open(settings.BASE_DIR / 'prompts' / file_name.get(request_type, 'no_file.txt')) as f:
            return f.read()


    def post(self, request):

        serializer = PromptSerializer(data=request.data)

        if serializer.is_valid():
            try:
                prompt = self.get_prompt(serializer.validated_data.get("process_name", None))
                return Response({"prompt": prompt}, status=status.HTTP_200_OK)
            except:
                return Response({"message": "Prompt file not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Invalid Data Passed"}, status=status.HTTP_400_BAD_REQUEST)
