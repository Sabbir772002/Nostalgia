# views.py
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
from .serializers import OwnerSerializer, OverseerSerializer,ChangePasswordSerializer,ProfileSerilazier,OwnwerUpdateSerializer,PassResetSerializer
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
            #Retrieve the overseer object to be updated
            overseer = Overseer.objects.get(pk=pk)
        except Overseer.DoesNotExist:
            return Response({"error": "Overseer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the incoming data
        serializer = OverseerSerializer(overseer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            # Retrieve the overseer object to be updated
            overseer = Overseer.objects.get(pk=pk)
        except Overseer.DoesNotExist:
            return Response({"error": "Overseer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the incoming data, but only partially update the overseer
        serializer = OverseerSerializer(overseer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class Owner_update(APIView):
    def put(self, request, username):
        try:
            #print(request.data)
            # Retrieve the user object to be updated
            owner = Owner.objects.get(username=username)
        except Owner.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        #print("you are in put")
        # Deserialize the incoming data
        serializer = OwnwerUpdateSerializer(owner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            # Retrieve the user object to be updated
            owner = Owner.objects.get(pk=pk)
        except Owner.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the incoming data, but only partially update the user
        serializer = OwnerSerializer(owner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class sign(APIView):
    def post(self, request):
        #print(request.data)
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
        # data=request.data   
        # overseer=Overseer(username=data['username'],password=data['password'],email=data['email'],phone=data['phone'],address=data['address'],nid=data['nid'],thana_id=data['thana'])
        # overseer.save()
        return Response({"message": "User created successfully", "user_id":user.id}, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        #serializer = UserLoginSerializer(data=data)
        print(data)
        #logout(request)
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
                if owner:
                    serializer.data['pp'] = owner.p_image.url
                else:
                    serializer.data['pp'] = "media/image/download_lX6bjA6.jpeg"

                return JsonResponse({'auth': True,'user':serializer.data}, status=status.HTTP_200_OK)
        
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
        # Extract query parameters from the request
        name = request.GET.get('name')
        #age = request.GET.get('age')

        # Initialize queryset
        queryset = MyModel.objects.all()
        print(name)

        # Apply filters based on query parameters
        if name:
            queryset = queryset.filter(name=name)
        #if age:
        #    queryset = queryset.filter(age=age)

        # Convert queryset to a list of dictionaries
        data = list(queryset.values())

        # Return the filtered data as JSON response
        serializer = MyModelSerializer(queryset, many=True)
        return Response(serializer.data)


# class MyModelListCreateAPIView(views.APIView):
#     def get(self, request):
#         queryset = MyModel.objects.all()
#         serializer = MyModelSerializer(queryset, many=True)
#         print(request.user)
#         return Response(serializer.data)
        
#     def post(self, request):
#         serializer = MyModelSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
            #print(username)
            #print(new_password)
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
        #check who send fnd request(future work)
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
        #print(fnd)
        #check who send fnd request(future work)
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
        #print(fnd)
        #check who send fnd request(future work)
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
        # Serialize the data
        serialized_data = []
        for user in users:
            fnd=Friend.objects.filter(user1=Owner.objects.get(id=userid),user2=user.id)
            fnd2=Friend.objects.filter(user2=Owner.objects.get(id=userid),user1=user.id)
            fnd=fnd[0] if len(fnd) > 0 else None
            if(fnd is not None and fnd.is_fnf ==1) or (len(fnd2)>0  and fnd2[0].is_fnf==1):
                    serialized_data.append({
                        'id': user.id,
                        'pp': user.p_image.url if user.p_image else "media\image\download_lX6bjA6.jpeg",
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
        userid=request.GET.get('user_id')
       # users = Owner.objects.exclude(id=userid)
        users = Owner.objects.all()
        # Serialize the data
        serialized_data = []
        for user in users:
                fnd=Friend.objects.filter(user1=Owner.objects.get(id=userid),user2=user.id)
                fnd2=Friend.objects.filter(user2=Owner.objects.get(id=userid),user1=user.id)

                if(str(user.id) == str(userid)):
                    continue
                if(len(fnd)>0 and fnd[0].is_fnf==1):
                    continue
                if(len(fnd2)>0 and fnd2[0].is_fnf==1):
                    continue
                fnd=fnd[0] if len(fnd) > 0 else None 
                serialized_data.append({
                        'id': user.id,
                        'pp': user.p_image.url if user.p_image else "media\image\download_lX6bjA6.jpeg",
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
                        'status': 1 if fnd is not None else 1 if len(fnd2)>0 else 0,
                    })
        print(serialized_data)
        return Response({"users": serialized_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)
        
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.models import KeyedVectors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
# word_pre_vectors = KeyedVectors.load_word2vec_format(r'D:\DEV\Django\Nostalgia\GoogleNews-vectors-negative300.bin\GoogleNews-vectors-negative300.bin', binary=True)

class PreRun():
    def __init__(self):
        print("pre run is called")
        self.word_pre_vectors= KeyedVectors.load_word2vec_format(r'D:\DEV\GoogleNews-vectors-negative300.bin\GoogleNews-vectors-negative300.bin', binary=True)

        


class FriendSuggestion(APIView):
    def __init__(self):
        prerun=PreRun()
        print("ye bhai eid ka chand hai")
        self.word_vectors=prerun.word_pre_vectors
    # Preprocess text
    def preprocess_text(self,text):
        # Tokenize text
        tokens = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
        #print(filtered_tokens)
        # Lemmatize tokens
        #not working comment
        # lemmatizer = WordNetLemmatizer()
        # lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        # Join tokens back into text
        preprocessed_text = ' '.join(filtered_tokens)
        return preprocessed_text

    # Encode text into fixed-length vectors using GloVe
    def encode_text(self,text):
            tokens = self.preprocess_text(text)
            # tokens=text
            #print(tokens)
            for token in tokens.split():
                if token not in self.word_vectors:
                    print(token)
            vectors = [self.word_vectors[token] for token in tokens.split() if token in self.word_vectors]
            return np.mean(vectors, axis=0) if vectors else np.zeros(self.word_vectors.vector_size)
            #return vectors if vectors else None

            
    # Calculate similarity between two texts
    def calculate_similarity(self,text1, text2):
            vector1=[]
            vector2=[]
            vector1 = self.encode_text(text1)
            vector2 = self.encode_text(text2)
            if vector1 is not None and vector2 is not None:
                return cosine_similarity([vector1], [vector2])[0][0]
                #return cosine_similarity(vector1, vector2)[0][0]
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
        # Tokenize text
        tokens = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
        # Lemmatize tokens
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        # Join tokens back into text
        preprocessed_text = ' '.join(lemmatized_tokens)
        return preprocessed_text'''

    def get(self, request):
        userid = request.GET.get('user_id')
        # Retrieve the user
        user = Owner.objects.get(username=userid)
        
        # Retrieve the IDs of the user's friends where user1 is the given user
        friend_ids = Friend.objects.filter(user1=user, is_fnf=1).values_list('user2_id', flat=True)
        # Retrieve the IDs of the user's friends where user2 is the given user
        friend_ids2 = Friend.objects.filter(user2=user, is_fnf=1).values_list('user1_id', flat=True)
        # Convert QuerySets to lists
        friend_ids = list(friend_ids)
        friend_ids2 = list(friend_ids2)
        # Include the user's ID in the friend list
        friend_ids.append(user.id)
        # Combine the friend IDs
        friend_ids.extend(friend_ids2)
        
        # Retrieve blog posts, comments, and group posts for the user
        user_blog_posts = Blog.objects.filter(author=user)
        user_comments = Comment.objects.filter(username=user)
        user_group_posts = GroupPost.objects.filter(p_username=user)
        
        # Combine text from blog posts, comments, and group posts for the user
        user_text = ''
        for post in user_blog_posts:
            user_text += post.content + ' '
        for comment in user_comments:
            user_text += comment.comment + ' '
        for group_post in user_group_posts:
            user_text += group_post.GPost_contents + ' '
        
        text1=user_text
        # Preprocess user text
        # user_text = preprocess_text(user_text)
        # # Retrieve other users excluding friends
        users = Owner.objects.exclude(id__in=friend_ids)
        
        # # Calculate TF-IDF vectors for user and other users
        # vectorizer = TfidfVectorizer()
        # user_tfidf = vectorizer.fit_transform([user_text])
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
            
            # Preprocess other user text
            # other_user_text = preprocess_text(other_user_text)
            
            # other_user_tfidf = vectorizer.transform([other_user_text])
            other_users_tfidf.append(other_user_text)
        # Calculate cosine similarity between user and other users
        similarities = []
        for other_user_tfidf in other_users_tfidf:
            #similarity = cosine_similarity(user_tfidf, other_user_tfidf)
            similarity = self.calculate_similarity(text1, other_user_tfidf)
            print(similarity)
            similarities.append(similarDity)
            #similarities.append(similarity[0][0])
        
        # Sort users based on similarity scores
        sorted_users = sorted(zip(users, similarities), key=lambda x: x[1], reverse=True)
        # Prepare response
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
                'p_image': sorted_user.p_image.url if sorted_user.p_image else 'media/image/download_lX6bjA6.jpeg',
                'is_fnf': 0,
                'type': Friend.objects.filter(user1=user, user2=sorted_user).values_list('type', flat=True).first() if Friend.objects.filter(user1=user, user2=sorted_user).exists() else Friend.objects.filter(user2=user, user1=sorted_user).values_list('type', flat=True).first() if Friend.objects.filter(user2=user, user1=sorted_user).exists() else None,
                'f_created_date':Friend.objects.filter(user1=user, user2=sorted_user).values_list('f_created_date', flat=True).first() if Friend.objects.filter(user1=user, user2=sorted_user).exists() else Friend.objects.filter(user2=user, user1=sorted_user).values_list('f_created_date', flat=True).first() if Friend.objects.filter(user2=user, user1=sorted_user).exists() else None,
                'f_id': Friend.objects.filter(user1=user, user2=sorted_user).values_list('f_id', flat=True).first() if Friend.objects.filter(user1=user, user2=sorted_user).exists() else Friend.objects.filter(user2=user, user1=sorted_user).values_list('f_id', flat=True).first() if Friend.objects.filter(user2=user, user1=sorted_user).exists() else None,
                'abedon': 1 if Friend.objects.filter(user1=user, user2=sorted_user).exists() else 0,
                'good': user.username if Friend.objects.filter(user1=user, user2=sorted_user).exists() else sorted_user.username if Friend.objects.filter(user2=user, user1=sorted_user).exists() else 0,
                'status': 1 if Friend.objects.filter(user1=user, user2=sorted_user).exists() else 1 if Friend.objects.filter(user2=user, user1=sorted_user).exists() else 0,
                 })


        return Response({"users": serialized_data, "message": "User suggestions retrieved successfully"}, status=status.HTTP_200_OK)




class EventShow(APIView):
    def get(self,request):
        return response("Hello, this is the event page!")


#Pre done code      
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.models import KeyedVectors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer

class FriendSugg(APIView):
    def preprocess_text(self, text):
        # Tokenize text
        tokens = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
        # Lemmatize tokens
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        # Join tokens back into text
        preprocessed_text = ' '.join(lemmatized_tokens)
        return preprocessed_text

    def get(self, request):
        userid = request.GET.get('user_id')
        # Retrieve the user
        user = Owner.objects.get(id=userid)
        # Retrieve the IDs of the user's friends where user1 is the given user
        friend_ids = Friend.objects.filter(user1=user, is_fnf=1).values_list('user2_id', flat=True)
        # Retrieve the IDs of the user's friends where user2 is the given user
        friend_ids2 = Friend.objects.filter(user2=user, is_fnf=1).values_list('user1_id', flat=True)
        # Convert QuerySets to lists
        friend_ids = list(friend_ids)
        friend_ids2 = list(friend_ids2)
        # Include the user's ID in the friend list
        friend_ids.append(user.id)
        # Combine the friend IDs
        friend_ids.extend(friend_ids2)
        
        # Retrieve blog posts, comments, and group posts for the user
        user_blog_posts = Blog.objects.filter(author=user)
        user_comments = Comment.objects.filter(username=user)
        user_group_posts = GroupPost.objects.filter(p_username=user)
        
        # Combine text from blog posts, comments, and group posts for the user
        user_text = ''
        for post in user_blog_posts:
            user_text += post.content + ' '
        for comment in user_comments:
            user_text += comment.comment + ' '
        for group_post in user_group_posts:
            user_text += group_post.GPost_contents + ' '
        
        text1=user_text
        # Preprocess user text
        user_text = self.preprocess_text(user_text)
        
        # Retrieve other users excluding friends
        users = Owner.objects.exclude(id__in=friend_ids)
        
        # Calculate TF-IDF vectors for user and other users
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
            # Preprocess other user text
            other_user_text = self.preprocess_text(other_user_text)
            
            other_user_tfidf = vectorizer.transform([other_user_text])
            other_users_tfidf.append(other_user_tfidf)
        # Calculate cosine similarity between user and other users
        similarities = []
        for other_user_tfidf in other_users_tfidf:
            similarity = cosine_similarity(user_tfidf, other_user_tfidf)
            similarities.append(similarity[0][0])
        # Sort users based on similarity scores
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
                'pp': sorted_user.p_image.url if sorted_user.p_image else 'media/image/download_lX6bjA6.jpeg',
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
            user={
                'id': user.id,
                'pp': user.p_image.url if user.p_image else "media\image\download_lX6bjA6.jpeg",
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
            # print(user.errors)
            # return Response({"message": "User not serialize"}, status=status.HTTP_404_NOT_FOUND)
        except Owner.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import requests
import random
import string
#change it for email....
class OTPAPI(APIView):
    def post(self, request):
        # Extract the email address from the request data
        #print(request.data)
        username = request.data.get('input')
        
        # Verify the email address using an email verification API (optional)
        # You can skip the verification API and directly send the email
        # is_email_valid = self.verify_email(email_address)
        try:
            user = Owner.objects.get(username=username)
            #print(user)
            email_address = user.email
            #print(email_address)
            verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            print(verification_code)
            # Send verification email with the verification code

            #uncomment when send mail....
            # self.send_verification_email(email_address, verification_code)
            return Response({"message": "Verification email sent successfully", "code": verification_code,"username":user.username}, status=status.HTTP_200_OK)
        except Owner.DoesNotExist:
                print("User not found")
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                
    def send_verification_email(self, email_address, verification_code):
        # Send verification email using Django's email functionality
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
    #permission_classes = [IsAuthenticated]  # Requires authentication
    paginate_by = 10  # Number of items per page (adjust as needed)

    def get_queryset(self):
        # Get the current user from the request
        user = self.request.user

        # Filter friends where the user is either user1 or user2 (excluding the current user)
        queryset = Friend.objects.filter(user1=user) | Friend.objects.filter(user2=user)
        queryset = queryset.exclude(user1=user) | queryset.exclude(user2=user)
        fndlist=[Owner.objects.get(id=fr.user1_id) for fr in queryset]
        print(fndlist)
        return queryset
    

    def get(self, request, *args, **kwargs):
        # Check if the request is for paginated data
        page_number = request.query_params.get('page')
        if page_number:
            return self.list(request, *args, **kwargs)  # Call list method for paginated response
        else:
            # Handle non-paginated GET request (e.g., retrieve specific friend details)
            friend_id = kwargs.get('pk')  # Get the friend ID from URL parameters
            try:
                friend = Friend.objects.get(pk=friend_id)
            except Friend.DoesNotExist:
                return Response({"error": "Friend not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if the current user is user1 or user2 in the friendship
            current_user = request.user
            if friend.user1 == current_user:
                friend_owner = friend.user2
            else:
                friend_owner = friend.user1

            # Serialize the friend owner object
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
        # Read image files and convert them to base64 strings
        base64_image1 = self.encode_image_to_base64(image_path1)
        base64_image2 = self.encode_image_to_base64(image_path2)

        # Prepare the payload
        payload = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "image_base64_1": base64_image1,
            "image_base64_2": base64_image2,
        }

        # Send the POST request to Face++ API
        response = requests.post(self.url, data=payload)
        response_json = response.json()

        # Process the response and return the result
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
        # Prepare the payload for Face++ API
        payload = {
            "api_key": self.API_KEY,
            "api_secret": self.API_SECRET,
            "image_base64_1": image_base64_1,
            "image_base64_2": image_base64_2,
        }
        # Send POST request to Face++ API
        response = requests.post(self.URL, data=payload)
        if(response.json().get('error_message')):
            return "Error: {}".format(response.json().get('error_message'))
        response_json = response.json()
        # Process the response and return the result
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
        # Get image data from the POST request
        print(request.data)
        image_file1 = request.FILES.get('image1')
        # image_file2 = request.FILES.get('image2')
        image_file2 = request.data['image2']
        if(image_file1 is not None):
            print("image1")
        if(image_file2 is not None):
            print(image_file2)

        if not (image_file1 and image_file2):
            return JsonResponse({'error': 'Missing image data in request'}, status=400)
        
        # Convert images to base64 strings
        image_base64_1 = base64.b64encode(image_file1.read()).decode('utf-8')
        # image_base64_1 = base64.b64encode(image_file2.read()).decode('utf-8')
        # Download and save the second image file
        image_file2_url = "http://localhost:8000" + image_file2
        print(image_file2_url)
        image_file2_path = r"D:\DEV\Django\Nostalgia\media\image\image_file2.jpg"
        image_base64_2=""
        response = requests.get(image_file2_url)
        if response.status_code == 200:
            # Save the image file
            with open(image_file2_path, "wb") as f:
                f.write(response.content)
                print("Image file saved successfully.")
            
            # Convert the saved image file to base64
            with open(image_file2_path, "rb") as f:
                image_base64_2 = base64.b64encode(f.read()).decode('utf-8')
        # Perform image comparison using FaceApiCompare class method
        if not image_base64_2:
            return JsonResponse({'error': 'Failed to download the Profile image file'}, status=500)

        result = face_api_compare.compare_images(image_base64_1, image_base64_2)

        # Return the comparison result as JSON response
        return JsonResponse({'result': result})
        
class CompareImages(APIView):
      def post(self, request, *args, **kwargs):
        # Get image data from the POST request
        print(request.data)
        # image_file2 = request.FILES.get('image2')
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
            # Save the image file
            with open(image_file1_path, "wb") as f:
                f.write(response.content)
                print("Image file saved successfully.")
            
            # Convert the saved image file to base64
            with open(image_file1_path, "rb") as f:
                image_base64_1 = base64.b64encode(f.read()).decode('utf-8')
        # Perform image comparison using FaceApiCompare class method
        if not image_base64_1:
            return JsonResponse({'error': 'Failed to download the Profile image file'}, status=500)
        # image_base64_1 = base64.b64encode(image_file2.read()).decode('utf-8')
        # Download and save the second image file
        image_file2_url = "http://localhost:8000" + image_file2
        print(image_file2_url)
        image_file2_path = r"D:\DEV\Django\Nostalgia\media\image\image_file2.jpg"
        image_base64_2=""
        response = requests.get(image_file2_url)
        if response.status_code == 200:
            # Save the image file
            with open(image_file2_path, "wb") as f:
                f.write(response.content)
                print("Image file saved successfully.")
            # Convert the saved image file to base64
            with open(image_file2_path, "rb") as f:
                image_base64_2 = base64.b64encode(f.read()).decode('utf-8')
        # Perform image comparison using FaceApiCompare class method
        if not image_base64_2:
            return JsonResponse({'error': 'Failed to download the Profile image file'}, status=500)

        result = face_api_compare.compare_images(image_base64_1, image_base64_2)
        # Return the comparison result as JSON response
        return JsonResponse({'result': result})

class WalkingBuddyList(APIView):
    def get(self, request):
        users = Owner.objects.all()
        # Serialize the data
        serialized_data = []
        for user in users:
            serialized_data.append({
                'id': user.id,
                'pp': user.p_image.url if user.p_image else "media\image\download_lX6bjA6.jpeg",
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
        target = request.GET.get('target')  # Assuming 'target' is passed as a query parameter
        print(target)
        if not target:
            return Response({"message": "Please provide a target value"}, status=status.HTTP_400_BAD_REQUEST)
        target="@"+target
        users = Overseer.objects.filter(username__contains=target)
        serialized_data = []
        for user in users:
            serialized_data.append({
                'id': user.id,
                'pp': user.p_image.url if user.p_image else "media\image\download_lX6bjA6.jpeg",
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
                #'thana': Thana.objects.get(thana=user.thana_id).thana,
            })
        
        return Response({"users": serialized_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)


    
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Blog,Upvote
from .serializers import BlogSerializer
from django.http import JsonResponse
class BlogListView(APIView):
    def get(self, request):
        # Retrieve all Blog objects from the database
            queryset = Blog.objects.all().order_by('-post_date', '-post_time')
            blogs_data = []
            username = request.GET.get('username')
           # print(username)

            for blog in queryset:
                #print(blog.author)
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
           # print(blogs_data)

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
                # upvote_instance1 = Upvote(Username=Owner.objects.get(username=username), blogid=blog)
                # upvote_instance1.save()
                print("dont be like that")
                Noti=Notification(noti_type="Upvote",noti_msg="upvoted your blog",noti_sender=Owner.objects.get(username=username),noti_receiver=Owner.objects.get(username=blog.author),noti_status=0)
                Noti.save()
            upvoted = Upvote.objects.filter(
                Username=Owner.objects.get(username=username), blogid=id)
            if len(upvoted)==1:
                upvote_instance = Upvote(Username=Owner.objects.get(username=username), blogid=blog)
                upvote_instance.save()
                #this have to think, bcz, user knwo who withdraw his upvote
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
        # Retrieve all Blog objects from the database
            username = request.GET.get('username')
            print("shuno na go kotha")
            print(username)
            queryset = Blog.objects.filter(author=Owner.objects.get(username=username).id).order_by('-post_date', '-post_time')
            blogs_data = []
            print(Owner.objects.get(username=username).id)
            for blog in queryset:
                #print(blog.author)
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
    #serializer_class = BlogSerializer
    def post(self, request, *args, **kwargs):
        # Retrieve data from the request
        username = request.data['username']
        data = request.data
        user = Owner.objects.get(username=username)
        # print(data)
        blog_img = request.data.get('blog_img')
        #print(blog_img)
        if blog_img is not None:
            blog = Blog.objects.create(
                    author=user,
                    content=data['content'],
                    post_date=datetime.now().date(),
                    post_time=datetime.now().time(),
                    blog_img=blog_img if blog_img else None
                )
                # Save the blog instance
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
        #walks = Walk.objects.filter(Q(w_creator=user) | Q(walkmember__username=user)).order_by('walk_date').distinct()
          # Retrieve the IDs of the user's friends where user1 is the given user
        friend_ids = Friend.objects.filter(user1=user, is_fnf=1).values_list('user2_id', flat=True)
        # Retrieve the IDs of the user's friends where user2 is the given user
        friend_ids2 = Friend.objects.filter(user2=user, is_fnf=1).values_list('user1_id', flat=True)
        # Convert QuerySets to lists
        friend_ids = list(friend_ids)
        friend_ids2 = list(friend_ids2)
        # Include the user's ID in the friend list
        friend_ids.append(user.id)
        # Combine the friend IDs
        friend_ids.extend(friend_ids2)
        friend_ids.extend([user.id])
        walks=Walk.objects.all().filter(w_creator__in=friend_ids).order_by('-walk_date','-end_date').distinct()
        walks_data = []
        for walk in walks:
            #print(walk.w_creator.p_image)
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
    # Calculate the time difference
    time_difference = datetime.utcnow() - timestamp

    # Convert time difference to days, hours, and minutes
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
           #Retrieve all Blog objects from the database
           # username = request.GET.get('username')
            print("retrive comment")
            #print(username)
            blog = request.GET.get('blog')
            blog=Blog.objects.get(blogid=blog)
            print(blog.content)
            queryset = Comment.objects.filter(blogid=blog).order_by( '-time')
            blogs_data = []
            #print(Owner.objects.get(username=username).id)
            for blog in queryset:
                #print(blog.comment)
                #timestamp = blog.time.replace(tzinfo=timezone.utc)
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
    #serializer_class = BlogSerializer
    def post(self, request, *args, **kwargs):
        print("comment create")
        print(request.data)
        # Retrieve data from the request
        username = request.data['author']
        print(username)
        data = request.data
        user = Owner.objects.get(username=username)
        # print(data)
        blog_img = ""#request.data.get('blog_img')
        #print(blog_img)
        if blog_img is not None:
            blog = Comment.objects.create(
                   blogid=Blog.objects.get(blogid=data['blog']),
                    username=user,
                    comment=data['content'],
                    time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                # Save the blog instance
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
        user = User.objects.get(username=username)
        user_blogs = Blog.objects.filter(author__username=username)
        user_comments = Comment.objects.filter(username__username=username)
        user_content = []
        for blog in user_blogs:
            user_content.append(blog.content)
        for comment in user_comments:
            user_content.append(comment.comment)
        # Get all blogs excluding the user's blogs
        all_blogs = Blog.objects.exclude(author__username=username)
        # Combine the content of all blogs and comments
        all_content = []
        for blog in all_blogs:
            all_content.append(blog.content)
            # Also consider comments associated with this blog
            comments = Comment.objects.filter(blogid=blog.blogid)
            for comment in comments:
                all_content.append(comment.comment)

        # Calculate TF-IDF vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(user_content + all_content)

        # Calculate cosine similarity
        user_tfidf = tfidf_matrix[:len(user_content)]
        all_tfidf = tfidf_matrix[len(user_content):]
        similarity_matrix = cosine_similarity(user_tfidf, all_tfidf)

        # Sort blogs based on cosine similarity
        similarity_scores = similarity_matrix.mean(axis=0)  # Taking mean across user content
        sorted_indices = [int(i) for i in np.argsort(similarity_scores)[::-1]]

        def preprocess_text(text):
            return text

        def combine_text(posts):
            combined_text = ''
            for post in posts:
                if isinstance(post, Blog):
                    combined_text += post.content + ' '
                elif isinstance(post, Comment):
                    combined_text += post.comment + ' '  # Adjust this according to your Comment model
                elif isinstance(post, GroupPost):
                    combined_text += post.GPost_contents + ' '
            return combined_text

        all_blog_posts = Blog.objects.all()
        all_comments = Comment.objects.all()
        all_group_posts = GroupPost.objects.all()

        # Combine text from all posts
        all_posts_text = combine_text(all_blog_posts) + combine_text(all_comments) + combine_text(all_group_posts)

        # Preprocess all posts text
        all_posts_text = preprocess_text(all_posts_text)

        # Calculate TF-IDF vectors for all posts
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([all_posts_text])

        # Retrieve the posts of the given user
        user_blog_posts = Blog.objects.filter(author=user)
        user_comments = Comment.objects.filter(username=user)
        user_group_posts = GroupPost.objects.filter(p_username=user)

        # Combine text from the user's posts
        user_posts_text = combine_text(user_blog_posts) + combine_text(user_comments) + combine_text(user_group_posts)

        # Preprocess the user's posts text
        user_posts_text = preprocess_text(user_posts_text)

        # Calculate TF-IDF vectors for the user's posts
        user_tfidf = vectorizer.transform([user_posts_text])

        # Calculate cosine similarity between the user's posts and all other posts
        similarities = []
        for post in all_blog_posts:
            post_text = combine_text([post])
            post_text = preprocess_text(post_text)
            post_tfidf = vectorizer.transform([post_text])
            similarity = cosine_similarity(user_tfidf, post_tfidf)[0][0]
            similarities.append((post, similarity))

        # Sort posts based on similarity scores
        sorted_posts = sorted(similarities, key=lambda x: x[1], reverse=True)
        sorted_posts = [post for post, similarity in sorted_posts]
        userbox=Friend.objects.filter()
        blogs_data = []
        # Retrieve the IDs of the user's friends where user1 is the given user
        friend_ids = Friend.objects.filter(user1=user, is_fnf=1).values_list('user2_id', flat=True)
        # Retrieve the IDs of the user's friends where user2 is the given user
        friend_ids2 = Friend.objects.filter(user2=user, is_fnf=1).values_list('user1_id', flat=True)
        # Convert QuerySets to lists
        friend_ids = list(friend_ids)
        friend_ids2 = list(friend_ids2)
        # Include the user's ID in the friend list
        friend_ids.append(user.id)
        # Combine the friend IDs
        friend_ids.extend(friend_ids2)
        ninety_days_ago = datetime.now().date() - timedelta(days=90)
        date= datetime.now().date()
        for post in sorted_posts:
            blog = Blog.objects.filter(blogid=post.blogid)
            if blog.exists():
                blog = blog[0]
                if blog.author.id not in friend_ids and blog.author.username != username:
                    continue
                if blog.post_date + timedelta(days=90) < date:
                    continue
                blog_data = {
                    'id': blog.blogid,
                    'author': blog.author.username,
                    'author_img': blog.author.p_image.url if blog.author.p_image else "/media/image/download_lsX6bjA6.jpeg",
                    'content': blog.content,
                    'post_date': blog.post_date,
                    'post_time': blog.post_time,
                    'blog_img': blog.blog_img.url if blog.blog_img else None,
                    'upvote': blog.upvote_set.count(),
                    'is_upvoted': 1 if blog.upvote_set.filter(Username__username=username).exists() else 0
                }
                blogs_data.append(blog_data)

        return Response(blogs_data)
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
from .models import Group
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
    def get(self,request):
        username=request.GET.get('user_id')
        user=Owner.objects.get(id=username)
        groups=GroupMember.objects.filter(member_id=user,accept=1).values_list('G_username',flat=True).distinct()
        print(groups)
          # Retrieve the IDs of the user's friends where user1 is the given user
        friend_ids = Friend.objects.filter(user1=user, is_fnf=1).values_list('user2_id', flat=True)
        # Retrieve the IDs of the user's friends where user2 is the given user
        friend_ids2 = Friend.objects.filter(user2=user, is_fnf=1).values_list('user1_id', flat=True)
        # Convert QuerySets to lists
        friend_ids = list(friend_ids)
        friend_ids2 = list(friend_ids2)
        # Include the user's ID in the friend list
        friend_ids.append(user.id)
        # Combine the friend IDs
        friend_ids.extend(friend_ids2)
        groups=Group.objects.exclude(G_username__in=groups)
        print(groups)
        groups_data=[]
        for group in groups:
            fd=Friend.objects.filter(user1=user, user2=group.Creator)
            if(len(fd)==0):
                fd=Friend.objects.filter(user2=user, user1=group.Creator)
            if(len(fd)>0):
                fd=fd[0]
                if(fd.type!=group.Privacy and group.Privacy=="Bondhu" and group.Privacy!="Public"):
                    print("continue 1")
                    continue
            if group.Creator.id not in friend_ids and group.Privacy!="Public":
                    print("continue 2")
                    continue
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
        print("in group list")
        print(groups_data)
        return Response(groups_data)
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
                # 'upvote': GroupUpvote.objects.filter(post_id=post).count(),
                # 'is_upvoted': 1 if GroupUpvote.objects.filter(post_id=post,Username=Owner.objects.get(username=username)).exists() else 0
            })
        print(posts_data)
        return Response(posts_data)
class GT_post(APIView):
    def get(self,request):
        username=request.GET.get('username')
        # print(username)
        # group=Group.objects.get(G_username=username)
        # posts=GroupPost.objects.filter(G_username=group)
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
                # 'upvote': GroupUpvote.objects.filter(post_id=post).count(),
                # 'is_upvoted': 1 if GroupUpvote.objects.filter(post_id=post,Username=Owner.objects.get(username=username)).exists() else 0
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
    #serializer_class = BlogSerializer
    def post(self, request, *args, **kwargs):
        # Retrieve data from the request
        print(request.data)
        username = request.data['username']
        data = request.data
        user = Owner.objects.get(username=username)
        # print(data)
        blog_img = request.data.get('blog_img')
        #print(blog_img)
        if blog_img is not None:
            blog = GroupPost.objects.create(
                    G_username=Group.objects.get(G_username=data['gp']),
                    p_username=user,
                    GPost_contents=data['content'],
                    GPost_date=data['post_date'],
                    GPost_Time=data['post_time'],
                    GPost_image=blog_img if blog_img else None
                )
                # Save the blog instance
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
import easyocr
import cv2
import re
class NIDImage(APIView):
    def post(self,request):

        def compare_nid(image1, image2):
            url = 'http://127.0.0.1:8000/comparenid'
            try:
                response = requests.post(url, data={'image2': "/media/"+image1,'image1': image2})
                response.raise_for_status()  # Raise an exception for HTTP errors
                print('Upload success:', response.json())
                return response.json().get('result')
                # Handle success (e.g., show a success message)
            except requests.exceptions.RequestException as e:
                print('Error uploading images:', e)
            return 0

        def match(str1, str2):
            m = len(str1)
            n = len(str2)

            # Initialize a table to store lengths of LCS
            dp = [[0] * (n + 1) for _ in range(m + 1)]

            # Build dp table in bottom-up manner
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if str1[i - 1] == str2[j - 1]:
                        dp[i][j] = dp[i - 1][j - 1] + 1
                    else:
                        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

            # Read the characters from the dp table
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
                # Read the file content as bytes
                image_bytes = img.read()
                # Convert bytes to numpy array
                nparr = np.frombuffer(image_bytes, np.uint8)
                # Load image using OpenCV
                img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                # Process the image with EasyOCR
                reader = easyocr.Reader(['en', 'bn'], gpu=True)
                result = reader.readtext(img_cv)

                # Continue with processing the result
                # with open("nid.txt", 'w', encoding='utf-8') as f:
                #     for detection in result:
                #         text.append(detection[1])
                #         f.write(detection[1])
                #         f.write('\n')
                #         print(detection[1])
                #     f.close()
                for detection in result:
                    #print(detection[1])
                    text.append(detection[1])
                text = ' '.join(text)
                # Define regular expressions to extract name, date of birth, and ID number
                # name_pattern = r'Name:\s*(.+?)\s+'
                # dob_pattern = r'Date of Birth:\s*(\d{2}\s+[A-Za-z]+\s+\d{4})'
                # id_pattern = r'ID NO:\s*(\d+)'
                name_pattern = r'[Nn][Aa][Mm][Ee]?\s*[: ]\s*([A-Za-z]+(?:\s+[A-Za-z]+)*)\s+'
                dob_pattern = r'Date of Birth:\s*(\d{2}\s+[A-Za-z]+\s+\d{4})'
                id_pattern = r'(?:ID|NO)s*[: ]\s*(\d+)'
                # Extract name
                name_match = re.search(name_pattern, text)
                if name_match:
                    name = name_match.group(1)
                    
                # Extract date of birth
                dob_match = re.search(dob_pattern, text)
                if dob_match:
                    dob = dob_match.group(1)
                # Extract ID number
                id_match = re.search(id_pattern, text)
                if id_match:
                    id= id_match.group(1)
                # Concatenate the extracted information into one string
                # result = name + ' ' + dob + ' ' + id
                # print(result)
                
                # name_pattern = r'STUDENT\s+NAME\s+(.*)'
                # dob_pattern = r'DATE\s+OF\s+BIRTH\s+(.*)'
                # nationality_pattern = r'NATIONALITY\s+(.*)'

                # # Initialize variables to store extracted information
                # student_name = None
                # date_of_birth = None
                # nationality = None
                # # Iterate through detected text and apply regex patterns
                # for line in text:
                #     name_match = re.match(name_pattern, line)
                #     if name_match:
                #         student_name = name_match.group(1).strip()
                    
                #     dob_match = re.match(dob_pattern, line)
                #     if dob_match:
                #         date_of_birth = dob_match.group(1).strip()
                    
                #     nationality_match = re.match(nationality_pattern, line)
                #     if nationality_match:
                #         nationality = nationality_match.group(1).strip()

                # # Print the extracted information
                # print("Student Name: ", student_name)
                # print("Date of Birth: ", date_of_birth)
                # print("Nationality: ", nationality)

            else:
                # If img is a file path or URL
                IMAGE_PATH = img
                reader = easyocr.Reader(['en', 'bn'], gpu=True)
                result = reader.readtext(IMAGE_PATH)
        except catch(e):
              return Response({"message": "NID Not Matched"}, status=status.HTTP_400_BAD_REQUEST)

        # print(text)
        user=Owner.objects.get(username=user)
        uname=user.first_name+" "+user.last_name
        mtn=match((user.first_name+" "+user.last_name).lower(),name.lower())
        mti=match(user.nid,id)
        if(mti>=9 and mtn>=(len(uname)-(len(uname)//6))):
                print(str(user.p_image))
                image_file2_path = r"D:\DEV\Django\Nostalgia\media\1.png"
                with open(image_file2_path, "wb") as f:
                    for chunk in img.chunks():
                        f.write(chunk)
                    print("Image file saved(1) successfully.")
                to=compare_nid(str(user.p_image),"\media\image\1_6xohGA6.png")
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

# from django.http import JsonResponse
# from django.views import View
# from PIL import Image
# from pyzbar.pyzbar import decode

# from django.http import JsonResponse
# from django.views import View
# from PIL import Image
# from pyzbar.pyzbar import decode

# class DecodeImageView(View):
#     def decode_image(self, image):
#         # Decode the barcode from the image
#         decoded_objects = decode(image)

#         # Extract decoded text from the decoded objects
#         decoded_text = []
#         for obj in decoded_objects:
#             decoded_text.append(obj.data.decode('utf-8'))

#         return decoded_text

#     def post(self, request, *args, **kwargs):
#         try:
#             # Check if 'image' file is present in the request
#             if 'image' not in request.FILES:
#                 return JsonResponse({"error": "No image file found in the request"}, status=400)
            
#             # Get the 'image' file from the request
#             image_file = request.FILES['image']

#             # Open the image file using PIL
#             image = Image.open(image_file)

#             # Call the decode_image function to decode the barcode
#             decoded_text = self.decode_image(image)

#             # Return the decoded text
#             return JsonResponse({"decoded_text": decoded_text})

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
from .models import Caregiver
class CareGiver(APIView):
    def get(self,request):
        caregivers=Caregiver.objects.all()
        caregivers_data=[]
        for caregiver in caregivers:
            caregivers_data.append({
                'id': caregiver.caregiver_id,
                'name': caregiver.name,
                #'img': caregiver.img.url if caregiver.img else "/media/image/download_lsX6bjA6.jpeg",
                'img': "media\images\download.jpeg",
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
        # Serialize the data
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
                'Image': event.Image.url if event.Image else "media\image\default.jpeg",
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
            Approve=1,  # Assuming this is a boolean field indicating approval
            start_time=data['start_time'],  # Fixing the syntax here
            end_time=data['end_time'],
            Description=data['Description'],  # Fixing the typo in 'Description'
            E_type=data['type'],
            Thana=Thana.objects.get(thana=data['thana'])  # Assuming 'thana' is a foreign key to Thana model
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
        event=Event.objects.get(event_id=event_id)
        members=JoinEvent.objects.filter(event_id=event_id,accept=0)
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

class HandleEventmember(APIView):
    def post(self,request):
        if request.data['type'] == 'confirm':
            event_id=request.data['event_id']
            user_id=request.data['id']
            user=Owner.objects.get(id=user_id)
            event=Event.objects.get(event_id=event_id)
            members=JoinEvent.objects.filter(event_id=event,username=user)
            print(members)
            if(len(members)>0):
                members[0].accept=1
                members[0].save()
                return Response({"user": members[0].username.username})
        if request.data['type'] == 'delete':
            event_id=request.data['event_id']
            user_id=request.data['id']
            user=Owner.objects.get(id=user_id)
            event=Event.objects.get(walk_id=walk_id)
            members=JoinEvent.objects.filter(event_id=event,username=user)
            print(members)
            if(len(members)>0):
                members[0].delete()
                return Response({"user": members[0].username.username})
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
        # Serialize the data
        serialized_data = []
        user = Owner.objects.get(username=request.GET.get('username'))
        print(user)
        print("in trip list view... ")
        # Retrieve the IDs of the user's friends where user1 is the given user
        friend_ids = Friend.objects.filter(user1=user, is_fnf=1).values_list('user2_id', flat=True)
        # Retrieve the IDs of the user's friends where user2 is the given user
        friend_ids2 = Friend.objects.filter(user2=user, is_fnf=1).values_list('user1_id', flat=True)
        # Convert QuerySets to lists
        friend_ids = list(friend_ids)
        friend_ids2 = list(friend_ids2)
        # Include the user's ID in the friend list
        friend_ids.append(user.id)
        # Combine the friend IDs
        friend_ids.extend(friend_ids2)
        friend_ids.extend([user.id]) 
        trips = Trip.objects.filter(Creator__in=friend_ids,end_date__gte=datetime.now())
        for trip in trips:
            if trip.Creator.id not in friend_ids and trip.creator != user:
                continue
            serialized_data.append({
                'id': trip.TripID,
                'name': trip.name,
                'location': trip.Location,
                'start_date': trip.start_date,
                'end_date': trip.end_date,
                'propose_date': trip.propose_date,
                'privacy': trip.Privacy,
                'creator': trip.Creator.username,  
                'thana': trip.Thana.thana,  
                'guide': trip.guide,
                'member' : 1 if TripMember.objects.filter(TripID=trip,member=Owner.objects.get(username=request.GET.get('username')),Approve=1,cancel=0).exists() else 0,
                'join' : 1 if TripMember.objects.filter(TripID=trip,member=Owner.objects.get(username=request.GET.get('username')),Approve=0,cancel=0).exists() else 0
            })
        print(serialized_data)
        
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
            # guide=Owner.objects.get(username=data['guide'])
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
        # trip=TripMember.objects.get(TripID=trip_id)
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
            # Check the morning, noon, and night attributes and append corresponding times to med_times
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
    def get(self,request):
        search=request.GET.get('search')
        print(request.GET.get('username'))
        user=Owner.objects.get(username=request.GET.get('username'))
        userbox=Owner.objects.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
        user_data=[]
        for sorted_user in userbox:
            if sorted_user==user:
                print("yi to harami hai")
                continue
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
                'pp': sorted_user.p_image.url if sorted_user.p_image else 'media/image/download_lX6bjA6.jpeg',
                'is_fnf': 0,
                'type': Friend.objects.filter(user1=user, user2=sorted_user).values_list('type', flat=True).first() if Friend.objects.filter(user1=user, user2=sorted_user).exists() else Friend.objects.filter(user2=user, user1=sorted_user).values_list('type', flat=True).first() if Friend.objects.filter(user2=user, user1=sorted_user).exists() else None,
                'f_created_date':Friend.objects.filter(user1=user, user2=sorted_user).values_list('f_created_date', flat=True).first() if Friend.objects.filter(user1=user, user2=sorted_user).exists() else Friend.objects.filter(user2=user, user1=sorted_user).values_list('f_created_date', flat=True).first() if Friend.objects.filter(user2=user, user1=sorted_user).exists() else None,
                'f_id': Friend.objects.filter(user1=user, user2=sorted_user).values_list('f_id', flat=True).first() if Friend.objects.filter(user1=user, user2=sorted_user).exists() else Friend.objects.filter(user2=user, user1=sorted_user).values_list('f_id', flat=True).first() if Friend.objects.filter(user2=user, user1=sorted_user).exists() else None,
                'abedon': 1 if Friend.objects.filter(user1=user, user2=sorted_user).exists() else 0,
                'good': 1 if Friend.objects.filter(user1=user, user2=sorted_user).exists() else 1 if Friend.objects.filter(user2=user, user1=sorted_user).exists() else 0,
                'status': 1 if Friend.objects.filter(user1=user, user2=sorted_user).exists() else 1 if Friend.objects.filter(user2=user, user1=sorted_user).exists() else 0,
                 })
        return Response({"users":user_data, "message": "User retrieved successfully"}, status=status.HTTP_200_OK)

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
                    user_data.append({
                        'id': user.id,
                        'pp': user.p_image.url if user.p_image else "media\image\download_lX6bjA6.jpeg",
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
    # def post(self,request):
    #     data=request.data
    #     print(data)
    #     user=Owner.objects.get(username=data['username'])
    #     add=Additional.objects.create(user=user,type=data['type'],content=data['content'])
    #     add.save()
    #     return Response({"message": "Additional info added successfully"}, status=status.HTTP_201_CREATED)
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
       # group.G_description=data['gdescription']
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
        #.values('thana')
        print(thana_names)
        return JsonResponse(thana_names,safe=False)
class FindDistrict(APIView):
    def get(self,request):
        data=request.GET.get('division')
        district=District.objects.filter(division_id=data)
        #.values('district')
        print(district)
        district_data=[]
        district_names = [district for district in District.objects.filter(division_id=data).values_list('district', flat=True)]
        print(district_names)
        return JsonResponse(district_names, safe=False)