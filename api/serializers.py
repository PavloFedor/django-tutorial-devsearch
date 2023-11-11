from rest_framework import serializers
from projects.models import Project, Tag, Reviews
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        exclude = ['project']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.reviews_set.all()
        return ReviewSerializer(reviews, many=True).data
