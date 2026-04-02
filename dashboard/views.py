from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth, TruncWeek
from datetime import date, timedelta
from records.models import FinancialRecord
from users.permissions import IsAnalystOrAdmin


def get_base_queryset(user):
    queryset = FinancialRecord.objects.filter(is_deleted=False)
    if user.role == 'viewer':
        queryset = queryset.filter(user=user)
    return queryset


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def summary(request):

    queryset = get_base_queryset(request.user)

    income_data = queryset.filter(type='income').aggregate(
        total=Sum('amount')
    )
    expense_data = queryset.filter(type='expense').aggregate(
        total=Sum('amount')
    )


    total_income = income_data['total'] or 0
    total_expense = expense_data['total'] or 0
    net_balance = total_income - total_expense

    return Response({
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'total_records': queryset.count(),
        'status': 'profit' if net_balance >= 0 else 'loss'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_breakdown(request):
    queryset = get_base_queryset(request.user)

    # Type filter optional hai — ?type=expense
    record_type = request.query_params.get('type')
    if record_type:
        queryset = queryset.filter(type=record_type)

    breakdown = (
        queryset
        .values('category', 'type')   
        .annotate(
            total=Sum('amount'),       
            count=Count('id')          
        )
        .order_by('-total')            
    )

    return Response(list(breakdown))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_trend(request):
    queryset = get_base_queryset(request.user)

    # Aaj se 6 mahine pehle ki date
    six_months_ago = date.today() - timedelta(days=180)
    queryset = queryset.filter(date__gte=six_months_ago)

    
    trend = (
        queryset
        .annotate(month=TruncMonth('date'))  
        .values('month', 'type')              
        .annotate(total=Sum('amount'))        
        .order_by('month')                    
    )

    result = {}
    for entry in trend:
        month_str = entry['month'].strftime('%Y-%m')  # "2024-03"

        if month_str not in result:
            result[month_str] = {
                'month': month_str,
                'income': 0,
                'expense': 0
            }

        if entry['type'] == 'income':
            result[month_str]['income'] = entry['total']
        else:
            result[month_str]['expense'] = entry['total']

    return Response(list(result.values()))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_activity(request):
    queryset = get_base_queryset(request.user)

    recent = queryset.order_by('-date', '-created_at')[:10]

    # Import yahan karo circular import se bachne ke liye
    from records.serializers import FinancialRecordSerializer
    serializer = FinancialRecordSerializer(recent, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAnalystOrAdmin])  # viewer ko nahi — analyst/admin ko
def analytics(request):
    queryset = get_base_queryset(request.user)

    
    avg_data = queryset.aggregate(avg=Avg('amount'))
    average_amount = avg_data['avg'] or 0

    
    today = date.today()
    this_month_start = today.replace(day=1)

    # Pichle mahine ki dates
    last_month_end = this_month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    this_month = queryset.filter(date__gte=this_month_start)
    this_income = this_month.filter(type='income').aggregate(
        t=Sum('amount')
    )['t'] or 0
    this_expense = this_month.filter(type='expense').aggregate(
        t=Sum('amount')
    )['t'] or 0


    last_month = queryset.filter(
        date__gte=last_month_start,
        date__lte=last_month_end
    )
    last_income = last_month.filter(type='income').aggregate(
        t=Sum('amount')
    )['t'] or 0
    last_expense = last_month.filter(type='expense').aggregate(
        t=Sum('amount')
    )['t'] or 0

   
    top_expense_category = (
        queryset
        .filter(type='expense')
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        .first()
    )

    top_income_category = (
        queryset
        .filter(type='income')
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        .first()
    )

    return Response({
        'average_transaction_amount': round(average_amount, 2),
        'top_expense_category': top_expense_category,
        'top_income_category': top_income_category,
        'this_month': {
            'income': this_income,
            'expense': this_expense,
            'net': this_income - this_expense
        },
        'last_month': {
            'income': last_income,
            'expense': last_expense,
            'net': last_income - last_expense
        }
    })