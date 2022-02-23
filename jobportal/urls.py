
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.IndexPage,name="index"),
    path("signup/",views.SignupPage,name="singup"),
    path("register/",views.RegisterPage,name="register"),
    path("otppage/",views.OTPPage,name="otppage"),
    path("otpverify/",views.Otpverify,name="otp"),
    path("loginpage/",views.LoginPage,name="loginpage"),
    path("loginuser/",views.LoginUser,name="login"),
    path("profile/<int:pk>",views.ProfilePage,name="profile"),
    path("updateprofile/<int:pk>",views.ProfileUpdate,name="updateprofile"),
    path("joblist/",views.CandidateJobPostList,name="joblist"),
    path("apply/<int:pk>",views.ApplyPage,name="apply"),
    path("applyjob/<int:pk>",views.ApplyJob,name = "applyjob"),



    ##################Company Side #################################################################
    path("companyindex/",views.CompanyIndexPage,name="companyindex"),
    path("companyprofile/<int:pk>",views.CompanyProfilePage,name="companyprofile"),
    path("updatecompanyprofile/<int:pk>",views.UpdatecompanyProfile,name="updatecompanyprofile"),
    path("jobpostpage/",views.JobPostPage,name="jobpostpage"),
    path("jobpost/<int:pk>",views.JobDetailsSubmit,name="jobpost"),
    path("jobpostlist/",views.JobPostList,name="jobpostlist"),
    path("applyjoblist/",views.jobApplyList,name="applylist"),

    # Logouts
    path("companylogout/",views.CompanyLogout,name="companylogout"),
    path("candidatelogout/",views.CandidateLogout,name="candidatelogout"),
     

    ###########Admin Site####################
    path("adminloginpage/",views.AdminLoginPage,name="adminloginpage"),
    path("adminindexpage/",views.AdminIndexPage,name="adminindexpage"),
    path("adminlogin/",views.AdminLogin,name="adminlogin"),
    path("adminuserlist/",views.AdminUserList,name="userlist"),
    path("admincompanylist/",views.AdminCompanyList,name="companylist"),
    path("userdelete/<int:pk>",views.UserDelete,name="userdelete"),
    path("verifycompanypage/<int:pk>",views.VerifyCompanyPage,name="verifypage"),
    path("updatecompanyprofile/<int:pk>",views.UpdateCompanyProfile,name="updatecompanyprofile"),
    path("companydelete/<int:pk>",views.CompanyDelete,name="companydelete")



    
    
]