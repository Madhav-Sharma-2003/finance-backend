from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.permissions import IsAnalystOrAdmin, IsAdmin
from .models import FinancialRecord
from .serializers import FinancialRecordSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def record_list(request):

    if request.method == 'GET':
        records = FinancialRecord.objects.filter(is_deleted=False)

        if request.user.role == 'viewer':
            records = records.filter(user=request.user)

        # Filtering
        record_type = request.query_params.get('type')
        if record_type:
            records = records.filter(type=record_type)

        category = request.query_params.get('category')
        if category:
            records = records.filter(category=category)

        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        if start_date:
            records = records.filter(date__gte=start_date)
        if end_date:
            records = records.filter(date__lte=end_date)

        serializer = FinancialRecordSerializer(records, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not IsAnalystOrAdmin().has_permission(request, None):
            return Response(
                {'error': 'Viewers cannot create records.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = FinancialRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def record_detail(request, pk):

    try:
        record = FinancialRecord.objects.get(pk=pk, is_deleted=False)
    except FinancialRecord.DoesNotExist:
        return Response(
            {'error': 'Record not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        if request.user.role == 'viewer' and record.user != request.user:
            return Response(
                {'error': 'You cannot view this record.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = FinancialRecordSerializer(record)
        return Response(serializer.data)

    if request.method == 'PUT':
        if not IsAnalystOrAdmin().has_permission(request, None):
            return Response(
                {'error': 'Viewers cannot update records.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = FinancialRecordSerializer(
            record, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if not IsAdmin().has_permission(request, None):
            return Response(
                {'error': 'Only admins can delete records.'},
                status=status.HTTP_403_FORBIDDEN
            )
        record.is_deleted = True
        record.save()
        return Response(
            {'message': 'Record deleted successfully.'},
            status=status.HTTP_200_OK
        )