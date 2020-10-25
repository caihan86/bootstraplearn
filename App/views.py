from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from App.models import ImeiForm


def index(request):
    if request.method == 'GET':
        dealforms = ImeiForm.objects.filter(Q(f_dealman='测试人员2'))
        myforms = ImeiForm.objects.filter(Q(f_createman='测试人员2'))
        data = {
            'title': 'ImeiM&C-个人中心',
            'dealformlist': dealforms,
            'myformlist': myforms
        }
        return render(request, 'main_home.html', context=data)
    elif request.method == "POST":
        data = {
            'title': 'ImeiM&C-个人中心',
        }
        return render(request, 'main_home.html', context=data)


def login(request):
    return render(request, 'login.html')


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
        paginator = Paginator(searchresult, 10)
        page_object = paginator.page(page)
        result_list = list(page_object.object_list.values())
        result = {'has_previous': page_object.has_previous(),
                  'has_next': page_object.has_next(),
                  'result_list': result_list}
        # print(result)
        return JsonResponse(result)
    elif request.method == 'GET':
        print(2)
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
    for i in range(1, 100):
        iform = ImeiForm()
        iform.f_title = 'TestModify' + str(i)
        iform.f_content = '测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试'
        iform.f_createman = '测试人员1'
        iform.f_lastdealman = '测试人员2'
        iform.f_dealman = '测试人员3'
        iform.f_type = 'modify'
        iform.f_status = '0'
        iform.save()
    for i in range(1, 100):
        iform = ImeiForm()
        iform.f_title = 'TestCancel' + str(i)
        iform.f_content = '测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试'
        iform.f_createman = '测试人员1'
        iform.f_lastdealman = '测试人员2'
        iform.f_dealman = '测试人员3'
        iform.f_type = 'cancel'
        iform.f_status = '0'
        iform.save()
    return HttpResponse('ok')
