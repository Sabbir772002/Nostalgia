         
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
                    
    MyAPIView, _sign, sign, login_api, ChangePass, show, friends,
    Owner_update, O_update, UserLogin,
    CustomTokenObtainPairView, CustomTokenRefreshView, HelloWorldView,
    add_fnf, Profile,
    PlanEventCreateAPIView, PlanEventListAPIView, PlanEventUpdateAPIView,
    FriendListView, FriendList, OverseerList, FindFriend, update_fnf,
    OTPAPI, PassReset, BlogListView, BlogSingleView, BlogCreateView,
    Add_group, My_Group, GroupProfile, GP_post, GT_post,
    JoinGroup, AddGroupPost, GroupMembers, RequestMembers, GroupRequest,
    WalkListView, WalkMembers, Walk_request, WalkNotMember, Handlemember,
    NotificationView, BlogCommentsView, CommentCreateView, HTimeline,
    UpvoteAPIView, CompareImagesView, CompareImages,
    CareGiver, MedicationBox, Done, MedTime,
    Search, Searchfnd, DeleteGroup, OverseerDelete,
    AddHandler, PostUpdate, SearchFndBox, Addinfo,
    UpdateGroup, FindThana, FindDistrict, AllOwners,
    EventListView, EventMembers, Event_request, EventNotMember, HandleEventmember,
    TripListView, TripUpdate, TripMembers, Trip_request, TripNotMember, HandleTripmember,
    FriendSugg, Not_My_Group, RecommendedFeedView, RecommendedFriendsView,
    RecommendedGroupsView, RecommendedTripsView, RecommendedWalksView,
    RecommendedEventsView,Delete_fnd, NIDImage, BlogViewAPIView, BlogDetailAPIView
)

urlpatterns = [
                                                            
    path('login', login_api.as_view(), name='login'),
    path('log', UserLogin.as_view(), name='log'),
    path('sign', sign.as_view(), name='sign'),
    path('add_overseer', _sign.as_view(), name='add_overseer'),
    path('changepass', ChangePass.as_view(), name='changepass'),
    path('resetpass', PassReset.as_view(), name='resetpass'),
    path('otp', OTPAPI.as_view(), name='otp'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

                                    
    path('profile/<username>', Profile.as_view(), name='profile'),
    path('owner/<username>', Owner_update.as_view(), name='Owner_update'),
    path('overseer/<int:pk>', O_update.as_view(), name='O_update'),
    path('show', show.as_view(), name='show'),
    path('owners', AllOwners.as_view(), name='all_owners'),
    path('overseerlist', OverseerList.as_view(), name='overseerlist'),

                                            
    path('friends', FriendList.as_view(), name='friend-list'),
    path('friend', friends, name='friend'),                               
    path('findfriend', FindFriend.as_view(), name='findfriend'),
    path('add_fnf', add_fnf.as_view(), name='add_fnf'),
    path('update_fnf', update_fnf.as_view(), name='update_fnf'),
    path('delete_fnd', Delete_fnd.as_view(), name='delete_fnd'),
    path('friendsugg', FriendSugg.as_view(), name='friendsugg'),                                               
    path('searchfnd', Searchfnd.as_view(), name='searchfnd'),
    path('searchfndbox', SearchFndBox.as_view(), name='searchfndbox'),

                                       
    path('blog', BlogListView.as_view(), name='blog'),
    path('singleblog', BlogSingleView.as_view(), name='singleblog'),
    path('addblog', BlogCreateView.as_view(), name='addblog'),
    path('upvote', UpvoteAPIView.as_view(), name='upvote'),
    path('comments', BlogCommentsView.as_view(), name='comments'),
    path('comment', CommentCreateView.as_view(), name='newcomment'),
    path('posts', PostUpdate.as_view(), name='posts'),
    path('post_view', BlogViewAPIView.as_view(), name='post_view'),
    path('blog_detail', BlogDetailAPIView.as_view(), name='blog_detail'),

                                                           
    path('htimeline', HTimeline.as_view(), name='htimeline'),                                          

                                  
    path('add_group', Add_group.as_view(), name='add_group'),
    path('my_groups', My_Group.as_view(), name='my_groups'),
    path('!my_groups', Not_My_Group.as_view(), name='!my_groups'),                                        
    path('g_profile/<username>', GroupProfile.as_view(), name='g_profile'),
    path('gp_post', GP_post.as_view(), name='GP_post'),
    path('gt_post', GT_post.as_view(), name='GT_post'),
    path('join_group', JoinGroup.as_view(), name='join_group'),
    path('addgroupost', AddGroupPost.as_view(), name='addgroupost'),
    path('groupmembers', GroupMembers.as_view(), name='groupmembers'),
    path('requestmembers', RequestMembers.as_view(), name='requestmembers'),
    path('grouprequest', GroupRequest.as_view(), name='grouprequest'),
    path('deletegroup', DeleteGroup.as_view(), name='DeleteGroup'),
    path('updategroup', UpdateGroup.as_view(), name='updategroup'),

                                 
    path('walk', WalkListView.as_view(), name='walk'),                                                
    path('walkmembers', WalkMembers.as_view(), name='walk_members'),
    path('walk_request', Walk_request.as_view(), name='walk_request'),
    path('walk!members', WalkNotMember.as_view(), name='walk!members'),
    path('handlemember', Handlemember.as_view(), name='Handlemember'),

                                  
    path('event', EventListView.as_view(), name='event'),                                              
    path('eventmembers', EventMembers.as_view(), name='event_members'),
    path('event_request', Event_request.as_view(), name='event_request'),
    path('event!members', EventNotMember.as_view(), name='event!members'),
    path('handle_eventmember', HandleEventmember.as_view(), name='handle_eventmember'),
                                  
    path('api/events/create/', PlanEventCreateAPIView.as_view(), name='event-create'),
    path('api/events/list/', PlanEventListAPIView.as_view(), name='event-list'),
    path('api/events/update/<int:pk>/', PlanEventUpdateAPIView.as_view(), name='event-update'),

                                 
    path('trip', TripListView.as_view(), name='trip'),                                               
    path('tripupdate', TripUpdate.as_view(), name='tripupdate'),
    path('tripmembers', TripMembers.as_view(), name='trip_members'),
    path('trip_request', Trip_request.as_view(), name='trip_request'),
    path('trip!members', TripNotMember.as_view(), name='trip!members'),
    path('handletripmember', HandleTripmember.as_view(), name='handletripmember'),

                                      
    path('caregiver', CareGiver.as_view(), name='caregiver'),
    path('medication', MedicationBox.as_view(), name='medication'),
    path('done', Done.as_view(), name='done'),
    path('medtime', MedTime.as_view(), name='medtime'),

                                         
    path('notification', NotificationView.as_view(), name='notification'),

                                  
    path('search', Search.as_view(), name='search'),
    path('findthana', FindThana.as_view(), name='findthana'),
    path('finddistrict', FindDistrict.as_view(), name='finddistrict'),

                                                  
    path('nidimg', NIDImage.as_view(), name='nidimg'),
    path('compare', CompareImagesView.as_view(), name='compare_images'),
    path('comparenid', CompareImages.as_view(), name='compare_images'),

                                           
    path('addinfo', Addinfo.as_view(), name='addinfo'),
    path('addhandle', AddHandler.as_view(), name='addhandler'),
    path('doverseer', OverseerDelete.as_view(), name='doverseer'),

                                           
    path('orm', MyAPIView.as_view(), name='MyAPIView'),
    path('hello/', HelloWorldView.as_view(), name='hello_world'),
]

                                      
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


