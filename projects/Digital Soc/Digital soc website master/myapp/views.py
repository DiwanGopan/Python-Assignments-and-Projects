from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from django.contrib import messages
from django.utils import timezone
from uuid import uuid4

# Create your views here.

def index(request):
    if "email" in request.session:

        u_id = User.objects.get(email=request.session["email"])
        
        if u_id.role=="chairman":
            cid=Chairman.objects.get(user_id=u_id)
            context={
                "u_id":u_id,
                "cid":cid
            }
            return render(request,"myapp/index.html",context)
        else:
            mem_id = Member.objects.get(m_user_id=u_id)
            context={
                "u_id":u_id,
                "mem_id":mem_id
            }
            return render(request,"myapp/mem_index.html", context)
    else:
        return render(request,"myapp/login.html")
 
        
def login(request):
    if "email" in request.session:
        return redirect("home")
    else:
        if request.POST:
            v_email=request.POST['email']
            v_password=request.POST['password']
            try:
                u_id=User.objects.get(email=v_email)

                if u_id.password == v_password and u_id.role=="chairman":
                    cid=Chairman.objects.get(user_id=u_id)
                    request.session['email']=v_email
                    context={
                        "u_id":u_id,
                        "cid":cid
                    }
                    return render(request,"myapp/index.html",context)

                elif u_id.password == v_password and u_id.role == "member":
                    mem_id = Member.objects.get(m_user_id=u_id)
                    request.session["email"] = v_email
                    context={
                        "u_id":u_id,
                        "mem_id":mem_id
                    }
                    return render(request,"myapp/mem_index.html",context)
                    
                else:
                    context={
                        "msg":"Invalid password"
                            }
                return render(request,"myapp/login.html",context)
                    
            except Exception as e:
                print(f"\n\n\n{e}\n\n\n")
                context={"msg":"Invalid Email address"}  
                return render(request,"myapp/login.html",context)
        else:

            return render(request,"myapp/login.html")


def profile(request):
    if "email" in request.session:
        u_id=User.objects.get(email=request.session["email"])
        cid=Chairman.objects.get(user_id=u_id)
        if cid:
            context={
                "u_id":u_id,
                "cid":cid
            }
            return render(request,"myapp/profile.html",context)
        else:
             return render(request,"myapp/login.html")
    else:
         return render(request,"myapp/login.html")


def logout(request):
    if "email" in request.session:
        del request.session['email']

        return render(request,"myapp/login.html")
        
    else:
        return render(request,"myapp/login.html")


def change_password(request):
    if "email" in request.session :
        u_id = User.objects.get(email = request.session["email"])
        cid = Chairmamn.objects.get(user_id = u_id)

        if request.POST:
            old_password = request.POST["password"]
            new_password = request.POST["newpassword"]
            confirm_password = request.POST["cpassword"]
            
            if old_password != new_password :
                if old_password == u_id.password:
                    if new_password == confirm_password:
                        u_id.password = new_password
                        u_id.save()
                        context = {
                            "smsg" : "Your pasword is successfully changed...",
                            "cid" : cid,
                            "u_id" : u_id,

                        }
                        return render(request, "myapp/profile.html", context)
                    else:
                        context = {
                            "emsg" : "confirm password and new password doesn't match", 
                            "cid" : cid,
                            "u_id" : u_id,
                        }
                        return render(request, "myapp/profile.html", context)     
                else:
                    context = {
                        "emsg" : " old password is wrong", 
                        "cid" : cid ,
                        "u_id" : u_id, 
                    }
                    return render(request, "myapp/profile.html", context)    
            else:
                context = {
                    "emsg" : "old password and new password is same", 
                    "cid" : cid,
                    "u_id" : u_id,
                }
                return render(request, "myapp/profile.html", context) 
        else:
            context = {
                "emsg" : "something went wrong...",
                "cid" : cid,
                "u_id" : u_id,
            }
            return render(request, "myapp/profile.html", context)


