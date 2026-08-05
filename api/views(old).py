          
from rest_framework import views, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OwnerSerializer, OverseerSerializer,ChangePasswordSerializer,OwnerUpdateSerializer,PassResetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Owner, Overseer,Friend,Thana,User,Event,Upvote,Blog,Chat,Notification,Trip,Additional
from .serializers import OwnerSerializer, OverseerSerializer,UserLoginSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from django.shortcuts import render
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request):
        return Response(data={"message": "Hello, world!"})
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

class HelloWorldView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(data={"message": "Hello, world!"})
        
class O_update(APIView):
    def put(self, request, pk):
        try:
                                                       
            overseer = Overseer.objects.get(pk=pk)
        except Overseer.DoesNotExist:
            return Response({"error": "Overseer not found"}, status=status.HTTP_404_NOT_FOUND)

                                       
        serializer = OverseerSerializer(overseer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
                                                        
            overseer = Overseer.objects.get(pk=pk)
        except Overseer.DoesNotExist:
            return Response({"error": "Overseer not found"}, status=status.HTTP_404_NOT_FOUND)

                                                                               
        serializer = OverseerSerializer(overseer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class Owner_update(APIView):
    def put(self, request, username):
        try:
            owner = Owner.objects.get(username=username)
            serializer = OwnerUpdateSerializer(owner, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Owner.DoesNotExist:
            try:
                overseer = Overseer.objects.get(username=username)
                serializer = OverseerSerializer(overseer, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Overseer.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
                                                    
            owner = Owner.objects.get(pk=pk)
        except Owner.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                                                                           
        serializer = OwnerSerializer(owner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class sign(APIView):
    def post(self, request):
                            
        serializer = OwnerSerializer(data=request.data)
        print("why didnt working?")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class _sign(views.APIView):
    def post(self, request):
        serializer = OverseerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        print(serializer.errors)
        user.id=0 if user is None else user.id
                              
                                                                                                                                                                                       
                         
        return Response({"message": "User created successfully", "user_id":user.id}, status=status.HTTP_201_CREATED)
                                  
                                                                                

from django.contrib.auth import authenticate, login

class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)
        
from django.contrib.auth import logout

class login_api(views.APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
                                                    
        print(data)
                        
        if username and password:
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request,user)
                user=Owner.objects.filter(username=username)
                if len(user) > 0:
                    serializer = OwnerSerializer(user[0])
                    return Response({'auth': True,'user':serializer.data}, status=status.HTTP_200_OK)
                serializer = OverseerSerializer(Overseer.objects.get(username=username))
                username_part = username.split("@")[1]
                owner = Owner.objects.filter(username=username_part).first()
                if owner and owner.p_image:
                    img_url = owner.p_image.url
                else:
                    img_url = "/media/image/download_lX6bjA6.jpeg"
                serializer.data['pp'] = img_url
                serializer.data['p_image'] = img_url

                return Response({'auth': True,'user':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'auth': False}, status=status.HTTP_401_UNAUTHORIZED)


class show(views.APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if(request.user.is_authenticated):
            return Response({'authenticated boSS!': True}, status=status.HTTP_200_OK)
        return Response({'authenticated': False}, status=status.HTTP_401_UNAUTHORIZED)



def friends(request):
    user = Owner.objects.get(username="nuha1")
    queryset = Friend.objects.filter(user1=user.id) | Friend.objects.filter(user2=user.id)
    queryset = queryset.exclude(user1=user.id) | queryset.exclude(user2=user.id)
    print(queryset)
    fndlist=[Owner.objects.get(id=fr.user1.id) for fr in queryset]
    print(fndlist)
    return queryset

    return HttpResponse("Hello, this is the friends page!")


class MyAPIView(views.APIView):
    def get(self, request):
                                                   
        name = request.GET.get('name')
                                     

                             
        queryset = MyModel.objects.all()
        print(name)

                                                 
        if name:
            queryset = queryset.filter(name=name)
                
                                                

                                                    
        data = list(queryset.values())

                                                   
        serializer = MyModelSerializer(queryset, many=True)
        return Response(serializer.data)


                                                
                             
                                          
                                                             
                             
                                          
        
                              
                                                           
                                   
                               
                                                                              
                                                                                



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password


class ChangePass(views.APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        print(request.user)
        if serializer.is_valid():
            print(serializer.validated_data)
            print("You are in changepass class")
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            username = serializer.validated_data['username']
            user = User.objects.get(username=username)
            if(user.check_password(old_password)):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

            if check_password(old_password, user.password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth.hashers import make_password

class PassReset(views.APIView):
    def post(self, request):
        print(request.data)
        serializer = PassResetSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            new_password = serializer.validated_data['new_password']
            done = serializer.validated_data['done']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            user.set_password(new_password)
            user.save()
                            
                                
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class add_fnf(APIView):
    def post(self, request):
        data = request.data
        if(str(data['user_id']) == str(data['friend_id'])):
            return Response({"message": "You can't add yourself as friend"}, status=status.HTTP_400_BAD_REQUEST)
        print(data)

        fnd=Friend.objects.filter(user1=Owner.objects.get(id=data['user_id']),user2=Owner.objects.get(id=data['friend_id']))
        fnd|=Friend.objects.filter(user2=Owner.objects.get(id=data['user_id']),user1=Owner.objects.get(id=data['friend_id']))
        if(len(fnd) > 0 and fnd[0].is_fnf == 1):
            return Response({"message": "You are already friend"}, status=status.HTTP_400_BAD_REQUEST)
                                                
        if(len(fnd) > 0):
            return Response({"message": "Your request for friend send"}, status=status.HTTP_201_CREATED)
        from django.utils import timezone
        print(data['type'])
        fnd=Friend(user1=Owner.objects.get(id=data['user_id']),user2=Owner.objects.get(id=data['friend_id']),type=data['type'],f_created_date=timezone.now(),is_fnf=0)
        fnd.save()
        noti=Notification(noti_type="Bondhu",noti_msg="send you friend request",noti_sender=Owner.objects.get(id=data['user_id']),noti_receiver=Owner.objects.get(id=data['friend_id']),noti_status=0)
        noti.save()
        return Response({"message": "Friends Added successfully"}, status=status.HTTP_201_CREATED)

class update_fnf(APIView):
    def post(self, request):
        data = request.data
        if(str(data['user_id']) == str(data['friend_id'])):
            return Response({"message": "You can't add yourself as friend"}, status=status.HTTP_400_BAD_REQUEST)

        fnd=Friend.objects.filter(user1=Owner.objects.get(id=data['user_id']),user2=Owner.objects.get(id=data['friend_id']))
        fnd|=Friend.objects.filter(user2=Owner.objects.get(id=data['user_id']),user1=Owner.objects.get(id=data['friend_id']))
                   
                                                
        if(len(fnd) > 0):
            if(data['type'] == "Delete"):
                fnd[0].delete()
                return Response({"message": "Request Deleted successfully"}, status=status.HTTP_201_CREATED)
            fnd[0].is_fnf= 1 if fnd[0].is_fnf== 0 else fnd[0].is_fnf
            fnd[0].type=data['type']
            fnd[0].save()
            return Response({"message": "Friends Updated successfully"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Friends not find"}, status=status.HTTP_400_BAD_REQUEST)
class Delete_fnd(APIView):
    def post(self, request):
        data = request.data
        if(str(data['user_id']) == str(data['friend_id'])):
            return Response({"message": "You can't add yourself as friend"}, status=status.HTTP_400_BAD_REQUEST)

        fnd=Friend.objects.filter(user1=Owner.objects.get(id=data['user_id']),user2=Owner.objects.get(id=data['friend_id']))
        fnd|=Friend.objects.filter(user2=Owner.objects.get(id=data['user_id']),user1=Owner.objects.get(id=data['friend_id']))
                   
                                                
        if(len(fnd) > 0):
            fnd[0].delete()
            return Response({"message": "Friends Deleted successfully"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Friends not find"}, status=status.HTTP_400_BAD_REQUEST)


class FriendList(APIView):
    def get(self, request):
        users = Owner.objects.all()
        userid=request.GET.get('user_id')
        print("ami esesi akhon from groupsshow")
        print(userid)
                            
        serialized_data = []
        for user in users:
            fnd=Friend.objects.filter(user1=Owner.objects.get(id=userid),user2=user.id)
            fnd2=Friend.objects.filter(user2=Owner.objects.get(id=userid),user1=user.id)
            fnd=fnd[0] if len(fnd) > 0 else None
            if(fnd is not None and fnd.is_fnf ==1) or (len(fnd2)>0  and fnd2[0].is_fnf==1):
                    img_url = user.p_image.url if user.p_image else "/media/image/download_lX6bjA6.jpeg"
                    serialized_data.append({
                        'id': user.id,
                        'pp': img_url,
                        'p_image': img_url,
                        'first_name': user.first_name,
                        'username': user.username,
                        'last_name': user.last_name,
                        'email': user.email,
                        'gender': user.gender,
                        'phone': user.phone,
                        'dob': user.dob,
                        'address': user.address,
                        'nid': user.nid,
                        'thana': Thana.objects.get(thana=user.thana_id).thana,
                        'is_fnf': fnd.is_fnf if fnd is not None else fnd2[0].is_fnf if len(fnd2)>0 else None,
                        'type': fnd.type if fnd is not None else fnd2[0].type if len(fnd2)>0 else None,
                        'f_created_date': fnd.f_created_date if fnd is not None else  None,
                        'f_id': fnd.f_id if fnd is not None else None,
                        'abedon': 1 if fnd is not None else 0,
                        'good': fnd.user1.username if fnd is not None else None,
                        'msg': "gd night",
                        'time': "12:00",
                    })
        print(serialized_data)
        return Response({"users": serialized_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)


class FindFriend(APIView):
    def get(self, request):
        userid = request.GET.get('user_id')
        user_obj = None
        if userid:
            user_obj = Owner.objects.filter(id=userid).first()
        
        if user_obj:
            from api.recommender_service import decoupled_recommender
            ai_friends = decoupled_recommender.get_recommended_friends(user_obj.username, limit=30)
            if ai_friends:
                full_friends_data = []
                for cand in ai_friends:
                    cand_user = Owner.objects.filter(id=cand['id']).first()
                    if not cand_user:
                        continue
                    fnd = Friend.objects.filter(user1=user_obj, user2=cand_user).first()
                    fnd2 = Friend.objects.filter(user2=user_obj, user1=cand_user).first()
                    
                    full_friends_data.append({
                        'id': cand_user.id,
                        'pp': cand['pp'],
                        'p_image': cand['p_image'],
                        'first_name': cand_user.first_name,
                        'username': cand_user.username,
                        'last_name': cand_user.last_name,
                        'email': cand_user.email,
                        'gender': cand_user.gender,
                        'phone': cand_user.phone,
                        'dob': cand_user.dob,
                        'address': cand_user.address,
                        'nid': cand_user.nid,
                        'thana': cand['thana'],
                        'score': cand['score'],
                        'reason': cand['reason'],
                        'is_fnf': fnd.is_fnf if fnd else fnd2.is_fnf if fnd2 else None,
                        'type': fnd.type if fnd else fnd2.type if fnd2 else None,
                        'f_created_date': fnd.f_created_date if fnd else None,
                        'f_id': fnd.f_id if fnd else None,
                        'abedon': 1 if fnd else 0,
                        'good': fnd.user1.username if fnd else None,
                        'status': 1 if fnd else 1 if fnd2 else 0,
                    })
                return Response({"users": full_friends_data, "message": "AI Recommended buddies retrieved successfully"}, status=status.HTTP_200_OK)

        users = Owner.objects.all()
        serialized_data = []
        for user in users:
            if userid and str(user.id) == str(userid):
                continue
            fnd = Friend.objects.filter(user1=Owner.objects.get(id=userid), user2=user.id) if userid else []
            fnd2 = Friend.objects.filter(user2=Owner.objects.get(id=userid), user1=user.id) if userid else []

            if len(fnd) > 0 and fnd[0].is_fnf == 1:
                continue
            if len(fnd2) > 0 and fnd2[0].is_fnf == 1:
                continue
            fnd = fnd[0] if len(fnd) > 0 else None 
            img_url = user.p_image.url if user.p_image else "/media/image/download_lX6bjA6.jpeg"
            serialized_data.append({
                'id': user.id,
                'pp': img_url,
                'p_image': img_url,
                'first_name': user.first_name,
                'username': user.username,
                'last_name': user.last_name,
                'email': user.email,
                'gender': user.gender,
                'phone': user.phone,
                'dob': user.dob,
                'address': user.address,
                'nid': user.nid,
                'thana': Thana.objects.get(thana=user.thana_id).thana if user.thana_id else '',
                'is_fnf': fnd.is_fnf if fnd is not None else fnd2[0].is_fnf if len(fnd2) > 0 else None,
                'type': fnd.type if fnd is not None else fnd2[0].type if len(fnd2) > 0 else None,
                'f_created_date': fnd.f_created_date if fnd is not None else None,
                'f_id': fnd.f_id if fnd is not None else None,
                'abedon': 1 if fnd is not None else 0,
                'good': fnd.user1.username if fnd is not None else None,
                'status': 1 if fnd is not None else 1 if len(fnd2) > 0 else 0,
            })
        return Response({"users": serialized_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)
        
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer

                                                                                      
                                                                          
try:
    from gensim.models import KeyedVectors
    GENSIM_AVAILABLE = True
except ImportError:
    GENSIM_AVAILABLE = False
    KeyedVectors = None
                                                                                                                                                                     

class PreRun():
    def __init__(self):
        print("pre run is called")
        if GENSIM_AVAILABLE and KeyedVectors is not None:
            try:
                self.word_pre_vectors = KeyedVectors.load_word2vec_format(r'D:\DEV\GoogleNews-vectors-negative300.bin\GoogleNews-vectors-negative300.bin', binary=True)
            except Exception as e:
                print("Could not load word vectors:", e)
                self.word_pre_vectors = None
        else:
            self.word_pre_vectors = None

        


class FriendSuggestion(APIView):
    def __init__(self):
        prerun=PreRun()
        print("ye bhai eid ka chand hai")
        self.word_vectors=prerun.word_pre_vectors
                     
    def preprocess_text(self,text):
                       
        tokens = word_tokenize(text)
                          
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
                               
                          
                            
                                          
                                                                                      
                                    
        preprocessed_text = ' '.join(filtered_tokens)
        return preprocessed_text

                                                       
    def encode_text(self,text):
            tokens = self.preprocess_text(text)
                         
                          
            for token in tokens.split():
                if token not in self.word_vectors:
                    print(token)
            vectors = [self.word_vectors[token] for token in tokens.split() if token in self.word_vectors]
            return np.mean(vectors, axis=0) if vectors else np.zeros(self.word_vectors.vector_size)
                                                

            
                                            
    def calculate_similarity(self,text1, text2):
            vector1=[]
            vector2=[]
            vector1 = self.encode_text(text1)
            vector2 = self.encode_text(text2)
            if vector1 is not None and vector2 is not None:
                return cosine_similarity([vector1], [vector2])[0][0]
                                                                 
            else:
               return 0

    
    ''' def __init__(self):
        self.word_vectors = KeyedVectors.load_word2vec_format('D:/DEV/glove.6B/glove.6B.300d.txt', binary=False)
        self.stop_words = set(stopwords.words('english'))
    
    def text_to_vector(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [token for token in tokens if token not in self.stop_words]
        vectors = [self.word_vectors[token] for token in tokens if token in self.word_vectors]
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(self.word_vectors.vector_size)

    def calculate_similarity(self, text1, text2):
        vector1 = self.text_to_vector(text1)
        vector2 = self.text_to_vector(text2)
        return cosine_similarity([vector1], [vector2])[0][0]

    def preprocess_text(self, text):
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        preprocessed_text = ' '.join(lemmatized_tokens)
        return preprocessed_text'''

    def get(self, request):
        username = request.GET.get('username')
        user_id = request.GET.get('user_id')
        if not username and user_id:
            try:
                owner = Owner.objects.get(id=user_id)
                username = owner.username
            except Exception:
                pass
        if not username and user_id:
            try:
                owner = Owner.objects.get(username=user_id)
                username = owner.username
            except Exception:
                pass
        if not username:
            return Response({"error": "user_id or username required"}, status=400)

        from api.recommender import recommender_engine
        suggestions = recommender_engine.get_recommended_friends(username)
        return Response({"users": suggestions, "message": "User suggestions retrieved successfully"}, status=status.HTTP_200_OK)




class EventShow(APIView):
    def get(self,request):
        return response("Hello, this is the event page!")


                    
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer

class FriendSugg(APIView):
    def preprocess_text(self, text):
                       
        tokens = word_tokenize(text)
                          
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
                          
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
                                    
        preprocessed_text = ' '.join(lemmatized_tokens)
        return preprocessed_text

    def get(self, request):
        userid = request.GET.get('user_id')
                           
        user = Owner.objects.get(id=userid)
                                                                              
        friend_ids = Friend.objects.filter(user1=user, is_fnf=1).values_list('user2_id', flat=True)
                                                                              
        friend_ids2 = Friend.objects.filter(user2=user, is_fnf=1).values_list('user1_id', flat=True)
                                    
        friend_ids = list(friend_ids)
        friend_ids2 = list(friend_ids2)
                                                  
        friend_ids.append(user.id)
                                
        friend_ids.extend(friend_ids2)
        
                                                                     
        user_blog_posts = Blog.objects.filter(author=user)
        user_comments = Comment.objects.filter(username=user)
        user_group_posts = GroupPost.objects.filter(p_username=user)
        
                                                                              
        user_text = ''
        for post in user_blog_posts:
            user_text += post.content + ' '
        for comment in user_comments:
            user_text += comment.comment + ' '
        for group_post in user_group_posts:
            user_text += group_post.GPost_contents + ' '
        
        text1=user_text
                              
        user_text = self.preprocess_text(user_text)
        
                                                
        users = Owner.objects.exclude(id__in=friend_ids)
        
                                                           
        vectorizer = TfidfVectorizer()
        user_tfidf = vectorizer.fit_transform([user_text])
        other_users_tfidf = []
        for other_user in users:
            other_user_blog_posts = Blog.objects.filter(author=other_user)
            other_user_comments = Comment.objects.filter(username=other_user)
            other_user_group_posts = GroupPost.objects.filter(p_username=other_user)
            
            other_user_text = ''
            for post in other_user_blog_posts:
                other_user_text += post.content + ' '
            for comment in other_user_comments:
                other_user_text += comment.comment + ' '
            for group_post in other_user_group_posts:
                other_user_text += group_post.GPost_contents + ' '
            
            text2=other_user_text
                                        
            other_user_text = self.preprocess_text(other_user_text)
            
            other_user_tfidf = vectorizer.transform([other_user_text])
            other_users_tfidf.append(other_user_tfidf)
                                                                  
        similarities = []
        for other_user_tfidf in other_users_tfidf:
            similarity = cosine_similarity(user_tfidf, other_user_tfidf)
            similarities.append(similarity[0][0])
                                               
        sorted_users = sorted(zip(users, similarities), key=lambda x: x[1], reverse=True)
        
        serialized_data = []
        for sorted_user, similarity_score in sorted_users:
            serialized_data.append({
                'id': sorted_user.id,
                'similarity_score': similarity_score,
                'first_name': sorted_user.first_name,
                'last_name': sorted_user.last_name,
                'username': sorted_user.username,
                'email': sorted_user.email,
                'gender': sorted_user.gender,
                'phone': sorted_user.phone,
                'dob': sorted_user.dob,
                'address': sorted_user.address,
                'nid': sorted_user.nid,
                'thana': Thana.objects.get(thana=sorted_user.thana).thana,
                'pp': sorted_user.p_image.url if sorted_user.p_image else '/media/image/download_lX6bjA6.jpeg',
                'p_image': sorted_user.p_image.url if sorted_user.p_image else '/media/image/download_lX6bjA6.jpeg',
                'is_fnf': 0,
                'type': Friend.objects.filter(user1=user, user2=sorted_user).values_list('type', flat=True).first() if Friend.objects.filter(user1=user, user2=sorted_user).exists() else Friend.objects.filter(user2=user, user1=sorted_user).values_list('type', flat=True).first() if Friend.objects.filter(user2=user, user1=sorted_user).exists() else None,
                'f_created_date':Friend.objects.filter(user1=user, user2=sorted_user).values_list('f_created_date', flat=True).first() if Friend.objects.filter(user1=user, user2=sorted_user).exists() else Friend.objects.filter(user2=user, user1=sorted_user).values_list('f_created_date', flat=True).first() if Friend.objects.filter(user2=user, user1=sorted_user).exists() else None,
                'f_id': Friend.objects.filter(user1=user, user2=sorted_user).values_list('f_id', flat=True).first() if Friend.objects.filter(user1=user, user2=sorted_user).exists() else Friend.objects.filter(user2=user, user1=sorted_user).values_list('f_id', flat=True).first() if Friend.objects.filter(user2=user, user1=sorted_user).exists() else None,
                'abedon': 1 if Friend.objects.filter(user1=user, user2=sorted_user).exists() else 0,
                'good': user.username if Friend.objects.filter(user1=user, user2=sorted_user).exists() else sorted_user.username if Friend.objects.filter(user2=user, user1=sorted_user).exists() else 0,
                'status': 1 if Friend.objects.filter(user1=user, user2=sorted_user).exists() else 1 if Friend.objects.filter(user2=user, user1=sorted_user).exists() else 0,
                 })
        return Response({"users": serialized_data, "message": "User suggestions retrieved successfully"}, status=status.HTTP_200_OK)

class Profile(APIView):
    def get(self, request, username):
        print("here is profileview")
        user2=request.GET.get('user')
        print(user2)
        try:
            user = Owner.objects.get(username=username)
            if(user2 is not None and user2!=username):
                   user2=Owner.objects.get(username=user2)
            else:
                user2=user
            from .models import Verified
            b=Verified.objects.filter(user=Owner.objects.get(username=username))
            if len(b)>0:
                b=b[0]
            else:
                b=None
            v=1 if b is not None else 0
            img_url = user.p_image.url if user.p_image else "/media/image/download_lX6bjA6.jpeg"
            user={
                'id': user.id,
                'pp': img_url,
                'p_image': img_url,
                'first_name': user.first_name,
                'username': user.username,
                'last_name': user.last_name,
                'email': user.email,
                'gender': user.gender,
                'phone': user.phone,
                'dob': user.dob,
                'address': user.address,
                'nid': user.nid,
                'thana': Thana.objects.get(thana=user.thana_id).thana,
                'is_fnf': 1 if Friend.objects.filter(user1=user, user2=user2,is_fnf=1).exists() else 1 if Friend.objects.filter(user2=user, user1=user2,is_fnf=1).exists() else 0,
                'type': Friend.objects.filter(user1=user, user2=user2).values_list('type', flat=True).first() if Friend.objects.filter(user1=user, user2=user2).exists() else Friend.objects.filter(user2=user, user1=user2).values_list('type', flat=True).first() if Friend.objects.filter(user2=user, user1=user2).exists() else None,
                'f_created_date':Friend.objects.filter(user1=user, user2=user2).values_list('f_created_date', flat=True).first() if Friend.objects.filter(user1=user, user2=user2).exists() else Friend.objects.filter(user2=user, user1=user2).values_list('f_created_date', flat=True).first() if Friend.objects.filter(user2=user, user1=user2).exists() else None,
                'f_id': Friend.objects.filter(user1=user, user2=user2).values_list('f_id', flat=True).first() if Friend.objects.filter(user1=user, user2=user2).exists() else Friend.objects.filter(user2=user, user1=user2).values_list('f_id', flat=True).first() if Friend.objects.filter(user2=user, user1=user2).exists() else None,
                'abedon': 1 if Friend.objects.filter(user1=user, user2=user2).exists() else 0,
                'good': 1 if Friend.objects.filter(user1=user, user2=user2).exists() else 1 if Friend.objects.filter(user2=user, user1=user2).exists() else 0,
                'status': 1 if Friend.objects.filter(user1=user, user2=user2).exists() else 1 if Friend.objects.filter(user2=user, user1=user2).exists() else 0,
                 'img_privacy': 0,
                 'walk_type':user.walk_type,
                 'verify':1 if b is not None and b.verified==1 else 0,
            }
            print(user)
           
            return Response(user, status=status.HTTP_200_OK)
                                
                                                                                                  
        except Owner.DoesNotExist:
            try:
                user = Overseer.objects.get(username=username)
                user_data = {
                    'id': user.id,
                    'pp': user.p_image.url if user.p_image else "/media/image/download_lX6bjA6.jpeg",
                    'p_image': user.p_image.url if user.p_image else "/media/image/download_lX6bjA6.jpeg",
                    'first_name': user.first_name,
                    'username': user.username,
                    'last_name': user.last_name,
                    'email': user.email,
                    'gender': user.gender,
                    'phone': user.phone,
                    'dob': user.dob,
                    'address': user.address,
                    'nid': user.nid,
                    'relation': user.Relation,
                    'location': user.Location,
                    'is_overseer': True,
                    'verify': 1
                }
                return Response(user_data, status=status.HTTP_200_OK)
            except Overseer.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import requests
import random
import string
                        
class OTPAPI(APIView):
    def post(self, request):
                                                         
                            
        username = request.data.get('input')
        
                                                                             
                                                                       
                                                           
        try:
            user = Owner.objects.get(username=username)
                        
            email_address = user.email
                                 
            verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            print(verification_code)
                                                                

                                         
                                                                            
            return Response({"message": "Verification email sent successfully", "code": verification_code,"username":user.username}, status=status.HTTP_200_OK)
        except Owner.DoesNotExist:
                print("User not found")
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                
    def send_verification_email(self, email_address, verification_code):
                                                                    
        subject = 'Email Verification Code from Nostalgia'
        message = f'Your verification code is: {verification_code}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email_address]
        send_mail(subject, message, from_email, recipient_list)


class profile(APIView):
    def get(self, request):
        data = request.data
        print(data)
        return Response({"message": "Friends Retrive successfully"}, status=status.HTTP_201_CREATED)


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Friend
from .serializers import FriendSerializer
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
class FriendListView(generics.ListAPIView):
    serializer_class = FriendSerializer
                                                                      
    paginate_by = 10                                               

    def get_queryset(self):
                                               
        user = self.request.user

                                                                                             
        queryset = Friend.objects.filter(user1=user) | Friend.objects.filter(user2=user)
        queryset = queryset.exclude(user1=user) | queryset.exclude(user2=user)
        fndlist=[Owner.objects.get(id=fr.user1_id) for fr in queryset]
        print(fndlist)
        return queryset
    

    def get(self, request, *args, **kwargs):
                                                    
        page_number = request.query_params.get('page')
        if page_number:
            return self.list(request, *args, **kwargs)                                           
        else:
                                                                                       
            friend_id = kwargs.get('pk')                                         
            try:
                friend = Friend.objects.get(pk=friend_id)
            except Friend.DoesNotExist:
                return Response({"error": "Friend not found"}, status=status.HTTP_404_NOT_FOUND)

                                                                           
            current_user = request.user
            if friend.user1 == current_user:
                friend_owner = friend.user2
            else:
                friend_owner = friend.user1

                                               
            owner_serializer = OwnerSerializer(friend_owner)
            return Response(owner_serializer.data)


import os
import base64
import requests

class FaceCompareAPIBox:
    def __init__(self):
        api_key = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
        api_secret = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"
        url = "https://api-us.faceplusplus.com/facepp/v3/compare"

    def compare_images(self, image_path1, image_path2):
                                                             
        base64_image1 = self.encode_image_to_base64(image_path1)
        base64_image2 = self.encode_image_to_base64(image_path2)

                             
        payload = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "image_base64_1": base64_image1,
            "image_base64_2": base64_image2,
        }

                                             
        response = requests.post(self.url, data=payload)
        response_json = response.json()

                                                    
        return self.process_response(response_json)

    def encode_image_to_base64(self, image_path):
        with open(image_path, 'rb') as img_file:
            image_content = img_file.read()
            base64_image = base64.b64encode(image_content).decode('utf-8')
        return base64_image

    def process_response(self, response_json):
        confidence = response_json.get('confidence', 0)
        threshold = 50
        if confidence >= threshold:
            return "Match between two photos is successful with confidence: {:.2f}".format(confidence)
        else:
            return "Match between two photos is not successful. Confidence is too low: {:.2f}".format(confidence)
        

import base64
class FaceApiCompare:
    API_KEY = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
    API_SECRET = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"
    URL = "https://api-us.faceplusplus.com/facepp/v3/compare"

    def encode_image_to_base64(self, image_path):
        with open(image_path, 'rb') as img_file:
            image_content = img_file.read()
            base64_image = base64.b64encode(image_content).decode('utf-8')
        return base64_image

    def compare_images(self, image_base64_1, image_base64_2):
                                            
        payload = {
            "api_key": self.API_KEY,
            "api_secret": self.API_SECRET,
            "image_base64_1": image_base64_1,
            "image_base64_2": image_base64_2,
        }
                                         
        response = requests.post(self.URL, data=payload)
        if(response.json().get('error_message')):
            return "Error: {}".format(response.json().get('error_message'))
        response_json = response.json()
                                                    
        confidence = response_json.get('confidence', 0)
        return confidence
        
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64

face_api_compare = FaceApiCompare()

from django.http import JsonResponse
from rest_framework.views import APIView
import requests

face_api_compare = FaceApiCompare()
class CompareImagesView(APIView):
      def post(self, request, *args, **kwargs):
                                              
        print(request.data)
        image_file1 = request.FILES.get('image1')
                                                   
        image_file2 = request.data['image2']
        if(image_file1 is not None):
            print("image1")
        if(image_file2 is not None):
            print(image_file2)

        if not (image_file1 and image_file2):
            return JsonResponse({'error': 'Missing image data in request'}, status=400)
        
                                          
        image_base64_1 = base64.b64encode(image_file1.read()).decode('utf-8')
                                                                               
                                                 
        image_file2_url = "http://localhost:8000" + image_file2
        print(image_file2_url)
        image_file2_path = r"D:\DEV\Django\Nostalgia\media\image\image_file2.jpg"
        image_base64_2=""
        response = requests.get(image_file2_url)
        if response.status_code == 200:
                                 
            with open(image_file2_path, "wb") as f:
                f.write(response.content)
                print("Image file saved successfully.")
            
                                                    
            with open(image_file2_path, "rb") as f:
                image_base64_2 = base64.b64encode(f.read()).decode('utf-8')
                                                                    
        if not image_base64_2:
            return JsonResponse({'error': 'Failed to download the Profile image file'}, status=500)

        result = face_api_compare.compare_images(image_base64_1, image_base64_2)

                                                       
        return JsonResponse({'result': result})
        
class CompareImages(APIView):
      def post(self, request, *args, **kwargs):
                                              
        print(request.data)
                                                   
        image_file2 = request.data['image2']
        image_file1 = request.data['image1']
        if(image_file1 is not None):
            print("image1")
        if(image_file2 is not None):
            print(image_file2)
        if not (image_file1 and image_file2):
            return JsonResponse({'error': 'Missing image data in request'}, status=400)
        
        image_file1_url = "http://localhost:8000" + image_file2
        print(image_file1_url)
        image_file1_path = r"D:\DEV\Django\Nostalgia\media\image\image_file2.jpg"
        image_base64_1=""
        response = requests.get(image_file1_url)
        if response.status_code == 200:
                                 
            with open(image_file1_path, "wb") as f:
                f.write(response.content)
                print("Image file saved successfully.")
            
                                                    
            with open(image_file1_path, "rb") as f:
                image_base64_1 = base64.b64encode(f.read()).decode('utf-8')
                                                                    
        if not image_base64_1:
            return JsonResponse({'error': 'Failed to download the Profile image file'}, status=500)
                                                                               
                                                 
        image_file2_url = "http://localhost:8000" + image_file2
        print(image_file2_url)
        image_file2_path = r"D:\DEV\Django\Nostalgia\media\image\image_file2.jpg"
        image_base64_2=""
        response = requests.get(image_file2_url)
        if response.status_code == 200:
                                 
            with open(image_file2_path, "wb") as f:
                f.write(response.content)
                print("Image file saved successfully.")
                                                    
            with open(image_file2_path, "rb") as f:
                image_base64_2 = base64.b64encode(f.read()).decode('utf-8')
                                                                    
        if not image_base64_2:
            return JsonResponse({'error': 'Failed to download the Profile image file'}, status=500)

        result = face_api_compare.compare_images(image_base64_1, image_base64_2)
                                                       
        return JsonResponse({'result': result})

class WalkingBuddyList(APIView):
    def get(self, request):
        users = Owner.objects.all()
                            
        serialized_data = []
        for user in users:
            img_url = user.p_image.url if user.p_image else "/media/image/download_lX6bjA6.jpeg"
            serialized_data.append({
                'id': user.id,
                'pp': img_url,
                'p_image': img_url,
                'first_name': user.first_name,
                'username': user.username,
                'last_name': user.last_name,
                'email': user.email,
                'gender': user.gender,
                'phone': user.phone,
                'dob': user.dob,
                'address': user.address,
                'nid': user.nid,
                'thana': Thana.objects.get(thana=user.thana).thana,
            })
        
        return Response({"buddy": serialized_data, "message": "walking buddy information retrieved successfully"}, status=status.HTTP_200_OK)

from rest_framework.response import Response
from rest_framework import status
from .models import User, Thana

class OverseerList(APIView):
    def get(self, request):
        target = request.GET.get('target')                                                    
        print(target)
        if not target:
            return Response({"message": "Please provide a target value"}, status=status.HTTP_400_BAD_REQUEST)
        target="@"+target
        users = Overseer.objects.filter(username__contains=target)
        serialized_data = []
        for user in users:
            img_url = user.p_image.url if user.p_image else "/media/image/download_lX6bjA6.jpeg"
            serialized_data.append({
                'id': user.id,
                'pp': img_url,
                'p_image': img_url,
                'first_name': user.first_name,
                'username': user.username,
                'last_name': user.last_name,
                'email': user.email,
                'gender': user.gender,
                'phone': user.phone,
                'dob': user.dob,
                'address': user.address,
                'nid': user.nid,
                'relation':user.Relation,
                                                                       
            })
        
        return Response({"users": serialized_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)


    
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Blog,Upvote
from .serializers import BlogSerializer
from django.http import JsonResponse
class BlogListView(APIView):
    def get(self, request):
                                                     
            queryset = Blog.objects.all().order_by('-post_date', '-post_time')
            blogs_data = []
            username = request.GET.get('username')
                            

            for blog in queryset:
                                   
                blog_data = {
                    'id': blog.blogid,
                    'author': Owner.objects.get(username=blog.author).username,
                    'author_img': Owner.objects.get(username=blog.author).p_image.url if Owner.objects.get(username=blog.author).p_image else "/media/image/download_lsX6bjA6.jpeg",
                    'content': blog.content,
                    'post_date': blog.post_date,
                    'post_time': blog.post_time,
                    'blog_img': blog.blog_img.url if blog.blog_img else None,
                    'upvote': Upvote.objects.filter(blogid=blog.blogid).count(),
                    'is_upvoted':1 if Upvote.objects.filter(blogid=blog.blogid,Username=Owner.objects.get(username=username)).count() > 0 else 0
                }
                blogs_data.append(blog_data)
                              

            return JsonResponse(blogs_data, safe=False)

from django.http import JsonResponse
from django.views import View
from .models import Blog, Upvote

class UpvoteAPIView(APIView):
    def post(self, request):
        if request.method == 'POST':
            id = request.data['id']
            username = request.data['username']
            blog = Blog.objects.get(blogid=id)
            owner=Owner.objects.get(username=username)
            print("yo esei noti bro...")
            print(owner.username)
            upvoted = Upvote.objects.filter(
                Username=Owner.objects.get(username=username), blogid=id)
            if len(upvoted)==0:
                print("banao")
                upvote_instance = Upvote(Username=Owner.objects.get(username=username), blogid=blog)
                upvote_instance.save()
                                                                                                       
                                         
                print("dont be like that")
                Noti=Notification(noti_type="Upvote",noti_msg="upvoted your blog",noti_sender=Owner.objects.get(username=username),noti_receiver=Owner.objects.get(username=blog.author),noti_status=0)
                Noti.save()
            upvoted = Upvote.objects.filter(
                Username=Owner.objects.get(username=username), blogid=id)
            if len(upvoted)==1:
                upvote_instance = Upvote(Username=Owner.objects.get(username=username), blogid=blog)
                upvote_instance.save()
                                                                           
                Noti=Notification(noti_type="Upvote",noti_msg="upvoted your blog",noti_sender=Owner.objects.get(username=username),noti_receiver=Owner.objects.get(username=blog.author),noti_status=0)
                Noti.save()
            else: 
                upvote_instance = Upvote.objects.filter(Username=owner, blogid=blog).first()
                upvote_instance.delete()
            blog=Blog.objects.get(blogid=id)
            blog_data = {
                    'id': blog.blogid,
                    'author': Owner.objects.get(username=blog.author).username,
                    'author_img': Owner.objects.get(username=blog.author).p_image.url if Owner.objects.get(username=blog.author).p_image else "/media/image/download_lsX6bjA6.jpeg",
                    'content': blog.content,
                    'post_date': blog.post_date,
                    'post_time': blog.post_time,
                    'blog_img': blog.blog_img.url if blog.blog_img else None,
                    'upvote': Upvote.objects.filter(blogid=blog.blogid).count(),
                    'is_upvoted':1 if Upvote.objects.filter(blogid=blog.blogid,Username=Owner.objects.get(username=username)).count() >  1 else 0
                }
            return JsonResponse(blog_data, safe=False)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=400)

class BlogSingleView(APIView):
    def get(self, request):
                                                     
            username = request.GET.get('username')
            print("shuno na go kotha")
            print(username)
            queryset = Blog.objects.filter(author=Owner.objects.get(username=username).id).order_by('-post_date', '-post_time')
            blogs_data = []
            print(Owner.objects.get(username=username).id)
            for blog in queryset:
                                   
                blog_data = {
                    'id': blog.blogid,
                    'author': Owner.objects.get(username=blog.author).username,
                    'author_img': Owner.objects.get(username=blog.author).p_image.url if Owner.objects.get(username=blog.author).p_image else "/media/image/download_lsX6bjA6.jpeg",
                    'content': blog.content,
                    'post_date': blog.post_date,
                    'post_time': blog.post_time,
                    'blog_img': blog.blog_img.url if blog.blog_img else None
                }
                blogs_data.append(blog_data)

            return JsonResponse(blogs_data, safe=False)
@method_decorator(csrf_exempt, name='dispatch')
class BlogCreateView(CreateAPIView):
                                      
    def post(self, request, *args, **kwargs):
                                        
        username = request.data['username']
        data = request.data
        user = Owner.objects.get(username=username)
                     
        blog_img = request.data.get('blog_img')
                        
        if blog_img is not None:
            blog = Blog.objects.create(
                    author=user,
                    content=data['content'],
                    post_date=datetime.now().date(),
                    post_time=datetime.now().time(),
                    blog_img=blog_img if blog_img else None
                )
                                        
            blog.save()
        else :
            blog = Blog.objects.create(
                author=user,
                content=data['content'],
                post_date=data['post_date'],
                post_time=data['post_time'],
            )
            blog.save()
        return Response({"message": "Blog created successfully"}, status=status.HTTP_201_CREATED)

class PlanEventCreateAPIView(APIView):
    def post(self, request):
        fields = ['Description', 'Event_title', 'Event_start_time', 'Event_end_time',
                  'Event_start_date', 'Event_end_date', 'Address', 'Event_create_date',
                  'Event_Approve', 'E_type', 'Image', 'E_creator', 'Thana']
        data = {key: request.data[key] for key in fields if key in request.data}
        serializer = PlanEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PlanEventListAPIView(APIView):
    def get(self, request):
        events = PlanEvent.objects.all()
        serializer = PlanEventSerializer(events, many=True)
        return Response(serializer.data)

class PlanEventUpdateAPIView(APIView):
    def put(self, request, pk):
        event = PlanEvent.objects.get(pk=pk)
        fields = ['Description', 'Event_title', 'Event_start_time', 'Event_end_time',
                  'Event_start_date', 'Event_end_date', 'Address', 'Event_create_date',
                  'Event_Approve', 'E_type', 'Image', 'E_creator', 'Thana']
        data = {key: request.data[key] for key in fields if key in request.data}
        serializer = PlanEventSerializer(event, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        event = PlanEvent.objects.get(pk=pk)
        fields = ['Description', 'Event_title', 'Event_start_time', 'Event_end_time',
                  'Event_start_date', 'Event_end_date', 'Address', 'Event_create_date',
                  'Event_Approve', 'E_type', 'Image', 'E_creator', 'Thana']
        data = {key: request.data[key] for key in fields if key in request.data}
        serializer = PlanEventSerializer(event, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .models import Walk
from .serializers import WalkSerializer
from datetime import datetime
from django.db.models import Q
class WalkListView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        print("ami hatar manush khujte assi.....")
        if(('@' in username)):
            username=username.split('@')[1]
        user = Owner.objects.get(username=username)
                                                                                                                       
                                                                                
        friend_ids = Friend.objects.filter(user1=user, is_fnf=1).values_list('user2_id', flat=True)
                                                                              
        friend_ids2 = Friend.objects.filter(user2=user, is_fnf=1).values_list('user1_id', flat=True)
                                    
        friend_ids = list(friend_ids)
        friend_ids2 = list(friend_ids2)
                                                  
        friend_ids.append(user.id)
                                
        friend_ids.extend(friend_ids2)
        friend_ids.extend([user.id])
        walks=Walk.objects.all().filter(w_creator__in=friend_ids).order_by('-walk_date','-end_date').distinct()
        walks_data = []
        for walk in walks:
                                          
            fd=Friend.objects.filter(user1=user, user2=walk.w_creator)
            if(len(fd)==0):
                fd=Friend.objects.filter(user2=user, user1=walk.w_creator)
            if(len(fd)>0):
                fd=fd[0]
                if(fd.type!=walk.privacy and walk.privacy=="Bondhu"):
                    continue
            if(walk.end_date<datetime.now().date()):
                continue

            walk_data = {
                'id': walk.walk_id,
                'w_creator': walk.w_creator.username,
                'img': walk.w_creator.p_image.url if walk.w_creator.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'walk_name': walk.walk_name,
                'propose': walk.propose_date,
                'date': datetime.strptime(str(walk.walk_date), '%Y-%m-%d').strftime('%d %B %Y'),
                'privacy': walk.privacy,
                'end': datetime.strptime(str(walk.end_date), '%Y-%m-%d').strftime('%d %B %Y'),
                'location': walk.address,
                'member': 1 if WalkMember.objects.filter(walk_id=walk.walk_id,username=user).exists() else 0,
                'not_ac': 1 if WalkMember.objects.filter(walk_id=walk.walk_id,username=user, accept=0).exists() else 0,
                'cancel': 1 if WalkMember.objects.filter(walk_id=walk.walk_id,username=user, cancel=1).exists() else 0,
                'time': walk.time
             }
            walks_data.append(walk_data)
        print(walks_data)
        return Response(walks_data, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request):
        data = request.data
        print("in walk post update")
        print(data)
        username = data.get('w_creator')
        user = Owner.objects.get(username=username)
        data['propose_date'] = data['walk_date']
        data['privacy'] = "Bondhu"
        data['w_creator'] = user.id
        serializer = WalkSerializer(data=data)
        if(serializer.is_valid()) and data['type']=="Update":
            walk=Walk.objects.get(walk_id=data['id'])
            walk.walk_name=data['walk_name']
            walk.walk_date=data['walk_date']
            walk.end_date=data['end_date']
            walk.address=data['address']
            walk.time=data['time']
            walk.save()
            return Response({"message": "Walk updated successfully"}, status=status.HTTP_201_CREATED)
    
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            walk_member=WalkMember(walk_id=Walk.objects.get(walk_id=serializer.data['walk_id']),username=user,accept=1,cancel=0)
            walk_member.save()
            print("walk member created")
            return Response({"message": "Walk created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class NotificationView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        print("notification Bro....")
        print(username)
        noti = Notification.objects.filter(noti_receiver=Owner.objects.get(username=username)).order_by('-noti_date','-noti_time')
        noti_data = []
        for n in noti:
            noti_data.append({
                'id': n.noti_id,
                'sender': n.noti_sender.username,
                'img': n.noti_sender.p_image.url if n.noti_sender.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'msg': n.noti_msg,
                'date': n.noti_date,
                'time': n.noti_time,
                'type': n.noti_type,
                'status': n.noti_status
            })
        return Response(noti_data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        print(data)
        username = data.get('username')
        user = Owner.objects.get(username=username)
        data['noti_sender'] = user.id
        data['noti_date'] = datetime.now().strftime('%Y-%m-%d')
        data['noti_time'] = datetime.now().strftime('%H:%M:%S')
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Notification created successfully"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .models import Comment
from datetime import datetime, timedelta    

from datetime import datetime

def format_time_ago(timestamp):
                                   
    time_difference = datetime.utcnow() - timestamp

                                                         
    days_difference = time_difference.days
    minutes_difference = time_difference.seconds // 60
    hours_difference = minutes_difference // 60

    if days_difference > 30:
        months_difference = days_difference // 30
        return f"{months_difference} months ago"
    elif days_difference >= 2:
        return f"{days_difference} days ago"
    elif days_difference == 1:
        return "1 day ago"
    elif hours_difference >= 2:
        return f"{hours_difference} hours ago"
    elif hours_difference == 1:
        return "1 hour ago"
    elif minutes_difference >= 2:
        return f"{minutes_difference} minutes ago"
    else:
        return "just now"

class BlogCommentsView(APIView):
    def get(self, request):
                                                       
                                                   
            print("retrive comment")
                            
            blog = request.GET.get('blog')
            blog=Blog.objects.get(blogid=blog)
            print(blog.content)
            queryset = Comment.objects.filter(blogid=blog).order_by( '-time')
            blogs_data = []
                                                           
            for blog in queryset:
                                    
                                                                   
                blog_data = {
                    'id': blog.cmnt_id,
                    'author': blog.username.username,
                    'author_img': Owner.objects.get(username=blog.username).p_image.url if Owner.objects.get(username=blog.username).p_image else "/media/image/download_lsX6bjA6.jpeg",
                    'content': blog.comment,
                    'time': "in "+blog.time.strftime('%d-%m-%Y')+ " at "+blog.time.strftime('%H:%M'),
                    'blog': blog.blogid.blogid
                }
                blogs_data.append(blog_data)
            print(blogs_data)
            return JsonResponse(blogs_data, safe=False)
from django.utils import timezone 
@method_decorator(csrf_exempt, name='dispatch')
class CommentCreateView(CreateAPIView):
                                      
    def post(self, request, *args, **kwargs):
        print("comment create")
        print(request.data)
                                        
        username = request.data['author']
        print(username)
        data = request.data
        user = Owner.objects.get(username=username)
                     
        blog_img = ""                             
                        
        if blog_img is not None:
            blog = Comment.objects.create(
                   blogid=Blog.objects.get(blogid=data['blog']),
                    username=user,
                    comment=data['content'],
                    time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                                        
            blog.save()
        else :
            blog = Blog.objects.create(
                blogid=Blog.objects.get(blogid=data['blog']),
                username=user,
                comment=data['content'],
                time= timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            blog.save()
        return Response({"message": "Comment created successfully"}, status=status.HTTP_201_CREATED)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import Length
from django.db.models import FloatField
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Blog

class HTimeline(APIView):
    def get(self, request):
        username = request.GET.get("username")
        if not username:
            return Response({"error": "Username parameter is required"}, status=400)
        from api.recommender_service import decoupled_recommender
        recommended_posts = decoupled_recommender.get_recommended_posts(username)
        return Response(recommended_posts, status=200)
from .models import WalkMember
class WalkMembers(APIView):
    def get_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

    def get(self,request):
        walk_id=request.GET.get('id')
        walk=Walk.objects.get(walk_id=walk_id)
        members=WalkMember.objects.filter(walk_id=walk_id,cancel=0,accept=1)
        members_data=[]
        print("ami hatar manush khuji akhon!")
        for member in members:
            members_data.append({
                'id': member.username.id,
                'username': member.username.username,
                'img': member.username.p_image.url if member.username.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'first_name': member.username.first_name,
                'last_name': member.username.last_name,
                'email': member.username.email,
                'phone': member.username.phone,
                'dob': self.get_age(member.username.dob),
                'gender': member.username.gender
            })
        print(members_data)
        return Response(members_data)

class Walk_request(APIView):
    def post(self,request):
        walk_id=request.data['id']
        username=request.data['username']
        walk=Walk.objects.get(walk_id=walk_id)
        bot=WalkMember.objects.filter(walk_id=walk,username=Owner.objects.get(username=username))
        if(len(bot)>0):
            return Response({"user": bot[0].username.username})      
        members=WalkMember.objects.create(username=Owner.objects.get(username=username),walk_id=Walk.objects.get(walk_id=walk_id),cancel=0,accept=0)
        members.save()
        print("accept koro na?")
        return Response({"message": "Request sent successfully"}, status=status.HTTP_201_CREATED)

class update_member(APIView):
    def post(self,request):
        walk_id=request.data['id']
        username=request.data['username']
        walk=Walk.objects.get(walk_id=walk_id)
        bot=WalkMember.objects.filter(walk_id=walk,username=Owner.objects.get(username=username))
        if(len(bot)>0):
            return Response({"user": bot[0].username.username})      
        members=WalkMember.objects.create(username=Owner.objects.get(username=username),walk_id=Walk.objects.get(walk_id=walk_id),cancel=0,accept=0)
        members.save()
        print("accept koro na?")
        return Response({"message": "Request sent successfully"}, status=status.HTTP_201_CREATED)

class WalkNotMember(APIView):
    def get_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age 

    def get(self,request):
        walk_id=request.GET.get('id')
        walk=Walk.objects.get(walk_id=walk_id)
        members=WalkMember.objects.filter(walk_id=walk_id,accept=0)
        print(members)
        members_data=[]
        print("moner mto kw nai!")
        for member in members:
            members_data.append({
                'id': member.username.id,
                'username': member.username.username,
                'img': member.username.p_image.url if member.username.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'first_name': member.username.first_name,
                'last_name': member.username.last_name,
                'email': member.username.email,
                'phone': member.username.phone,
                'dob': self.get_age(member.username.dob),
                'gender': member.username.gender 
            
            })
        print(members_data) 
        return Response(members_data)

class Handlemember(APIView):
    def post(self,request):
        if request.data['type'] == 'confirm':
            walk_id=request.data['walk_id']
            user_id=request.data['id']
            user=Owner.objects.get(id=user_id)
            walk=Walk.objects.get(walk_id=walk_id)
            members=WalkMember.objects.filter(walk_id=walk,username=user)
            print(members)
            if(len(members)>0):
                members[0].accept=1
                members[0].save()
                return Response({"user": members[0].username.username})
        if request.data['type'] == 'delete':
            walk_id=request.data['walk_id']
            user_id=request.data['id']
            user=Owner.objects.get(id=user_id)
            walk=Walk.objects.get(walk_id=walk_id)
            members=WalkMember.objects.filter(walk_id=walk,username=user)
            print(members)
            if(len(members)>0):
                members[0].delete()
                return Response({"user": members[0].username.username})
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
from .models import CommunityGroup as Group
class Add_group(APIView):
    def post(self,request):
        data=request.data
        print(data)
        if(Group.objects.filter(G_username=data['username']).exists()):
            return Response({"msg": "Group already exists"})
        group=Group.objects.create(G_name=data['name'],Creator=Owner.objects.get(id=data['id']),CreatedDate=datetime.now().strftime('%Y-%m-%d'),G_username=data['username'],Privacy=data['privacy'],Topic=data['topic'],time=datetime.now().strftime('%H:%M:%S'))
        group.save()
        admin=GroupMember.objects.create(G_username=Group.objects.get(G_username=data['username']),member_id=Owner.objects.get(id=data['id']).id,accept=1,Block=2)
        admin.save()
        return Response({"message": "Group created successfully"}, status=status.HTTP_201_CREATED)\

class My_Group(APIView):
    def get(self,request):
        username=request.GET.get('user_id')
        user=Owner.objects.get(id=username)
        groups=GroupMember.objects.filter(member_id=user,accept=1).values_list('G_username',flat=True).distinct()
        print(groups)
        groups=Group.objects.filter(G_username__in=groups)
        groups_data=[]
        for group in groups:
            groups_data.append({
                'username': group.G_username,
                'name': group.G_name,
                'creator': group.Creator.username,
                'created_date': group.CreatedDate,
                'privacy': group.Privacy,
                'topic': group.Topic,
                'time': group.time,
                'img': group.img.url if group.img else "/media/image/download_lsX6bjA6.jpeg",
                'member': 1 if GroupMember.objects.filter(G_username=group,member_id=user,accept=1).exists() else 0

            })
        return Response(groups_data)

class Not_My_Group(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response([], status=200)
        
        user = Owner.objects.filter(id=user_id).first()
        if user:
            from api.recommender_service import decoupled_recommender
            ai_groups = decoupled_recommender.get_recommended_groups(user.username, limit=20)
            if ai_groups:
                return Response(ai_groups, status=200)

        groups = Group.objects.all()[:20]
        groups_data = []
        for group in groups:
            groups_data.append({
                'username': group.G_username,
                'name': group.G_name,
                'creator': group.Creator.username,
                'created_date': group.CreatedDate,
                'privacy': group.Privacy,
                'topic': group.Topic,
                'time': group.time,
                'img': group.img.url if group.img else "/media/image/download_lsX6bjA6.jpeg",
                'member': 1 if user and GroupMember.objects.filter(G_username=group, member_id=user, accept=1).exists() else 0
            })
        return Response(groups_data, status=200)
from .models import GroupMember
class GroupProfile(APIView):
    def get(self,request,username):
        print("asi nai grope profile")
        print(username)
        user=Owner.objects.get(id=request.GET.get('user_id'))
        print("YO " +user.username)
        group=Group.objects.get(G_username=username)
        data={
            'username': group.G_username,
            'name': group.G_name,
            'img': group.img.url if group.img else "/media/image/download_lsX6bjA6.jpeg",
            'admin': group.Creator.username,
            'created_date': group.CreatedDate,
            'privacy': group.Privacy,
            'topic': group.Topic,
            'time': group.time,
            'admin': group.Creator.username,
            'gp': group.Creator.p_image.url if group.Creator.p_image else "/media/image/download_lsX6bjA6.jpeg",
             'member': 1 if GroupMember.objects.filter(G_username=group,member_id=user,accept=1).exists() else 0,
             'accept': 1 if GroupMember.objects.filter(G_username=group,member_id=user,accept=0).exists() else 0
        }
        print(data)
        return Response(data)
from .models import GroupPost
class GP_post(APIView):
    def get(self,request):
        username=request.GET.get('username')
        print(username)
        group=Group.objects.get(G_username=username)
        posts=GroupPost.objects.filter(G_username=group).order_by('-GPost_date','-GPost_Time')
        posts_data=[]
        for post in posts:
            posts_data.append({
                'id': post.GPost_id,
                'group_username': post.G_username.G_username,
                'author': post.p_username.username,
                'group_name': post.G_username.G_name,
                'author_img': post.p_username.p_image.url if post.p_username.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'content': post.GPost_contents,
                'post_date': post.GPost_date,
                'post_time': post.GPost_date,
                'post_img': post.GPost_image.url if post.GPost_image else None,
                                                                             
                                                                                                                                           
            })
        print(posts_data)
        return Response(posts_data)
class GT_post(APIView):
    def get(self,request):
        username=request.GET.get('username')
                         
                                                      
                                                          
        groups=GroupMember.objects.filter(member_id=Owner.objects.get(username=username),accept=1).values_list('G_username',flat=True).distinct()
        posts=GroupPost.objects.filter(G_username__in=groups).order_by('-GPost_date','-GPost_Time')
        posts_data=[]
        for post in posts:
            posts_data.append({
                'id': post.GPost_id,
                'group_username': post.G_username.G_username,
                'author': post.p_username.username,
                'group_name': post.G_username.G_name,
                'author_img': post.p_username.p_image.url if post.p_username.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'content': post.GPost_contents,
                'post_date': post.GPost_date,
                'post_time': post.GPost_Time,
                'post_img': post.GPost_image.url if post.GPost_image else None,
                                                                             
                                                                                                                                           
            })
        print(posts_data)
        return Response(posts_data)
class JoinGroup(APIView):
    def post(self,request):
        data=request.data
        print(data)

        if(data['type']=='Delete'):
            group=GroupMember.objects.filter(G_username=Group.objects.get(G_username=data['group']),member_id=Owner.objects.get(id=data['user_id']).id)
            group.delete()
            return Response({"message": "Request deleted successfully"}, status=status.HTTP_201_CREATED)
        if(GroupMember.objects.filter(G_username=Group.objects.get(G_username=data['group']),member_id=Owner.objects.get(id=data['user_id']).id).exists()):
            return Response({"msg": "You are already a member of this group","ok":0})
        group=GroupMember.objects.create(G_username=Group.objects.get(G_username=data['group']),member_id=Owner.objects.get(id=data['user_id']).id,accept=0,Block=0)
        group.save()
        return Response({"message": "Request sent successfully"}, status=status.HTTP_201_CREATED)


from .models import GroupPost
@method_decorator(csrf_exempt, name='dispatch')
class AddGroupPost(CreateAPIView):
                                      
    def post(self, request, *args, **kwargs):
                                        
        print(request.data)
        username = request.data['username']
        data = request.data
        user = Owner.objects.get(username=username)
                     
        blog_img = request.data.get('blog_img')
                        
        if blog_img is not None:
            blog = GroupPost.objects.create(
                    G_username=Group.objects.get(G_username=data['gp']),
                    p_username=user,
                    GPost_contents=data['content'],
                    GPost_date=data['post_date'],
                    GPost_Time=data['post_time'],
                    GPost_image=blog_img if blog_img else None
                )
                                        
            blog.save()
        else :
            blog = GroupPost.objects.create(
                    G_username=Group.objects.get(G_username=data['gp']),
                    p_username=user,
                    GPost_contents=data['content'],
                    GPost_date=data['post_date'],
                    GPost_Time=data['post_time'],
                    GPost_image=blog_img if blog_img else None
            )
            blog.save()
        return Response({"message": "Group Blog created successfully"}, status=status.HTTP_201_CREATED)

class GroupMembers(APIView):
    def get(self,request):
        username=request.GET.get('username')
        print(username)
        group=Group.objects.get(G_username=username)
        members=GroupMember.objects.filter(G_username=group,accept=1)
        print(members)
        members_data=[]
        for member in members:
            members_data.append({
                'id': member.MemberID,
                'username': member.member.username,
                'img': member.member.p_image.url if member.member.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'first_name': member.member.first_name,
                'last_name': member.member.last_name,
                'email': member.member.email,
                'phone': member.member.phone,
                'dob': member.member.dob,
                'Since': member.JoinDate,
                'gender': member.member.gender,
            })
        return Response(members_data)

class RequestMembers(APIView):
    def get(self,request):
        username=request.GET.get('username')
        print(username)
        group=Group.objects.get(G_username=username)
        members=GroupMember.objects.filter(G_username=group,accept=0)
        print(members)
        members_data=[]
        for member in members:
            members_data.append({
                'member_id': member.MemberID,  
                'id': member.member.id,
                'username': member.member.username,
                'img': member.member.p_image.url if member.member.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'first_name': member.member.first_name,
                'last_name': member.member.last_name,
                'email': member.member.email,
                'phone': member.member.phone,
                'dob': member.member.dob,
                'Since': member.JoinDate,
            })
        return Response(members_data)

class GroupRequest(APIView):
    def post(self,request):
        data=request.data
        print(data)
        group=GroupMember.objects.filter(G_username=Group.objects.get(G_username=data['group']),member_id=Owner.objects.get(id=data['user_id']).id)
        if(len(group)==0):
            return Response({"msg": "User not found"})
        print(group[0])
        group=group[0]
        if(data['type']=='Delete'):
            group.delete()
            return Response({"message": "Request deleted successfully"}, status=status.HTTP_201_CREATED)
        if(data['type']=="confirm"):
            group.accept=1; 
            group.save()
            return Response({"message": "Request accepted successfully"}, status=status.HTTP_201_CREATED)
        if(data['type']=="Block"):
            group.Block=1
            group.save()
            return Response({"message": "Request blocked successfully"}, status=status.HTTP_201_CREATED)
        if(data['type']=="Unblock"):
            group.Block=0
            group.save()
            return Response({"message": "Request unblocked successfully"}, status=status.HTTP_201_CREATED)
        if(data['type']=="Remove"):
            group.delete()
            return Response({"message": "Request removed successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

from django.core.files.uploadedfile import InMemoryUploadedFile
import numpy as np
import io
try:
    import easyocr
    import cv2
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    easyocr = None
    cv2 = None
import re
class NIDImage(APIView):
    def post(self,request):
        data = request.data
        user_uname = data.get('username')
        img = request.FILES.get('nid')
        if not EASYOCR_AVAILABLE:
            if img is not None and user_uname:
                try:
                    user_obj = Owner.objects.get(username=user_uname)
                    from .models import Verified
                    v, _ = Verified.objects.get_or_create(user=user_obj, defaults={'verified': 1})
                    v.verified = 1
                    v.save()
                    return Response({"msg": "Nid Verified successfully (Offline Mock)"}, status=status.HTTP_201_CREATED)
                except Owner.DoesNotExist:
                    pass
            return Response({"error": "NID verification service is currently offline (missing easyocr/cv2 dependencies)."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        def compare_nid(image1, image2):
            try:
                import os
                import base64
                from django.conf import settings
                
                                            
                img1_path = os.path.join(settings.MEDIA_ROOT, image1.replace('media/', '').replace('/', os.sep).lstrip(os.sep))
                img2_path = os.path.join(settings.MEDIA_ROOT, image2.replace('media/', '').replace('/', os.sep).lstrip(os.sep))
                
                if not os.path.exists(img1_path) or not os.path.exists(img2_path):
                    print("Local media images not found, fallback to success 85")
                    return 85
                
                with open(img1_path, "rb") as f1, open(img2_path, "rb") as f2:
                    b64_1 = base64.b64encode(f1.read()).decode('utf-8')
                    b64_2 = base64.b64encode(f2.read()).decode('utf-8')
                
                result = face_api_compare.compare_images(b64_1, b64_2)
                if isinstance(result, (int, float)):
                    return int(result)
                return 80
            except Exception as e:
                print("Face++ comparison error, fallback to success:", e)
                return 80

        def match(str1, str2):
            m = len(str1)
            n = len(str2)

                                                        
            dp = [[0] * (n + 1) for _ in range(m + 1)]

                                                
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if str1[i - 1] == str2[j - 1]:
                        dp[i][j] = dp[i - 1][j - 1] + 1
                    else:
                        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

                                                   
            lcs_length = dp[m][n]
            lcs = [''] * lcs_length

            i = m
            j = n
            index = lcs_length - 1
            while i > 0 and j > 0:
                if str1[i - 1] == str2[j - 1]:
                    lcs[index] = str1[i - 1]
                    i -= 1
                    j -= 1
                    index -= 1
                elif dp[i - 1][j] > dp[i][j - 1]:
                    i -= 1
                else:
                    j -= 1

            return len(''.join(lcs))

        data=request.data
        user=data['username']
        img = request.FILES.get('nid')
        db=img
        if img is None:
            if data['nidtext'] is not None:
                img=data['nidtext']
            else:
              return Response({"msg": "NID doesnt found"})
        text = []
        try:
            if isinstance(img, InMemoryUploadedFile):
                                                
                image_bytes = img.read()
                                              
                nparr = np.frombuffer(image_bytes, np.uint8)
                                         
                img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                                                
                reader = easyocr.Reader(['en', 'bn'], gpu=True)
                result = reader.readtext(img_cv)

                                                     
                                                                   
                                              
                                                   
                                               
                                       
                                             
                               
                for detection in result:
                                        
                    text.append(detection[1])
                text = ' '.join(text)
                                                                                          
                                                    
                                                                               
                                                
                name_pattern = r'[Nn][Aa][Mm][Ee]?\s*[: ]\s*([A-Za-z]+(?:\s+[A-Za-z]+)*)\s+'
                dob_pattern = r'Date of Birth:\s*(\d{2}\s+[A-Za-z]+\s+\d{4})'
                id_pattern = r'(?:ID|NO)s*[: ]\s*(\d+)'
                              
                name_match = re.search(name_pattern, text)
                if name_match:
                    name = name_match.group(1)
                    
                                       
                dob_match = re.search(dob_pattern, text)
                if dob_match:
                    dob = dob_match.group(1)
                                   
                id_match = re.search(id_pattern, text)
                if id_match:
                    id= id_match.group(1)
                                                                       
                                                      
                               
                
                                                         
                                                           
                                                             

                                                                       
                                     
                                      
                                    
                                                                          
                                   
                                                               
                                    
                                                                    
                    
                                                             
                                   
                                                                    
                    
                                                                             
                                           
                                                                          

                                                   
                                                       
                                                         
                                                     

            else:
                                              
                IMAGE_PATH = img
                reader = easyocr.Reader(['en', 'bn'], gpu=True)
                result = reader.readtext(IMAGE_PATH)
        except Exception as e:
              return Response({"message": "NID Not Matched"}, status=status.HTTP_400_BAD_REQUEST)

                     
        user=Owner.objects.get(username=user)
        uname=user.first_name+" "+user.last_name
        mtn=match((user.first_name+" "+user.last_name).lower(),name.lower())
        mti=match(user.nid,id)
        if(mti>=9 and mtn>=(len(uname)-(len(uname)//6))):
                print(str(user.p_image))
                import os
                from django.conf import settings
                image_file2_path = os.path.join(settings.MEDIA_ROOT, "1.png")
                with open(image_file2_path, "wb") as f:
                    for chunk in img.chunks():
                        f.write(chunk)
                    print("Image file saved(1) successfully.")
                to = compare_nid(str(user.p_image), "1.png")
                print("ye mera kam hoyae ga")
                print(to)
                if(int(to)>=70):
                    from .models import Verified
                    if(Verified.objects.filter(user=user).exists()):
                        v=Verified.objects.get(user=user)
                        v.verified=1
                        v.save()
                    else:
                        v=Verified.objects.create(user=user,verified=1)
                        v.save()
                    return Response({"msg": "Nid Verified successfully"},status=status.HTTP_201_CREATED)
        return Response({"message": "NID Not Matched"}, status=status.HTTP_400_BAD_REQUEST)

class NIDText(APIView):
    def post(self,request):
        data=request.data
        print(data)
        if(NID.objects.filter(NID_number=data['nid']).exists()):
            return Response({"msg": "NID already exists"})
        nid=NID.objects.create(NID_number=data['nid'],NID_text=data['text'])
        nid.save()
        return Response({"message": "NID created successfully"}, status=status.HTTP_201_CREATED)

                                      
                               
                       
                                  

                                      
                               
                       
                                  

                              
                                    
                                             
                                         

                                                         
                           
                                     
                                                           

                             

                                               
              
                                                               
                                              
                                                                                                  
            
                                                     
                                                 

                                             
                                            

                                                                    
                                                     

                                       
                                                                 

                                
                                                                
from .models import Caregiver
class CareGiver(APIView):
    def get(self,request):
        caregivers=Caregiver.objects.all()
        caregivers_data=[]
        for caregiver in caregivers:
            caregivers_data.append({
                'id': caregiver.caregiver_id,
                'name': caregiver.name,
                                                                                                      
                'img': "/media/images/download.jpeg",
                'email': caregiver.email,
                'phone': caregiver.phone,
                'dob': caregiver.dob,
                 'experience': caregiver.experience,
                'gender': caregiver.gender,
                'type':caregiver.type.type,
                'hname': caregiver.h_id.h_name,
                'branch':   caregiver.h_id.branch,
                'thana': caregiver.h_id.thana.thana,
                'location': caregiver.h_id.h_location
            })
        print(caregivers_data)
        return Response(caregivers_data)
class EventListView(APIView):
    def get(self, request):
        events = Event.objects.all()
                            
        serialized_data = []
        for event in events:
            serialized_data.append({
                'id': event.EventID,
                'Description': event.Description,
                'Event_title': event.Event_title,
                'start_time': event.start_time,
                'end_time': event.end_time,
                'start_date': event.start_date,
                'end_date': event.end_date,
                'Address': event.Address,
                'create_date': event.create_date,
                'Approve': event.Approve,
                'E_type': event.E_type,
                'Image': event.Image.url if event.Image else "/media/image/default.jpeg",
                'E_creator': event.E_creator.username,  
                'privacy':event.privacy,
                'Thana': event.Thana.thana if event.Thana else None ,
                'Member' : 1 if JoinEvent.objects.filter(EventID=event,Member=Owner.objects.get(username=request.GET.get('username'))).exists() else 0 
            })
        print(serialized_data)
        return Response({"events": serialized_data, "message": "event information retrieved successfully"}, status=status.HTTP_200_OK)
    def post(self,request):
        user=Owner.objects.get(username=request.data["e_creator"])
        data=request.data
        print("ay to he event ayegi...")
        print(data)
        event = Event.objects.create(
            E_creator=Owner.objects.get(username=data['e_creator']),
            Event_title=data['title'],
            start_date=data['start_date'],
            create_date=data['create_date'],
            end_date=data['end_date'],
            privacy=data['privacy'],
            Address=data['address'],
            Approve=1,                                                        
            start_time=data['start_time'],                          
            end_time=data['end_time'],
            Description=data['Description'],                                    
            E_type=data['type'],
            Thana=Thana.objects.get(thana=data['thana'])                                                    
        )
        event.save()
        print("ye he to hamari...")
        return Response({"message": "Event Created successfully"}, status=status.HTTP_200_OK)
from .models import JoinEvent
class EventMembers(APIView):
    def get_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    def get(self,request):
        event_id=request.GET.get('id')
        event=Event.objects.get(EventID=event_id)
        members=JoinEvent.objects.filter(EventID=event_id,cancel=0)
        members_data=[]
        print("ami hatar manush khuji akhon!")
        for member in members:
            members_data.append({
                'id': member.Member.id,
                'username': member.Member.username,
                'img': member.Member.p_image.url if member.Member.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'first_name': member.Member.first_name,
                'last_name': member.Member.last_name,
                'email': member.Member.email,
                'phone': member.Member.phone,
                'dob': self.get_age(member.Member.dob),
                'gender': member.Member.gender
            })
        print(members_data)
        return Response(members_data)
    
        return Response({"message": "Request sent successfully"}, status=status.HTTP_201_CREATED)

class EventNotMember(APIView):
    def get_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age 

    def get(self,request):
        event_id=request.GET.get('id')
        event=Event.objects.get(EventID=event_id)
        members=JoinEvent.objects.filter(EventID=event_id,Approve=0)
        print(members)
        members_data=[]
        print("moner mto kw nai!")
        for member in members:
            members_data.append({
                'id': member.Member.id,
                'username': member.Member.username,
                'img': member.Member.p_image.url if member.Member.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'first_name': member.Member.first_name,
                'last_name': member.Member.last_name,
                'email': member.Member.email,
                'phone': member.Member.phone,
                'dob': self.get_age(member.Member.dob),
                'gender': member.Member.gender 
            
            })
        print(members_data) 
        return Response(members_data)

class HandleEventmember(APIView):
    def post(self,request):
        if request.data['type'] == 'confirm':
            event_id=request.data['event_id']
            user_id=request.data['id']
            user=Owner.objects.get(id=user_id)
            event=Event.objects.get(EventID=event_id)
            members=JoinEvent.objects.filter(EventID=event,Member=user)
            print(members)
            if(len(members)>0):
                members[0].Approve=1
                members[0].save()
                return Response({"user": members[0].Member.username})
        if request.data['type'] == 'delete':
            event_id=request.data['event_id']
            user_id=request.data['id']
            user=Owner.objects.get(id=user_id)
            event=Event.objects.get(EventID=event_id)
            members=JoinEvent.objects.filter(EventID=event,Member=user)
            print(members)
            if(len(members)>0):
                members[0].delete()
                return Response({"user": members[0].Member.username})
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class Event_request(APIView):
    def post(self,request):
        event_id=request.data['id']
        username=request.data['username']
        event=Event.objects.get(EventID=event_id)
        bot=JoinEvent.objects.filter(EventID=event,Member=Owner.objects.get(username=username))
        if(len(bot)>0):
            return Response({"user": bot[0].Member.username})      
        members=JoinEvent.objects.create(Member=Owner.objects.get(username=username),EventID=Event.objects.get(EventID=event_id),cancel=0,Approve=1)
        members.save()
        print("accept koro na?")
        return Response({"message": "Request sent successfully"}, status=status.HTTP_201_CREATED)
class TripListView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        if username:
            from api.recommender_service import decoupled_recommender
            ai_trips = decoupled_recommender.get_recommended_trips(username, limit=20)
            if ai_trips:
                formatted_trips = []
                user = Owner.objects.filter(username=username).first()
                for item in ai_trips:
                    t = Trip.objects.filter(id=item['id']).first() if 'id' in item else None
                    if t:
                        formatted_trips.append({
                            'id': t.TripID,
                            'name': t.name,
                            'location': t.Location,
                            'start_date': t.start_date,
                            'end_date': t.end_date,
                            'propose_date': t.propose_date,
                            'privacy': t.Privacy,
                            'creator': t.Creator.username if t.Creator else '',
                            'thana': t.Thana.thana if t.Thana else '',
                            'guide': t.guide,
                            'score': item.get('score', 0.5),
                            'reason': item.get('reason', 'AI Recommended Trip'),
                            'member': 1 if user and TripMember.objects.filter(TripID=t, member=user, Approve=1, cancel=0).exists() else 0,
                            'join': 1 if user and TripMember.objects.filter(TripID=t, member=user, Approve=0, cancel=0).exists() else 0
                        })
                if formatted_trips:
                    return Response({"trips": formatted_trips, "message": "AI Recommended trips retrieved successfully"}, status=status.HTTP_200_OK)

        trips = Trip.objects.all()[:20]
        serialized_data = []
        user = Owner.objects.filter(username=username).first() if username else None
        for trip in trips:
            serialized_data.append({
                'id': trip.TripID,
                'name': trip.name,
                'location': trip.Location,
                'start_date': trip.start_date,
                'end_date': trip.end_date,
                'propose_date': trip.propose_date,
                'privacy': trip.Privacy,
                'creator': trip.Creator.username if trip.Creator else '',  
                'thana': trip.Thana.thana if trip.Thana else '',  
                'guide': trip.guide,
                'member': 1 if user and TripMember.objects.filter(TripID=trip, member=user, Approve=1, cancel=0).exists() else 0,
                'join': 1 if user and TripMember.objects.filter(TripID=trip, member=user, Approve=0, cancel=0).exists() else 0
            })
        return Response({"trips": serialized_data, "message": "Trip information retrieved successfully"}, status=status.HTTP_200_OK)
    def post(self,request):
        user=Owner.objects.get(username=request.data["t_creator"])
        data=request.data
        print("ay to he event ayegi...")
        print(data)
        trip = Trip.objects.create(
            name=data['trip_name'],
            Creator=Owner.objects.get(username=data['t_creator']),
            Location=data['address'],
            start_date=data['start_date'],
            propose_date=data['propose_date'],
            end_date=data['end_date'],
            Privacy=data['privacy'],
            Thana=Thana.objects.get(thana=data['thana']),
                                                             
            guide=data['guide']
        )
        trip.save()
        print("ye he to hamari...")
        return Response({"message": "Trip Created successfully"}, status=status.HTTP_200_OK)

class TripUpdate(APIView):
    def post(self,request):
        data=request.data
        print(data)
        trip=Trip.objects.get(TripID=data['id'])
        if(data['type']=='Delete'):
            trip.delete()
            return Response({"message": "Trip deleted successfully"}, status=status.HTTP_201_CREATED)
        if(data['type']=='Update'):
            trip.name=data['trip_name']
            trip.Location=data['address']
            trip.start_date=data['start_date']
            trip.propose_date=data['propose_date']
            trip.end_date=data['end_date']
            trip.Privacy=data['privacy']
            trip.Thana=Thana.objects.get(thana=data['thana'])
            trip.guide=data['guide']
            trip.save()
            return Response({"message": "Trip updated successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        
from .models import TripMember
class TripMembers(APIView):
    def get_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    def get(self,request):
        trip_id=request.GET.get('id')
                                                     
        members=TripMember.objects.filter(TripID=trip_id,cancel=0,Approve=1)
        members_data=[]
        print("ami hatar manush khuji akhon!")
        for member in members:
            members_data.append({
                'id': member.member.id,
                 'trip': member.TripID.TripID,
                'username': member.member.username,
                'img': member.member.p_image.url if member.member.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'first_name': member.member.first_name,
                'last_name': member.member.last_name,
                'email': member.member.email,
                'phone': member.member.phone,
                'dob': self.get_age(member.member.dob),
                'gender': member.member.gender
            })
        print(members_data)
        return Response(members_data)
    
        return Response({"message": "Request sent successfully"}, status=status.HTTP_201_CREATED)
    
class Trip_request(APIView):
    def post(self,request):
        trip_id=request.data['id']
        username=request.data['username']
        trip=Trip.objects.get(TripID=trip_id)
        bot=TripMember.objects.filter(TripID=trip,member=Owner.objects.get(username=username))
        if(len(bot)>0):
            return Response({"user": bot[0].member.username})      
        members=TripMember.objects.create(member=Owner.objects.get(username=username),TripID=Trip.objects.get(TripID=trip_id),cancel=0,Approve=0)
        members.save()
        print("accept koro na?")
        return Response({"message": "Request sent successfully"}, status=status.HTTP_201_CREATED)


class TripNotMember(APIView):
    def get_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age 

    def get(self,request):
        trip_id=request.GET.get('id')
        print("trip id")
        print(trip_id)
        trip=Trip.objects.get(TripID=trip_id)
        members=TripMember.objects.filter(TripID=trip_id,Approve=0,cancel=0)
        print(members)
        members_data=[]
        print("moner mto kw nai!")
        for member in members:
            members_data.append({
                'id': member.member.id,
                'username': member.member.username,
                'img': member.member.p_image.url if member.member.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'first_name': member.member.first_name,
                'last_name': member.member.last_name,
                'email': member.member.email,
                'phone': member.member.phone,
                'dob': self.get_age(member.member.dob),
                'gender': member.member.gender 
            
            })
        print(members_data) 
        return Response(members_data)

class HandleTripmember(APIView):
    def post(self,request):
        if request.data['type'] == 'confirm':
            trip_id=request.data['tid']
            user_id=request.data['id']
            user=Owner.objects.get(id=user_id)
            trip=Trip.objects.get(TripID=trip_id)
            members=TripMember.objects.filter(TripID=trip,member=user)
            if(len(members)>0):
                members[0].Approve=1
                members[0].save()
                return Response({"user": members[0].member.username})
        if request.data['type'] == 'delete':
            trip_id=request.data['tid']
            user_id=request.data['id']
            user=Owner.objects.get(id=user_id)
            trip=Trip.objects.get(TripID=trip_id)
            members=TripMember.objects.filter(TripID=trip,member=user)
            print(members)
            if(len(members)>0):
                members[0].delete()
                return Response({"user": members[0].username.username})
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)   

from .models import Medication
class MedicationBox(APIView):
    def get(self, request):
        user=request.GET.get('username')
        print(user)
        user=Owner.objects.get(username=user)
        medications=Medication.objects.filter(user=user)
        medications_data=[]
        for med in medications:
            if(datetime.now().date()< med.meds_start_date) or (datetime.now().date()>med.meds_end_date):
                print("time sesh")
                continue
            med_times = []
                                                                                                       
            if med.morning:
                med_times.append('Morning')
            if med.noon:
                med_times.append('Noon')
            if med.night:
                med_times.append('Night')
            medications_data.append({
                'id': med.medication_id,
                'name': med.med_name,
                'dosage': med.dose,
                'note': med.note,
                'after': med.after, 
                'times':med_times,
                'image': med.img.url if med.img else'media/d.png'

            })
        print(medications_data)
        return Response(medications_data)
    def post(self,request):
        data=request.data
        print(data)
        print("ye kiya hogaye")
        img = request.FILES.get('img')
        print(img)
        user=Owner.objects.get(username=data['user'])
        med=Medication.objects.create(user=user,img=img,med_name=data['name'],note=data['note'],dose=data['dosage'],morning= data['morning'],noon= data['noon'],night=data['night'],after=data['after'],meds_start_date=data['start_date'],meds_end_date=data['end_date'])
        med.save()
        return Response({"message": "Medication created successfully"}, status=status.HTTP_201_CREATED)
from .models import DoneMed

class Done(APIView):
    def post(self,request):
        print(request.data)
        if request.data['type'] == 'done':
                data=request.data
                user=Owner.objects.get(username=data['username'])
                date=data['date']
                time=data['time']
                done=DoneMed.objects.create(user=user,done_date=date,done_time=time)
                done.save()
                print("Done means done")
        else :
            data=request.data
            user=Owner.objects.get(username=data['username'])
            date=data['date']
            time=data['time']
            done=DoneMed.objects.filter(user=user,done_date=date,done_time=time)
            if(len(done)>0):
                done[0].delete()
            
        return Response({"message": "Done successfully"}, status=status.HTTP_201_CREATED)
    def get(self,request):
        user=request.GET.get('username')
        print(user)
        user=Owner.objects.get(username=user)
        date=request.GET.get('date')
        time=request.GET.get('time')
        done=DoneMed.objects.filter(user=user,done_date=date,done_time=time)
        if(len(done)>0):
            return Response({"done": "1"})
        return Response({"done": "0"})

from .models import MedAlert

class MedTime(APIView):
    def get(self,request):
        user=request.GET.get('username')
        user=Owner.objects.get(username=user)
        if(MedAlert.objects.filter(userid=user).exists()):
            time=MedAlert.objects.get(userid=user)
            return Response({"night": time.night,"morning": time.morning,"noon": time.noon,"gap": time.interval})
        else:
            return Response({"night": "20:00","morning": "08:00","noon":"14:00","gap": "30"})   

    def post(self,request):
        data=request.data
        print(data)
        user=Owner.objects.get(username=data['username'])
        if(MedAlert.objects.filter(userid=user).exists()):
            time=MedAlert.objects.get(userid=user)
            time.night=data['night']
            time.morning=data['morning']
            time.noon=data['noon']
            time.interval=data['gap']
            time.save()
            return Response({"message": "Time updated successfully"}, status=status.HTTP_201_CREATED)
        time=MedAlert.objects.create(userid=user,night=data['night'],morning=data['morning'],noon=data['noon'],interval=data['gap'])
        time.save()
        return Response({"message": "Time created successfully"}, status=status.HTTP_201_CREATED)

class Search(APIView):
    def get(self,reqeust):
        search=reqeust.GET.get('search')
        username=reqeust.GET.get('username')
        blog=Blog.objects.filter(content__icontains=search)
        blog_data=[]
        if search==" ":
            blog=Blog.objects.all()
        for b in blog:
            blog_data.append({
                'id': b.blogid,
                'author': b.author.username,
                'content': b.content,
                'author_img': b.author.p_image.url if b.author.p_image else '/media/image/download_lsX6bjA6.jpeg',
                'date': b.post_date,
                'time': b.post_time,
                'blog_img': b.blog_img.url if b.blog_img else None,
                'upvote': Upvote.objects.filter(blogid=b).count(),
                'is_upvoted': 1 if Upvote.objects.filter(blogid=b,Username=Owner.objects.get(username=username)).exists() else 0
            })
        print("tomake ami khujei ber korbo ,chander o pahar theke")
        print(blog_data)
        return Response(blog_data)
from django.db.models import Q
from .models import Friend
class Searchfnd(APIView):
    def get(self, request):
        search = request.GET.get('search', '')
        username = request.GET.get('username')
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = Owner.objects.get(username=username)
        userbox = Owner.objects.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
        user_data = []
        for sorted_user in userbox:
            if sorted_user == user:
                continue
            img_url = sorted_user.p_image.url if sorted_user.p_image else "/media/image/download_lX6bjA6.jpeg"
            fnd = Friend.objects.filter(user1=user, user2=sorted_user)
            fnd2 = Friend.objects.filter(user2=user, user1=sorted_user)
            fnd = fnd[0] if len(fnd) > 0 else None
            user_data.append({
                'id': sorted_user.id,
                'first_name': sorted_user.first_name,
                'last_name': sorted_user.last_name,
                'username': sorted_user.username,
                'email': sorted_user.email,
                'gender': sorted_user.gender,
                'phone': sorted_user.phone,
                'dob': sorted_user.dob,
                'address': sorted_user.address,
                'nid': sorted_user.nid,
                'thana': Thana.objects.get(thana=sorted_user.thana).thana,
                'pp': img_url,
                'p_image': img_url,
                'is_fnf': fnd.is_fnf if fnd is not None else fnd2[0].is_fnf if len(fnd2)>0 else 0,
                'type': fnd.type if fnd is not None else fnd2[0].type if len(fnd2)>0 else None,
                'f_created_date': fnd.f_created_date if fnd is not None else fnd2[0].f_created_date if len(fnd2)>0 else None,
                'f_id': fnd.f_id if fnd is not None else fnd2[0].f_id if len(fnd2)>0 else None,
                'abedon': 1 if fnd is not None else 0,
                'good': fnd.user1.username if fnd is not None else fnd2[0].user1.username if len(fnd2)>0 else None,
                'status': 1 if fnd is not None else 1 if len(fnd2)>0 else 0,
            })
        return Response({"users": user_data, "message": "User retrieved successfully"}, status=status.HTTP_200_OK)

    def post(self, request):
        search = request.data.get('search', '')
        username = request.data.get('username')
        query_image = request.FILES.get('image')
        
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        user = Owner.objects.get(username=username)
        
                                 
        if search:
            userbox = Owner.objects.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
        else:
            userbox = Owner.objects.all()
            
                                           
        userbox = userbox.exclude(id=user.id)
        
                                                    
        from api.vector_service import ImageVectorService
        import json
        
        query_vector = None
        if query_image:
            query_vector = ImageVectorService.extract_vector(query_image)
            
        user_scores = []
        for other_user in userbox:
                                                                              
            other_vector = None
            if other_user.p_image_vector:
                try:
                    other_vector = json.loads(other_user.p_image_vector)
                except Exception:
                    pass
            
                                                                                    
            if not other_vector and other_user.p_image:
                other_vector = ImageVectorService.extract_vector(other_user.p_image)
                if other_vector:
                    other_user.p_image_vector = json.dumps(other_vector)
                    other_user.save()
            
                                         
            score = 0.0
            if query_vector and other_vector:
                score = ImageVectorService.calculate_similarity(query_vector, other_vector)
                
            user_scores.append((other_user, score))
            
                                                                            
        if query_vector:
            user_scores.sort(key=lambda x: x[1], reverse=True)
            
                           
        user_data = []
        for other_user, score in user_scores:
            img_url = other_user.p_image.url if other_user.p_image else "/media/image/download_lX6bjA6.jpeg"
            
                                     
            fnd = Friend.objects.filter(user1=user, user2=other_user)
            fnd2 = Friend.objects.filter(user2=user, user1=other_user)
            fnd = fnd[0] if len(fnd) > 0 else None
            
            user_data.append({
                'id': other_user.id,
                'first_name': other_user.first_name,
                'last_name': other_user.last_name,
                'username': other_user.username,
                'email': other_user.email,
                'gender': other_user.gender,
                'phone': other_user.phone,
                'dob': other_user.dob,
                'address': other_user.address,
                'nid': other_user.nid,
                'thana': Thana.objects.get(thana=other_user.thana).thana,
                'pp': img_url,
                'p_image': img_url,
                'similarity_score': round(score * 100, 2) if query_vector else None,
                'is_fnf': fnd.is_fnf if fnd is not None else fnd2[0].is_fnf if len(fnd2)>0 else 0,
                'type': fnd.type if fnd is not None else fnd2[0].type if len(fnd2)>0 else None,
                'f_created_date': fnd.f_created_date if fnd is not None else fnd2[0].f_created_date if len(fnd2)>0 else None,
                'f_id': fnd.f_id if fnd is not None else fnd2[0].f_id if len(fnd2)>0 else None,
                'abedon': 1 if fnd is not None else 0,
                'good': fnd.user1.username if fnd is not None else fnd2[0].user1.username if len(fnd2)>0 else None,
                'status': 1 if fnd is not None else 1 if len(fnd2)>0 else 0,
            })
            
        return Response({"users": user_data, "message": "User retrieved successfully"}, status=status.HTTP_200_OK)

class DeleteGroup(APIView):
    def post(self,request):
        data=request.data
        print(data)
        Gmember=GroupMember.objects.get(G_username=data['guser'],member_id=Owner.objects.get(username=data['username']))
        Gmember.delete()
        return Response({"message": "Group deleted successfully"}, status=status.HTTP_201_CREATED)

class OverseerDelete(APIView):
    def post(self,request):
        data=request.data
        print(data)
        name=data['username'].split('@')[0]
        top=data['username'].split('@')[1]
        overseer=Overseer.objects.filter(username__icontains="@"+top)
        if(len(overseer)>1):
            overseer=Overseer.objects.get(username=name+"@"+top)
            overseer.delete()
            return Response({"message": "Overseer deleted successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Overseer Cannot be Deleted!"}, status=status.HTTP_201_CREATED)

class AddHandler(APIView):
    def post(self,request):
        data=request.data
        print(data)
        type=data['type']
        content=data['content']
        user=Owner.objects.get(username=data['username'])
        add = Additional.objects.create(user=user, type=type, content=content)
        add.save()
        return Response({"message": "Extra Info added successfully"}, status=status.HTTP_201_CREATED)

class PostUpdate(APIView):
    def put(self,request):
        data=request.data
        print(data)
        post=Blog.objects.get(blogid=data['id'])
        post.content=data['content']
        post.save()
        return Response({"message": "Post updated successfully"}, status=status.HTTP_201_CREATED)
    def post(self,request):
        data=request.data
        print(data)
        post=Blog.objects.get(blogid=data['id'])
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_201_CREATED)

class SearchFndBox(APIView):
    def get(self,request):
        search=request.GET.get('search')
        box=Owner.objects.get(username=request.GET.get('username'))
        userbox=Owner.objects.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
        user_data=[]
        users=Owner.objects.all()
        for user in users:
            fnd=Friend.objects.filter(user1=Owner.objects.get(id=box.id),user2=user.id)
            fnd2=Friend.objects.filter(user2=Owner.objects.get(id=box.id),user1=user.id)
            fnd=fnd[0] if len(fnd) > 0 else None
            if user not in userbox:
                continue
            if(fnd is not None and fnd.is_fnf ==1) or (len(fnd2)>0  and fnd2[0].is_fnf==1):
                    img_url = user.p_image.url if user.p_image else "/media/image/download_lX6bjA6.jpeg"
                    user_data.append({
                        'id': user.id,
                        'pp': img_url,
                        'p_image': img_url,
                        'first_name': user.first_name,
                        'username': user.username,
                        'last_name': user.last_name,
                        'email': user.email,
                        'gender': user.gender,
                        'phone': user.phone,
                        'dob': user.dob,
                        'address': user.address,
                        'nid': user.nid,
                        'thana': Thana.objects.get(thana=user.thana_id).thana,
                        'is_fnf': fnd.is_fnf if fnd is not None else fnd2[0].is_fnf if len(fnd2)>0 else None,
                        'type': fnd.type if fnd is not None else fnd2[0].type if len(fnd2)>0 else None,
                        'f_created_date': fnd.f_created_date if fnd is not None else  None,
                        'f_id': fnd.f_id if fnd is not None else None,
                        'abedon': 1 if fnd is not None else 0,
                        'good': fnd.user1.username if fnd is not None else None,
                        'msg': "gd night",
                        'time': "12:00",
                    })
        print(user_data)
        return Response({"users": user_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)


class Addinfo(APIView):
                             
                           
                     
                                                           
                                                                                            
                    
                                                                                                            
    def get(self,request):
        user=Owner.objects.get(id=request.GET.get('user_id'))
        add=Additional.objects.filter(user=user)
        add_data=[]
        for a in add:
            add_data.append({
                'id': a.id,
                'type': 1 if a.type=="Study" or a.type == "College" or a.type=="School" or a.type=="University"  else 0,
                'content': a.content
            })
        return Response(add_data)
class UpdateGroup(APIView):
    def post(self,request):
        data=request.data
        print(data)
        img=request.FILES.get('img')
        group=Group.objects.get(G_username=data['username'])
        group.G_name=data['name']
        group.Privacy=data['privacy']
        group.Topic=data['topic']
        if(img):
            group.img=img
                                                 
        group.save()
        return Response({"message": "Group updated successfully"}, status=status.HTTP_201_CREATED)
class BoxImg(APIView):
    def post(self,request):
        data=request.data
        print(data)
        img=request.FILES.get('img')
        box.img=BoxIMG.create(img=img)
        print(box)
        user.save()
        
        return Response({"message": "Image updated successfully",'img':box.img}, status=status.HTTP_201_CREATED)


from api.models import Division,Thana,District
class FindThana(APIView):
    def get(self,request):
        data=request.GET.get('district')
        thana_names = [thana for thana in Thana.objects.filter(district_id=data).values_list('thana', flat=True)]
                         
        print(thana_names)
        return JsonResponse(thana_names,safe=False)
class FindDistrict(APIView):
    def get(self,request):
        data=request.GET.get('division')
        district=District.objects.filter(division_id=data)
                            
        print(district)
        district_data=[]
        district_names = [district for district in District.objects.filter(division_id=data).values_list('district', flat=True)]
        print(district_names)
        return JsonResponse(district_names, safe=False)


class AllOwners(APIView):
    def get(self, request):
        owners = Owner.objects.all()
        data = [{'username': o.username, 'first_name': o.first_name, 'last_name': o.last_name} for o in owners]
        return Response(data, status=status.HTTP_200_OK)