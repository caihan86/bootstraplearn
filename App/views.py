import uuid
from time import sleep

from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.cache import cache_page

from App.models import ImeiForm, f_status_convert, User, DealRecorde, Attachment
from App.utils import decrypt_data


def index(request):
    if request.method == 'GET':
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        dealforms = ImeiForm.objects.filter(~Q(_f_status=4)).filter(Q(f_dealman=user.username))
        dealforms = dealforms.order_by('-f_lastmodifytime')
        deal_paginator = Paginator(dealforms, 5)
        dealformslist = deal_paginator.page(1)
        deal_range = deal_paginator.page_range
        deal_count = dealforms.count()
        myforms = ImeiForm.objects.filter(~Q(_f_status=4)).filter(Q(f_createman=user.username))
        myforms = myforms.order_by('-f_lastmodifytime')
        my_paginator = Paginator(myforms, 5)
        myformslist = my_paginator.page(1)
        my_range = my_paginator.page_range
        my_count = myforms.count()

        data = {
            'title': 'ImeiM&C-个人中心',
            'dealformlist': dealformslist,
            'deal_range': deal_range,
            'deal_count': deal_count,
            'myformlist': myformslist,
            'my_range': my_range,
            'my_count': my_count,
            'page': 1,
        }
        return render(request, 'main_home.html', context=data)
    elif request.method == "POST":

        data = {
            'title': 'ImeiM&C-个人中心',
        }
        return render(request, 'main_home.html', context=data)


def login(request):
    if request.method == 'GET':
        data = {
            'title': 'ImeiM&C-登陆页面'
        }
        return render(request, 'login.html', context=data)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = decrypt_data(password)
        user = User.objects.get(username=username)
        if user and user.check_password(password):
            response = redirect(reverse('app:home'))
            request.session['userid'] = user.id
            token = uuid.uuid4().hex
            response.set_cookie('token', token, max_age=60 * 60 * 24 * 7)
            cache.set(token, user.id, 60 * 60 * 24 * 7)
            return response


