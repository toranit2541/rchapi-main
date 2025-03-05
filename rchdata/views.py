from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

# Create your views here.
from rest_framework import viewsets
from .models import PtLabRes, PatientInHos, LabApplication, PatientData, LabResultDetail, VResultApp
from .serializers import PtLabResSerializer, PatientInHosSerializer, LabApplicationSerializer, PatientDataSerializer ,LabResultDetailSerializer, VResultAppSerializer

class PtLabResViewSet(viewsets.ModelViewSet):
    queryset = PtLabRes.objects.all()
    serializer_class = PtLabResSerializer

class PatientInHosViewSet(viewsets.ModelViewSet):
    queryset = PatientInHos.objects.all()
    serializer_class = PatientInHosSerializer
    
class PatientDataViewSet(viewsets.ModelViewSet):
    queryset = PatientData.objects.all()
    serializer_class = PatientDataSerializer
    
class LabApplicationViewSet(viewsets.ModelViewSet):
    queryset = LabApplication.objects.all()
    serializer_class = LabApplicationSerializer
    
class LabResultDetailViewSet(viewsets.ModelViewSet):
    queryset = LabResultDetail.objects.all()
    serializer_class = LabResultDetailSerializer
    
class VResultAppViewSet(viewsets.ModelViewSet):
    queryset = VResultApp.objects.all()
    serializer_class = VResultAppSerializer
    
