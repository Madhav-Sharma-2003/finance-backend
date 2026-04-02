from rest_framework import serializers
from .models import FinancialRecord
from datetime import date


class FinancialRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialRecord
        fields = [
            'id', 'amount', 'type', 'category',
            'date', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )
        if value > 10000000:
            raise serializers.ValidationError(
                "Amount cannot exceed 1,00,00,000."
            )
        return value

    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Date cannot be in the future."
            )
        if value.year < date.today().year - 10:
            raise serializers.ValidationError(
                "Date cannot be more than 10 years in the past."
            )
        return value

    def validate_type(self, value):
        allowed = ['income', 'expense']
        if value not in allowed:
            raise serializers.ValidationError(
                f"Type must be one of: {', '.join(allowed)}"
            )
        return value

    def validate(self, data):
        notes = data.get('notes', '')
        if len(notes) > 500:
            raise serializers.ValidationError({
                'notes': 'Notes cannot exceed 500 characters.'
            })
        return data