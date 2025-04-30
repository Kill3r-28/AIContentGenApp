from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from .serializers import PromptSerializer, GptResponseSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class GptRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GptResponseSerializer(data=request.data)

        if serializer.is_valid():
            prompt = serializer.validated_data.get("prompt")
            if len(prompt.strip()) > 10:
                return Response({"message": self.get_response_from_gpt(prompt)}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid prompt data"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)

    def get_response_from_gpt(self, prompt):
        return "Generated Text"


class PromptView(APIView):
    permission_classes = [IsAuthenticated]

    def get_prompt(self, request_type):

        file_name = {
            "mcq": "temp.txt",
            "mcq_cpp": "mcq_cpp.txt",
            "ca_mcq": "ca_prompt_txt",
        }

        with open(settings.BASE_DIR / 'prompts' / file_name.get(request_type, 'no_file.txt')) as f:
            return f.read()

    def post(self, request):
        serializer = PromptSerializer(data=request.data)

        if serializer.is_valid():
            try:
                prompt = self.get_prompt(serializer.validated_data.get("process_name"))
                return Response({"prompt": prompt}, status=status.HTTP_200_OK)
            except:
                return Response({"error": "Prompt file not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid Data Passed"}, status=status.HTTP_400_BAD_REQUEST)

