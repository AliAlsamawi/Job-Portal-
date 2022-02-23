from django.shortcuts import render,redirect

# for chacking exiesting data for eg. email addresses
from .models import *

# for generating OTP
from random import randint

# Create your views here.
def IndexPage(request):
    return render(request,'jobportal/index.html')

def SignupPage(request):
    return render(request,'jobportal/signup.html')

def RegisterPage(request):
    if request.POST['role']=="Candidate":
        # storing the data which is come from html signup page
        role = request.POST['role'] 
        fname = request.POST['firstname']
        lname= request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        user = UserMaster.objects.filter(email=email)

        if user:
            message = " User already exiested"
            return render(request,'jobportal/signup.html',{'msg':message})
        else:
            if password == cpassword:
                otp = randint(100000,999999)
                # store information in table
                newuser = UserMaster.objects.create(role=role,otp=otp,email=email,password=password)

                newcand = Candidate.objects.create(user_id=newuser,firstname=fname,lastname=lname)
                return render(request,'jobportal/otpverify.html',{"email":email})
    else:
        if request.POST['role'] == "Company":
            role = request.POST['role']
            fname = request.POST['firstname']
            lname = request.POST['lastname']
            email = request.POST['email']
            password = request.POST['password']
            cpassword = request.POST['cpassword']

            user = UserMaster.objects.filter(email=email)

            if user:
                message = "Company email is already in use."
                return render(request,'jobportal/signup.html',{'msg':message})
            else:
                if password == cpassword:
                    otp = randint(100000,999999)
                    newuser = UserMaster.objects.create(role=role,otp=otp,email=email,password=password)
                    newcomp = Company.objects.create(user_id=newuser,firstname=fname,lastname=lname)
                    return render(request, 'jobportal/otpverify.html',{"email":email})



# Otp page view

def OTPPage(request):
    return render(request,'jobportal/otpverify.html')

# otp verify page

def Otpverify(request):
    email = request.POST['email']
    otp = int(request.POST['otp'])
    
    user = UserMaster.objects.get(email=email)

    if user:
        if user.otp == otp:
            message = "OTP Verified Successfully!!!"
            return render(request, 'jobportal/login.html',{'msg':message})
        else:
            message = "incorret otp"
            return render(request,'jobportal/otpverify.html',{'msg':message})
    else:
        return render(request,'jobportal/signup.html')

# Login page view

def LoginPage(request):
    return render(request,'jobportal/login.html')


def LoginUser(request):
    if request.POST['role'] == 'Candidate' :

        email = request.POST['email']
        password = request.POST['password']

        user = UserMaster.objects.get(email=email)
        if user:
            if user.password == password and user.role == "Candidate":
                can = Candidate.objects.get(user_id=user)
                request.session['id'] = user.id
                request.session['role'] = user.role
                request.session['firstname'] = can.firstname
                request.session['lastname'] = can.lastname
                request.session['email'] = user.email
                request.session['password'] = user.password
                return redirect('index')
            else:
                message = "Password does not matched"
                return render(request,'jobportal/login.html',{'msg':message})
        else:
            message = "User does not exiest"
            return render(request,'jobportal/login.html',{'msg':message})
    else:
        if request.POST['role'] == 'Company':
            email = request.POST['email']
            password = request.POST['password']

            user = UserMaster.objects.get(email=email)
            if user:
                if user.password == password and user.role == 'Company':
                    com=Company.objects.get(user_id = user)
                    request.session['id'] = user.id
                    request.session['role'] = user.role
                    request.session['firstname'] = com.firstname
                    request.session['lastname'] = com.lastname
                    request.session['email'] = user.email
                    request.session['password'] = user.password
                    return redirect('companyindex')
                else:
                    message="password does not matched"
                    return render(request,'jobportal/login.html',{'msg':message})
            else:
                message = "User does not Exiest"
                return render(request,'jobportal/login.html',{'msg':message})


# Profile page views

def ProfilePage(request,pk):
    # pass the primary key to access master table data
    # this view display the registration time save details

    user = UserMaster.objects.get(pk=pk)
    can = Candidate.objects.get(user_id = user)
    return render(request,'jobportal/profile.html',{'user':user, 'can':can})

# This view Update the data in profile page and first it add the data in database then display on the page
def ProfileUpdate(request,pk):
    # user = request.objects.get(pk=pk)
    user=UserMaster.objects.get(pk=pk)
    if user.role == 'Candidate':
        can = Candidate.objects.get(user_id=user)
        can.contact=request.POST['contact'] #First method belongs to database field and second method belongs to html page
        can.state=request.POST['state']
        can.city=request.POST['city']
        # c.['address']=request.POST['address']
        # c.['dob']=request.POST['dob']
        can.gender=request.POST['gender']
        can.min_salary=request.POST['min_salary']
        can.max_salary=request.POST['max_salary']
        can.job_type=request.POST['job_type']
        # c.['country']=request.POST['country']
        can.highestedu=request.POST['highestedu']
        can.experience=request.POST['experience']
        can.website=request.POST['website']
        can.shift=request.POST['shift']
        can.jobdescription=request.POST['jobdescription']
        # can.profile_pic=request.FILES['profile_pic']
        can.save()
        #FORMATING URL
        url = f'/profile/{pk}'
        return redirect(url)

def ApplyPage(request,pk):
    user = request.session['id']
    if user:
        cand = Candidate.objects.get(user_id=user)
        job = JobDetails.objects.get(id=pk)
        return render(request,"jobportal/apply.html",{'user':user,'cand':cand,'job':job})

