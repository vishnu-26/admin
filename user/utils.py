from .serializers import UserSerializer,RoleSerializer,PermissionSerializer
from .models import User,Role,Permission



def get_user(user):
    try:
        user_serializer=UserSerializer(user,many=False).data
        _role = Role.objects.get(id=user_serializer['role'])
        user_serializer['role']=_role.name
        role_serializer = RoleSerializer(_role).data
#       print(role_serializer.permissions)
        user_serializer['permissions'] = [p['name'] for p in role_serializer['permissions']]
    except:
        user_serializer=None
    
    return user_serializer