@api_view(['POST'])
def get_vresult(request):
    citizen_id = request.data.get('CitizenID')

    if not citizen_id:
        return Response({'error': 'CitizenID is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Query using the correct field name
    results = VResultApp.objects.filter(citizen_id=citizen_id)
    
    # Serialize the data
    serializer = VResultAppSerializer(results, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

from django.db import connection
from django.http import JsonResponse


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_lab_results(request):
    # Get CitizenID from POST request data (instead of query params)
    citizen_id = request.data.get("citizen_id")
    
    if not citizen_id:
        return JsonResponse({"error": "CitizenID is required"}, status=400)

    try:
        # SQL query to retrieve lab results
        sql = """
        SELECT  
            app.LabNameTH AS LabName, 
            ISNULL(patia1.LabResultValue, '-') AS LabResult, 
            ISNULL(CAST(patia1.LabResultMIN AS NVARCHAR) + ' - ' + CAST(patia1.LabResultMAX AS NVARCHAR), '-') AS Nomal
        FROM LabApplication AS app
        LEFT JOIN (
            SELECT 
                res.LabResultCode,
                detail.LabResult,
                res.LabResultValue,
                detail.LabResultMIN,
                detail.LabResultMAX,
                patient.CitizenID,
                patient.FName,
                patient.LName
            FROM PtLabRes AS res
            INNER JOIN LabResultDetail AS detail ON res.LabResultCode = detail.LabResultCode
            INNER JOIN PatientInHos AS hos ON res.VN = hos.VN AND res.VnDate = hos.VnDate
            INNER JOIN PatientData AS patient ON patient.HN = hos.HN AND patient.HnYear = hos.HnYear
            WHERE patient.CitizenID = %s
              AND res.VnDate = (
                SELECT MAX(res2.VnDate)
                FROM PtLabRes AS res2
                INNER JOIN LabResultDetail AS detail2 ON res2.LabResultCode = detail2.LabResultCode
                INNER JOIN PatientInHos AS hos2 ON res2.VN = hos2.VN AND res2.VnDate = hos2.VnDate
                INNER JOIN PatientData AS patient2 ON patient2.HN = hos2.HN AND patient2.HnYear = hos2.HnYear
                WHERE patient2.CitizenID = %s
              )
        ) AS patia1 ON app.LabResultCode = patia1.LabResultCode
        ORDER BY app.LabResultCode;
        """
        
        # Execute the SQL query
        with connection.cursor() as cursor:
            cursor.execute(sql, [citizen_id, citizen_id])
            rows = cursor.fetchall()  # Fetch all results
        
        if not rows:
            return JsonResponse({"message": "No results found for the given CitizenID."}, status=200)
        
        # Define column names based on the SQL SELECT clause
        columns = ["AppLabName", "LabResultValue", "LabResultMIN", "LabResultMAX", "CitizenID"]
        
        # Prepare results in JSON format
        results = [dict(zip(columns, row)) for row in rows]

        return JsonResponse(results, safe=False, status=200)
    
    except Exception as e:
        # Handle any database or query execution errors
        # Log the error (avoid logging sensitive data like CitizenID)
        print(f"Error: {str(e)}")  # Replace with proper logging if needed
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_lab_results_dynamic(request):
    citizen_id = request.data.get('citizen_id')
    if not citizen_id:
        return Response({'error': 'CitizenID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Call the function to execute the dynamic SQL query
        results = execute_query(citizen_id)
        return Response(results, status=status.HTTP_200_OK)
    except Exception as e:
        # Catch any exceptions during query execution and return a 500 error with the message
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def execute_query(citizen_id):
    try:
        with connection.cursor() as cursor:
            # Step 1: Generate dynamic columns based on distinct VnDates
            cursor.execute("""
            DECLARE @cols NVARCHAR(MAX);
            SET @cols = STUFF((
                SELECT ',' + QUOTENAME(CONVERT(varchar, VnDate, 23))
                FROM (
                    SELECT DISTINCT PtLabRes.VnDate
                    FROM PtLabRes
                    INNER JOIN LabResultDetail ON PtLabRes.LabResultCode = LabResultDetail.LabResultCode
                    INNER JOIN PatientInHos ON PtLabRes.VN = PatientInHos.VN AND PtLabRes.VnDate = PatientInHos.VnDate
                    INNER JOIN PatientData ON PatientData.HN = PatientInHos.HN AND PatientData.HnYear = PatientInHos.HnYear
                    WHERE PatientData.CitizenID = %s
                ) AS DistinctDates
                ORDER BY VnDate
                FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '');
            SELECT @cols;
            """, [citizen_id])

            # Fetch the result of the dynamic columns query
            result = cursor.fetchone()
            if not result or not result[0]:
                return []  # No data for the given CitizenID, returning empty list

            cols = result[0]

            # Step 2: Construct and execute the dynamic query using the generated columns
            query = f"""
            DECLARE @cols NVARCHAR(MAX) = '{cols}';
            DECLARE @query NVARCHAR(MAX);
            SET @query = '
            WITH LabData AS (
                SELECT 
                    app.LabNameTH AS AppLabName, 
                    ISNULL(patia1.LabResultValue, ''-'') AS LabResultValue,
                    CONVERT(varchar, patia1.VnDate, 23) AS VnDate
                FROM LabApplication AS app
                LEFT JOIN (
                    SELECT 
                        res.LabResultCode,
                        res.VnDate,
                        res.LabResultValue,
                        patient.CitizenID
                    FROM PtLabRes AS res
                    INNER JOIN LabResultDetail AS detail ON res.LabResultCode = detail.LabResultCode
                    INNER JOIN PatientInHos AS hos ON res.VN = hos.VN AND res.VnDate = hos.VnDate
                    INNER JOIN PatientData AS patient ON patient.HN = hos.HN AND patient.HnYear = hos.HnYear
                    WHERE patient.CitizenID = ''{citizen_id}'' 
                ) AS patia1 ON app.LabResultCode = patia1.LabResultCode
            )
            SELECT AppLabName, ' + @cols + '
            FROM LabData
            PIVOT (
                MAX(LabResultValue)
                FOR VnDate IN (' + @cols + ')
            ) AS PivotTable
            ORDER BY AppLabName;
            ';
            EXEC sp_executesql @query;
            """
            print(f"Executing Query: {query}")  # Log the query for debugging (Be cautious about logging sensitive info)
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [col[0] for col in cursor.description]

        return [dict(zip(column_names, row)) for row in rows]
    
    except Exception as e:
        raise Exception(f"Dynamic SQL Execution Error: {str(e)}")