def editprofile(request):
    if "email" in request.session:
        u_id=User.objects.get(email=request.session["email"])
        if request.POST:
            cid=Chairman.objects.get(user_id=u_id)
            if cid:
                cid.firstname=request.POST['fname']
                cid.lastname=request.POST['lname']
                cid.contact=request.POST['contact']
                cid.block_no=request.POST['blockno']
                cid.house_no=request.POST['house_no']
                cid.aboutme=request.POST['aboutme']

                if "pic" in request.FILES:
                    cid.pic=request.POST['pic']

                cid.save()
                context={
                    "s_msg":"u_id successfully updated",
                    "cid":cid,
                    "u_id":u_id
                        }
                return render(request,"myapp/profile.html",context)
            else:
                context={
                    "e_msg":"Error while updating u_id",
                    "cid":cid
                        }
            return render(request,"myapp/profile.html",context)


def mem_profile(request):
    if "email" in request.session:
        u_id = User.objects.get(email=request.session["email"])

        mem_id = Member.objects.get(m_user_id=u_id)
        context={
                "u_id":u_id,
                "mem_id":mem_id
                }
        return render(request,"myapp/mem-profile.html",context)
    else:
         return render(request,"myapp/login.html")


def mem_edit_profile(request):
    if "email" in request.session:
        u_id=User.objects.get(email=request.session["email"])
        if request.POST:
            mem_id = Member.objects.get(m_user_id=u_id)
            
            if mem_id:
                mem_id.m_f_name = request.POST["f_name"]
                mem_id.m_l_name = request.POST["l_name"]
                mem_id.dob = request.POST["dob"]
                mem_id.gender = request.POST["gender"]
                mem_id.vehicle = request.POST["vehicle"]
                mem_id.work = request.POST["work"]
                mem_id.m_block_no = request.POST["block_no"]
                mem_id.m_house_no = request.POST["house_no"]
                mem_id.family_member = request.POST["family_member"]
                mem_id.contact_no = request.POST["contact"]
                mem_id.m_about_me = request.POST["mem_about_me"]
    
                mem_id.save()

                if "m_pic" in request.FILES:
                    print("\n\n\n 5 \n\n\n")
                    mem_id.m_pic = request.FILES["m_pic"]
                    mem_id.save()

                print("\n\n\n 6 \n\n\n")
                context={
                    "s_msg":"Profile successfully updated",
                    "mem_id":mem_id,
                    "u_id":u_id
                        }
                return render(request,"myapp/mem-profile.html",context)
        else:
            context={
                "e_msg":"Error while updating u_id",
                "mem_id":mem_id
                    }
            return render(request,"myapp/mem-profile.html",context)
    else:
        return render(request,"myapp/login.html")


def mem_change_password(request):
    if "email" in request.session :
        u_id = User.objects.get(email = request.session["email"])
        mem_id = Member.objects.get(m_user_id = u_id)

        if request.POST:
            old_password = request.POST["password"]
            new_password = request.POST["newpassword"]
            confirm_password = request.POST["cpassword"]
            
            if old_password != new_password :
                if old_password == u_id.password:
                    if new_password == confirm_password:
                        u_id.password = new_password
                        u_id.save()
                        context = {
                            "smsg" : "Your pasword is successfully changed...",
                            "mem_id" : mem_id,
                            "u_id" :u_id,

                        }
                        return render(request, "myapp/mem-profile.html", context)
                    else:
                        context = {
                            "emsg" : "confirm password and new password doesn't match", 
                            "mem_id" : mem_id,
                            "u_id" :u_id,

                        }
                        return render(request, "myapp/mem-profile.html", context)     
                else:
                    context = {
                        "emsg" : " old password is wrong", 
                        "mem_id" : mem_id,
                        "u_id" :u_id,

                    }
                    return render(request, "myapp/mem-profile.html", context)    
            else:
                context = {
                    "emsg" : "old password and new password is same", 
                    "mem_id" : mem_id,
                    "u_id" :u_id,

                }
                return render(request, "myapp/mem-profile.html", context) 
        else:
            context = {
                "emsg" : "something went wrong...",
                "mem_id" : mem_id,
                "u_id" :u_id,

            }
            return render(request, "myapp/mem-profile.html", context)
    else:
        return render(request, "myapp/login.html")


