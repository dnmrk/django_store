from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .engine import forecast_revenue, forecast_product_demand


class RevenueForecastView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get("days", 30))
        days = max(7, min(days, 90))  # clamp between 7 and 90
        result = forecast_revenue(days_ahead=days)
        return Response(result)


class ProductDemandForecastView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        days = int(request.query_params.get("days", 30))
        days = max(7, min(days, 90))
        result = forecast_product_demand(days_ahead=days)
        return Response(result)