def register(request):
    if request.method == 'GET':
        data = {
            'title': 'ImeiM&C-注册页面'
        }
        return render(request, 'register.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        user = User()
        user.username = username
        user.mobile_number = mobile_number
        user.password = decrypt_data(password)
        user.save()
        return redirect(reverse('app:login'))


def testbs(request):
    return render(request, 'test.html')


def formsearch(request):
    if request.is_ajax():
        page = request.GET.get('page')
        formid = request.GET.get('formid')
        keyword = request.GET.get('keyword')
        createman = request.GET.get('createman')
        dealman = request.GET.get('dealman')
        status = request.GET.get('status')
        formtype = request.GET.get('formtype')
        begintime = request.GET.get('begintime')
        endtime = request.GET.get('endtime')
        searchresult = ImeiForm.objects.filter(Q(_f_status=status)).filter(Q(f_type=formtype))
        if formid.strip() != '':
            searchresult = searchresult.filter(Q(id=formid))
        if keyword.strip() != '':
            searchresult = searchresult.filter(Q(f_title__contains=keyword) | Q(f_content__contains=keyword))
        if createman.strip() != '':
            searchresult = searchresult.filter(Q(f_createman=createman))
        if dealman.strip() != '':
            searchresult = searchresult.filter(Q(f_dealman=dealman))
        if begintime != '' and endtime != '':
            searchresult = searchresult.filter(Q(f_createtime__gte=begintime) & Q(f_createtime__lte=endtime))
        searchresult = searchresult.order_by('-f_lastmodifytime')
        paginator = Paginator(searchresult, 10)
        page_object = paginator.page(page)
        result_list = list(page_object.object_list.values())
        for formdata in result_list:
            formdata['_f_status'] = f_status_convert.get(formdata['_f_status'])
            formdata['f_lastmodifytime'] = formdata['f_lastmodifytime'].strftime('%Y-%m-%d %H:%M:%S')
        result = {'has_previous': page_object.has_previous(),
                  'has_next': page_object.has_next(),
                  'result_list': result_list}
        # print(result_list)
        return JsonResponse(result)
    elif request.method == 'GET':
        data = {
            'title': 'ImeiM&C-工单查询',
        }
        return render(request, 'main_search.html', context=data)

    elif request.method == 'POST':
        formid = request.POST.get('inputFormid')
        keyword = request.POST.get('inputKeyword')
        createman = request.POST.get('inputCreateman')
        dealman = request.POST.get('inputDealman')
        status = request.POST.get('inputStatus')
        formtype = request.POST.get('inputType')
        begintime = request.POST.get('inputBegintime')
        endtime = request.POST.get('inputEndtime')
        print(formtype)

        searchresult = ImeiForm.objects.filter(Q(_f_status=status)).filter(Q(f_type=formtype))
        if formid.strip() != '':
            searchresult = searchresult.filter(Q(id=formid))
        if keyword.strip() != '':
            searchresult = searchresult.filter(Q(f_title__contains=keyword) | Q(f_content__contains=keyword))
        if createman.strip() != '':
            searchresult = searchresult.filter(Q(f_createman=createman))
        if dealman.strip() != '':
            searchresult = searchresult.filter(Q(f_dealman=dealman))
        if begintime != '' and endtime != '':
            searchresult = searchresult.filter(Q(f_createtime__gte=begintime) & Q(f_createtime__lte=endtime))
        searchresult = searchresult.order_by('-f_lastmodifytime')
        paginator = Paginator(searchresult, 10)
        page_object = paginator.page(1)
        # print(len(list(page_object.object_list.values())))
        resultlength = len(list(page_object.object_list.values()))
        data = {
            'title': 'ImeiM&C-工单查询',
            'formlist': page_object,
            'page_range': paginator.page_range,
            'page': 1,
            'formid': formid,
            'keyword': keyword,
            'createman': createman,
            'dealman': dealman,
            'status': status,
            'formtype': formtype,
            'begintime': begintime,
            'endtime': endtime,
            'resultlength': resultlength
        }
        return render(request, 'main_search.html', context=data)


def addform(request):
    for i in range(1, 10):
        iform = ImeiForm()
        iform.f_title = 'TestModify' + str(i)
        iform.f_content = '测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试'
        iform.f_createman = 'caihan'
        iform.f_lastdealman = '测试人员1'
        iform.f_dealman = '测试人员2'
        iform.f_type = 'modifytype'
        iform.f_status = '0'
        iform.save()
    for i in range(1, 10):
        iform = ImeiForm()
        iform.f_title = 'TestCancel' + str(i)
        iform.f_content = '测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试'
        iform.f_createman = '测试人员3'
        iform.f_lastdealman = '测试人员1'
        iform.f_dealman = 'caihan'
        iform.f_type = 'canceltype'
        iform.f_status = '0'
        iform.save()
    return HttpResponse('ok')


def getdealform(request):
    if request.is_ajax():
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        pagenum = request.GET.get('page')
        dealforms = ImeiForm.objects.filter(Q(f_dealman=user.username))
        dealforms = dealforms.order_by('-f_lastmodifytime')
        deal_paginator = Paginator(dealforms, 5)
        page_object = deal_paginator.page(pagenum)
        result_list = list(page_object.object_list.values())
        for formdata in result_list:
            formdata['_f_status'] = f_status_convert.get(formdata['_f_status'])
            formdata['f_lastmodifytime'] = formdata['f_lastmodifytime'].strftime('%Y-%m-%d %H:%M:%S')
        result = {'has_previous': page_object.has_previous(),
                  'has_next': page_object.has_next(),
                  'result_list': result_list}
        # print(result_list)
        return JsonResponse(result)


def getmyform(request):
    if request.is_ajax():
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        pagenum = request.GET.get('page')
        myforms = ImeiForm.objects.filter(Q(f_createman=user.username))
        myforms = myforms.order_by('-f_lastmodifytime')
        my_paginator = Paginator(myforms, 5)
        page_object = my_paginator.page(pagenum)
        result_list = list(page_object.object_list.values())
        for formdata in result_list:
            formdata['_f_status'] = f_status_convert.get(formdata['_f_status'])
            formdata['f_lastmodifytime'] = formdata['f_lastmodifytime'].strftime('%Y-%m-%d %H:%M:%S')
        result = {'has_previous': page_object.has_previous(),
                  'has_next': page_object.has_next(),
                  'result_list': result_list}
        # print(result_list)
        return JsonResponse(result)


def formdetail(request, id):
    userid = request.session['userid']
    user = User.objects.get(id=userid)

    if request.method == 'GET':
        formdata = ImeiForm.objects.get(id=id)
        dealdata = formdata.form_dealrec.order_by('-dealtime')
        attachdata = formdata.form_attach.order_by('-uploadtime')
        if formdata.f_type == 'modifytype':
            formdata.f_type = '修改捆绑'
        elif formdata.f_type == 'canceltype':
            formdata.f_type = '取消捆绑'
        data = {
            'title': 'ImeiM&C-工单详情',
            'formdata': formdata,
            'dealdata': dealdata,
            'attachdata': attachdata,
            'user': user
        }
        return render(request, 'form_detail.html', context=data)
    elif request.method == 'POST':
        formdata = ImeiForm.objects.get(id=id)
        dealcontent = request.POST.get('dealcontent')
        nextstatus = request.POST.get('nextstatus')
        dealrec = DealRecorde()
        dealrec.form = formdata
        dealrec.dealman = user.username
        dealrec.dealcontent = dealcontent
        formdata = ImeiForm.objects.get(id=id)
        if nextstatus == 'zuofei':
            formdata.f_status = 4
            dealrec.operate = '作废'
        elif nextstatus == 'tijiao':
            formdata.f_status = 1
            dealrec.operate = '提交'
        elif nextstatus == 'shenpi':
            formdata.f_status = 2
            dealrec.operate = '审批'
        elif nextstatus == 'tuihui':
            formdata.f_status = 3
            dealrec.operate = '退回'
        formdata.save()
        dealrec.save()
        dealdata = formdata.form_dealrec.order_by('-dealtime')
        attachdata = formdata.form_attach.order_by('-uploadtime')
        if formdata.f_type == 'modifytype':
            formdata.f_type = '修改捆绑'
        elif formdata.f_type == 'canceltype':
            formdata.f_type = '取消捆绑'
        data = {
            'title': 'ImeiM&C-工单详情',
            'formdata': formdata,
            'dealdata': dealdata,
            'attachdata': attachdata,
            'user': user
        }
        return render(request, 'form_detail.html', context=data)


def adddealrec(request, formid):
    for i in range(1, 10):
        dealrec = DealRecorde()
        imeiform = ImeiForm.objects.get(id=formid)
        dealrec.form = imeiform
        dealrec.dealman = 'test' + str(i)
        dealrec.dealcontent = '测试处理意见内容'
        dealrec.save()
    return HttpResponse('OK')


def uploadfile(request):
    if request.method == 'POST':
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        formid = request.POST.get('formid')
        form = ImeiForm.objects.get(id=formid)
        upload_file = request.FILES.get('file')
        attach = Attachment()
        attach.uploadman = user.username
        attach.uploadfile = upload_file
        attach.form = form
        attach.save()
        data = {
            'is_valid': True,
            'uploadman': attach.uploadman,
            'uploadtime': attach.uploadtime.strftime('%Y-%m-%d %H:%M:%S'),
            'filename': attach.filename,
            'url': attach.uploadfile.url
        }
        return JsonResponse(data)


def formvalid(request):
    if request.is_ajax():
        formid = request.GET.get('id')
        formdata = ImeiForm.objects.filter(id=formid)
        result = {'is_exist': False}
        if formdata:
            result = {'is_exist': True}
        return JsonResponse(result)


def formnew(request):
    if request.method == 'GET':
        formtype = request.GET.get('formtype')
        if formtype == 'modifytype':
            formtypechs = '修改捆绑'
        elif formtype == 'canceltype':
            formtypechs = '取消捆绑'
        data = {
            'title': 'ImeiM&C-新建工单',
            'formtype': formtype,
            'formtypechs': formtypechs
        }
        return render(request, 'form_new.html', context=data)
    elif request.method == 'POST':
        formtype = request.POST.get('formtype')
        title = request.POST.get('inputTitle')
        descrp = request.POST.get('inputDescrp')
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        form = ImeiForm()
        form.f_title = title
        form.f_type = formtype
        form.f_content = descrp
        form.f_createman = form.f_dealman = form.f_lastdealman = user.username
        form.save()
        return redirect(reverse('app:formdetail', args={form.id}))