def add_member(request):
    if "email" in request.session:
        u_id = User.objects.get(email=request.session["email"])
        cid = Chairman.objects.get(user_id=u_id)
        context = {
                "u_id" : u_id,
                "cid" : cid,
        }
        if request.method == "POST":

            passwrd = str(uuid4())[:6]

            new_u_id = User.objects.create(
                email=request.POST["email"],
                role= "member",
                password=passwrd,
            )
            new_u_id.save()
            
            mem_uid = User.objects.get(email=request.POST["email"])

            if mem_uid:
                mem_id = Member.objects.create(
                    m_user_id= mem_uid,
                    m_f_name=request.POST["f_name"],
                    m_l_name=request.POST["l_name"],
                    dob=request.POST["dob"],
                    gender=request.POST["gender"],
                    vehicle=request.POST["vehicle"],
                    work=request.POST["work"],
                    m_block_no=request.POST["block_no"],
                    m_house_no=request.POST["house_no"],
                    family_member=request.POST["family_member"],
                    contact_no=request.POST["contact"],
                    m_about_me=request.POST["mem_about_me"],
                )
                mem_id.save()
                context = {
                    "u_id" : u_id,
                    "cid" : cid,
                }
                if "m_pic" in request.FILES:
                    mem_id.m_pic = request.FILES["m_pic"]
                    mem_id.save()

                if mem_id:
                    messages.success(request, 'SuccessFully Add details')
                    return render(request,"myapp/add_member.html",context)
                else:
                    messages.error(request, 'Error While Adding Member')
                    return render(request, "myapp/add_member.html", context)
            else:
                messages.error(request, 'Error While Adding Member')
                return render(request, "myapp/add_member.html", context)
        else:
            return render(request, "myapp/add_member.html", context)
    else:
        return render(request, "myapp/login.html")


def all_member(request):
    if "email" in request.session:
        u_id = User.objects.get(email=request.session["email"])
        cid = Chairman.objects.get(user_id=u_id)
        mem_id = Member.objects.all()
        context = {
            "mem_id" : mem_id,
            "u_id" : u_id,
            "cid" : cid,
        }
        return render(request, "myapp/all-member.html", context)
    else:
        return render(request, "myapp/login.html")


def delete_member(request, pk):
    if "email" in request.session:
        mem_id = Member.objects.get(pk=pk)
        mem_id.delete()
        return redirect("all_member")


def add_notice(request):
    if "email" in request.session:
        u_id = User.objects.get(email=request.session["email"])
        cid = Chairman.objects.get(user_id=u_id)
        context = {
            "u_id" : u_id,
            "cid" : cid,
        }
        if request.POST:
            noc_id = Notice.objects.create(
                user_id=cid,
                title=request.POST["title"],
                content = request.POST["n_content"]
            )
            noc_id.save()

            if "n_pic" in request.FILES:
                noc_id.n_pic = request.FILES["n_pic"]
                noc_id.save()

            if "n_video" in request.FILES:
                noc_id.n_video = request.FILES.get("n_video")
                noc_id.save()

            if noc_id:
                messages.success(request, 'SuccessFully Add details')
                return render(request,"myapp/add_notice.html",context)
            else:
                messages.error(request, 'Error While Adding Member')
                return render(request, "myapp/add_notice.html", context)
        else:
            return render(request, "myapp/add_notice.html", context)
    else:
        return render(request, "myapp/login.html")


