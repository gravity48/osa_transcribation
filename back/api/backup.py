'''

class ConnectionsApi(APIView):

    @staticmethod
    def _add_connections(data):
        ccs = serializers.ConnectionsCustomSerializer(data=data)
        if ccs.is_valid():
            ccs.save()
            return {'success': True}, settings.DEFAULT_SUCCESS_STATUS
        else:
            return ccs.errors, settings.DEFAULT_ERROR_STATUS

    @staticmethod
    def _refresh_connection(data):
        try:
            cnnct_id = data['id']
        except KeyError:
            return {'error': 'no connection id'}, settings.DEFAULT_ERROR_STATUS
        return {'success': True}, settings.DEFAULT_SUCCESS_STATUS

    @staticmethod
    def _delete_connection(data):
        try:
            cnnct_id = data['id']
        except KeyError:
            return {'error': 'No connection id'}, settings.DEFAULT_ERROR_STATUS
        Connections.objects.get(pk=cnnct_id).delete()
        return {'success': True}, settings.DEFAULT_SUCCESS_STATUS

    def get(self, request):
        connections = Connections.objects.values('id', 'alias', 'db_system__name', 'ip', 'db_name',
                                                 'db_status__status_name').all()
        db_systems = DatabaseSystems.objects.values('id', 'name').all()
        context = {
            'connections': connections,
            'db_systems': db_systems,
        }
        return Response(context)

    def post(self, request):
        try:
            event = request.data['event']
        except KeyError:
            return Response(status=settings.DEFAULT_ERROR_STATUS)
        if event == 'add_connection':
            response, status = self._add_connections(request.data)
            return Response(response, status=status)
        if event == 'refresh':
            response, status = self._refresh_connection(request.data)
            return Response(response, status=status)
        if event == 'delete':
            response, status = self._delete_connection(request.data)
            return Response(response, status=status)
        return Response({'error': 'no event'}, settings.DEFAULT_ERROR_STATUS)



class ConnectionAliasApi(APIView):

    def get(self, request):
        queryset = Connections.objects.values('id','alias').all()
        return Response(queryset)


class TasksSerializer(serializers.ModelSerializer):
    db = serializers.SlugRelatedField(slug_field='id', read_only=True)
    model = serializers.SlugRelatedField(slug_field='id', read_only=True)
    task_type = serializers.SlugRelatedField(slug_field='id', read_only=True)
    status = serializers.SlugRelatedField(slug_field='id', read_only=True)
    '''
'''
task_type = TaskTypeSerializer()
db = ConnectionSerializer()
model = ModelListSerializer()
status = StatusSerilizer()
alias = serializers.CharField(allow_blank=True, required=False, validators=[tsl_alias_validator, ], max_length=100)
'''
'''
def validate(self, attrs):
    if not attrs['alias']:
        attrs['alias'] = generate_hash()
    return attrs

def create(self, validated_data):
    valid_data: dict = validated_data
    db = valid_data.pop('db')
    task_type = valid_data.pop('task_type')
    model = valid_data.pop('model')
    connection_model = Connections.objects.get(pk=db['id'])
    task_type_model = TaskType.objects.get(pk=task_type['id'])
    model_model = ModelsList.objects.get(pk=model['id'])
    Tasks.objects.create(db=connection_model, task_type=task_type_model, model=model_model, **valid_data)
    return True

class Meta:
    model = Tasks
    fields = "__all__"

class ConnectionsCustomSerializer(serializers.Serializer):
    alias = serializers.CharField(max_length=100, required=False, allow_blank=True,
                                  validators=[cnnct_alias_validator, ])
    db_system = serializers.IntegerField()
    ip = serializers.CharField(max_length=100)
    port = serializers.IntegerField()
    db_login = serializers.CharField(max_length=100)
    db_password = serializers.CharField(max_length=100)
    db_name = serializers.CharField(max_length=500)

    def validate(self, attrs):
        if not attrs['alias']:
            attrs['alias'] = generate_hash()
        return attrs

    def create(self, validated_data):
        return Connections.objects.create(**validated_data)
'''