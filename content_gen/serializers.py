from rest_framework import serializers

class PromptSerializer(serializers.Serializer):
    process_name = serializers.CharField(max_length=100)
