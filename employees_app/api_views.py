from .models import Employee2
from .serializers import EmployeeSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

def not_foun_error(res = {'Error': 'Employee Not Found'}, status = status.HTTP_404_NOT_FOUND):
    """This function will return 404 error as not found. 
       This function will take custom message as well status of response will accepted only
    """
    
    return Response(res, status = status)

# Employees APi
class EmployeeAPI(APIView):
    """This class is prodive features of fetch data,inserting data, update and deletion.
       Note: Basic Authentication is applied here So Only Authenticated user can make POST, PUT, PATCH request else
       They can only make GET request because of IsAuthenticatedOrReadonly Permission is applied. 
       Thank You Open Any Suggestion krishnayadav78887@gmail.com
       """
    # basic authentication classes applied here 
    authentication_classes = [BasicAuthentication]
    # rest_framework permission class is applied here as IsAuthenticated
    permission_classes = [IsAuthenticatedOrReadOnly]  # overriding global permission class herem

    # fetch data from database
    def get(self, request, format=None):
        """GET request for all kind od users to fetch the data/records"""
        id  = request.data.get('id', None)

        if id is not None:
            try:
                emp = Employee2.objects.get(pk = id)
            except Employee2.DoesNotExist:
                return not_foun_error(res={'Not Found': "Sorry! Employee Not Exist that your looking  for"})
            else:
                serializer = EmployeeSerializer(emp)
                return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            all_emp = Employee2.objects.all()
            serializer = EmployeeSerializer(all_emp, many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
    
    # post to use to insert data into datbase
    def post(self, request, format=None):
        """POST request for insert data/records into database Only FOR Authenticated Users  """
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            res = {'Inseretd Successfuly': serializer.data}
            return Response(res, status = status.HTTP_201_CREATED)
        else:
            res = {'Error': 'Invalid request'}
            return Response(res, status= status.HTTP_400_BAD_REQUEST)
    
    # update patch request for partialy update
    def patch(self, request, format=None):
        """PATCH request for update data/records into database Only FOR Authenticated Users  """

        id = request.data.get('id', None) # parsed data
        if id is not None:
            try:
                emp = Employee2.objects.get(pk = id)
            except Employee2.DoesNotExist:
                return not_foun_error()
            else:
                serializer = EmployeeSerializer(emp, data  = request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    res = {'Update Successfuly': serializer.data}
                    return Response(res, status = status.HTTP_200_OK)
                else:
                    return not_foun_error( res = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return not_foun_error(res = {'Error': 'Employee id is required for updation'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format = None):
        """DELETE request for delete existing data/records into database Only FOR Authenticated Users  """

        id  = request.data.get('id', None)
        if id is not None:
            try: 
                emp = Employee2.objects.get(pk = id)
            except Employee2.DoesNotExist: 
                return not_foun_error()
            else:
                emp.delete() #  deleting employee here
                res = {'Deleted Successfuly': 'Employee Successfuly Deleted'}
                return Response(res, status = status.HTTP_200_OK)
        else:
            res = {'Id required': 'Employee Id is required to delete the data'}
            return Response(res, status = status.HTTP_400_BAD_REQUEST)