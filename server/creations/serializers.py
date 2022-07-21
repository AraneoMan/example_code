from rest_framework import serializers

from creations.models import CreationType, Creation


class CreationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreationType
        fields = ('id', 'title')


class CreationParentTypeSerializer(serializers.ModelSerializer):
    subtitles = CreationTypeSerializer(many=True, read_only=True)

    class Meta:
        model = CreationType
        fields = ('id', 'title', 'subtitles')


class CreationCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Creation
        fields = ('id', 'title', 'title_en', 'type')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