def ApplyJob(request,pk):
    user = request.session['id']
    if user: 
        can = Candidate.objects.get(user_id = user)
        job = JobDetails.objects.get(id=pk)
        min_salary = request.POST['min_salary']
        max_salary = request.POST['max_salary']
        edu = request.POST['education']
        exp = request.POST['experience']
        web = request.POST['website']
        gender = request.POST['gender']
        resume = request.FILES.get('resume')
        newapply = ApplyList.objects.create(candidate=can,job=job,education=edu,experience=exp,
        website=web,min_salary=min_salary,max_salary=max_salary,gender=gender,resume=resume)
        message="apply message Successfully"
        return render(request,"jobportal/apply.html",{'msg':message})


        ####################### Company Side ###################################
def CompanyIndexPage(request):
    return render(request, 'jobportal/company/index.html')

def CompanyProfilePage(request,pk):
    user = UserMaster.objects.get(pk=pk)
    comp = Company.objects.get(user_id=user)
    return render(request, 'jobportal/company/companyprofile.html',{'user':user,'comp':comp})


def UpdatecompanyProfile(request,pk):
    user = UserMaster.objects.get(pk=pk)
    if user.role =="Company":
        comp = Company.objects.get(user_id=user)
        comp.firstname = request.POST['firstname']
        comp.lastname = request.POST['lastname']
        comp.company_name = request.POST['company_name']
        comp.state = request.POST['state']
        comp.city = request.POST['city']
        comp.contact = request.POST['contact']
        # comp.address = request.POST['address']
        comp.website = request.POST['website']
        comp.description = request.POST['description']
        # comp.logo_pic = request.FILES['logo_pic']
        comp.save()
        url = f'/companyprofile/{pk}'
        return redirect(url)
        
# Job post view page
def JobPostPage(request):
    return render(request, 'jobportal/company/jobpost.html')

def JobDetailsSubmit(request,pk):    
    # user = UserMaster.objects.get(id=request.session.id)
    user=UserMaster.objects.get(pk=pk)
    if user.role == "Company":
        comp = Company.objects.get(user_id=user)
        jobname = request.POST['jobname']
        companyname = request.POST['companyname']
        companyaddress = request.POST['companyaddress']
        jobdescription = request.POST['jobdescription']
        qualification = request.POST['qualification']
        responsibilities = request.POST['responsibilities']
        location = request.POST['location']
        companywebsite = request.POST['companywebsite']
        companyemail = request.POST['companyemail']
        companycontact = request.POST['companycontact']
        salarypackage = request.POST['salarypackage']
        experience = request.POST['experience']
        # logo = request.FILES['image']

        newjob = JobDetails.objects.create(company_id=comp,jobname=jobname,companyname=companyname,companyaddress=companyaddress,
        jobdescription=jobdescription,qualification=qualification,responsibilities=responsibilities,location=location,
        companywebsite=companywebsite,companyemail=companyemail,companycontact=companycontact,salarypackage=salarypackage,experience=experience)

        message = "Job post Successfully"
        return render(request,'jobportal/company/jobpost.html',{'msg':message})


# JobPostList View

def JobPostList(request):q
    all_job = JobDetails.objects.all()
    return render(request,"jobportal/company/jobpostlist.html",{'all_job':all_job})
  
# Candidate site
def CandidateJobPostList(request):
    all_job = JobDetails.objects.all()
    return render(request,"jobportal/job-list.html",{'all_job':all_job})

def jobApplyList(request):
    all_jobapply = ApplyList.objects.all()
    return render (request,"jobportal/company/applyjoblist.html",{'all_job':all_jobapply})

def CompanyLogout(request):
    del request.session['email']
    del request.session['password']
    return redirect('index')


def CandidateLogout(request):
    del request.session['email']    
    del request.session['password']
    return redirect('index')


##############ADMIN SITE##########
def AdminLoginPage(request):
    return render(request,"jobportal/admin/login.html")


def AdminIndexPage(request):
    if 'username' in request.session and 'password' in request.session:
        return render(request,"jobportal/admin/index.html")
    else:
        return redirect('adminloginpage')

       

def AdminLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    if username == "admin" and password == "password":
        request.session['username'] = username
        request.session['password'] = password
        return redirect('adminindexpage')
    else:
        message = "Username and Password does not matched"
        return render(request,"jobportal/admin/login.html",{'msg':message })


def AdminUserList(request):
    all_user = UserMaster.objects.filter(role="Candidate")
    return render(request,"jobportal/admin/userlist.html",{'alluser':all_user})

def AdminCompanyList(request):
    all_company = UserMaster.objects.filter(role="Company")
    return render(request,"jobportal/admin/companylist.html",{'allcompany':all_company})


def UserDelete(request,pk):
    user = UserMaster.objects.get(pk=pk)
    user.delete()
    return redirect('userlist')

def VerifyCompanyPage(request,pk):
    company = UserMaster.objects.get(pk=pk)
    if company:
        return render(request,"jobportal/admin/verify.html",{'company':company})


def UpdateCompanyProfile(request,pk):
    company = UserMaster.objects.get(pk=pk)
    if company:
        company.is_verified = request.POST['verify']
        company.save()
        return redirect('companylist')

def CompanyDelete(request,pk):
    company = UserMaster.objects.get(pk=pk)
    company.delete()
    return redirect('companylist')