def all_notice(request):
    
    if "email" in request.session:
        u_id = User.objects.get(email=request.session["email"])
        cid = Chairman.objects.get(user_id=u_id)
        noc_id = Notice.objects.all()
        context = {
            "noc_id" : noc_id,
            "u_id" : u_id,
            "cid" : cid,
        }
        return render(request, "myapp/all-notice.html", context)
    else:
        return render(request, "myapp/login.html")


def delete_notice(request, pk):
    if "email" in request.session:
        noc_id = Notice.objects.get(pk=pk)
        noc_id.delete()
        return redirect("all_notice")


def add_event(request):
    if "email" in request.session:
        u_id = User.objects.get(email=request.session["email"])
        cid = Chairman.objects.get(user_id=u_id)
        context = {
            "u_id" : u_id,
            "cid" : cid,
        }
        if request.POST:
            eve_id = Event.objects.create(
                user_id = cid,
                e_title = request.POST["e_title"],
                e_content = request.POST["e_content"],
                e_date = request.POST["e_date"],
                e_venue = request.POST["e_venue"]
            )
            eve_id.save()

            if "e_pic" in request.FILES:
                eve_id.e_pic = request.FILES["e_pic"]
                eve_id.save()

            if eve_id:
                messages.success(request, 'SuccessFully Add details')
                return render(request,"myapp/add_event.html",context)
            else:
                messages.error(request, 'Error While Adding Member')
                return render(request, "myapp/add_event.html", context)
        else:
            return render(request, "myapp/add_event.html", context)
    else:
        return render(request, "myapp/login.html")


def all_event(request):
    if "email" in request.session:
        u_id = User.objects.get(email=request.session["email"])
        cid = Chairman.objects.get(user_id=u_id)
        eve_id = Event.objects.all()
        context = {
            "eve_id" : eve_id,
            "u_id" : u_id,
            "cid" : cid,
        }
        return render(request, "myapp/all-event.html", context)
    else:
        return render(request, "myapp/login.html")


def delete_event(request, pk):
    if "email" in request.session:
        eve_id = Event.objects.get(pk=pk)
        eve_id.delete()
        return redirect("all_event")


def mem_all_notice(request):
    if "email" in request.session:
        u_id = User.objects.get(email=request.session["email"])
        mem_id = Member.objects.get(m_user_id=u_id)
        noc_id = Notice.objects.all()
        context = {
            "noc_id" : noc_id,
            "u_id" : u_id,
            "mem_id" : mem_id,
        }
        return render(request, "myapp/mem-all-notice.html", context)
    else:
        return render(request, "myapp/login.html")


def mem_all_notice(request):
    if "email" in request.session:
        u_id = User.objects.get(email=request.session["email"])
        mem_id = Member.objects.get(m_user_id=u_id)
        noc_id = Notice.objects.all()
        context = {
            "noc_id" : noc_id,
            "u_id" : u_id,
            "mem_id" : mem_id,
        }
        return render(request, "myapp/mem-all-notice.html", context)
    else:
        return render(request, "myapp/login.html")


def mem_all_event(request):
    if "email" in request.session:
        u_id = User.objects.get(email=request.session["email"])
        mem_id = Member.objects.get(m_user_id=u_id)
        eve_id = Event.objects.all()
        context = {
            "eve_id" : eve_id,
            "u_id" : u_id,
            "mem_id" : mem_id,
        }
        return render(request, "myapp/mem-all-event.html", context)
    else:
        return render(request, "myapp/login.html")


def mem_all_member(request):
    if "email" in request.session:
        u_id = User.objects.get(email=request.session["email"])
        mem_id = Member.objects.get(m_user_id = u_id)
        mem1_id = Member.objects.all()
        context = {
            "mem_id" : mem_id,
            "mem1_id" : mem1_id,
            "u_id" : u_id,
        }
        return render(request, "myapp/mem-all-member.html", context)
    else:
        return render(request, "myapp/login.html")
