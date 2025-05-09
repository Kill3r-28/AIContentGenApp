from openai import OpenAI
from django.conf import settings
from rest_framework import status
from .models import UserRequestTrack
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PromptSerializer, GptResponseSerializer


class GptRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GptResponseSerializer(data=request.data)

        if serializer.is_valid():
            prompt = serializer.validated_data.get("prompt")
            if len(prompt.strip()) > 10:
                response = self.get_response_from_gpt(prompt)

                if response.get("finish_reason", "") != 'stop':
                    return Response({"error": "GPT was unable to complete the request due to an internal error or because the output exceeded the maximum token limit."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                self.save_data(request.user, serializer.validated_data, response)

                return Response({
                    "message": response.get("message"),
                    "input_token": response.get("input_token"),
                    "output_token": response.get("output_token"),
                    "total_token": response.get("total_token"),
                                 }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid prompt data"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)

    def save_data(self, user, request_data, gpt_response_data):

        user_data = UserRequestTrack(
            user=user,
            difficulty=request_data.get("difficulty"),
            question_type=request_data.get("question_type"),
            topic=request_data.get("topic"),
            subtopic=request_data.get("subtopic"),
            question_count=request_data.get("number_of_question"),
            input_token=gpt_response_data.get("input_token"),
            output_token=gpt_response_data.get("output_token")
        )
        user_data.save()

    def get_response_from_gpt(self, prompt):

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = {
            "message": completion.choices[0].message.content,
            "input_token": completion.usage.prompt_tokens,
            "output_token": completion.usage.completion_tokens,
            "total_token": completion.usage.total_tokens,
            "finish_reason": completion.choices[0].finish_reason
        }

        return result

class PromptView(APIView):
    permission_classes = [IsAuthenticated]

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

    def get_prompt(self, request_type):

        file_name = {
            "mcq":               "temp.txt",
            "ca_mcq_cpp":        "ca_mcq_cpp.txt",
            "ca_mcq_python":     "ca_mcq_python.txt",
            "ca_mcq_java":       "ca_mcq_java.txt",
            "ca_mcq_c":          "ca_mcq_c.txt",
            "ca_mcq_javascript": "ca_mcq_javascript.txt",
            "ca_mcq_sql":        "ca_mcq_sql.txt",
        }

        with open(settings.BASE_DIR / 'prompts' / file_name.get(request_type, 'no_file.txt')) as f:
            return f.read()

