from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from hotel.master.models import CompetitorMaster,PointOfSaleMaster,DomainMaster,CountryMaster
import json
import os
import paramiko
import shutil
import pymysql
#import scp
from django.db import connection
from hotel.views import VisibleDomain



class index(TemplateView):
    """
    django generic view to display template of point of scale.
    """
    template_name = 'hotel/Domain/index.html'

    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        countries = CountryMaster.objects.order_by('name')
        comps = CompetitorMaster.objects.order_by('name')
        domains = DomainMaster.objects.order_by('domainname')
        CompetitorMasters = list(CompetitorMaster.objects.order_by('name').values_list('name', flat=True))
        CompetitorMasters = ','.join(CompetitorMasters)
        context.update(comps=comps)
        context.update(domains=domains)
        context.update(countries=countries)
        context.update(CompetitorMasters=CompetitorMasters)
        return context


@csrf_exempt
def GetDomainName(request):
    if request.method == 'POST' or request.is_ajax():
        data_lis = []
        # Domain = list(DomainMaster.objects.filter().values("id","domainname","country_id","competitorid"))
        db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                            user=settings.DATABASES['default']['USER'],
                            passwd=settings.DATABASES['default']['PASSWORD'],
                            db=settings.DATABASES['default']['NAME'])

        cur = db.cursor()
        # query = """SELECT D.DomainId, D.DomainName,C.name,E.CountryName FROM eCube_Centralized_DB.tbl_DomainMaster D
        #      join tbl_Competitor C on D.Competitorid= C.id
        #       join tbl_CountryMaster E on D.FK_CountryId= E.CountryID order by D.DomainId desc"""

        query = """SELECT D.DomainId, D.DomainName,C.name FROM eCube_Centralized_DB.tbl_DomainMaster D
                     join tbl_Competitor C on D.Competitorid= C.id order by D.DomainId desc"""

        cur.execute(query)
        dataObj = cur.fetchall()
        db.close()
        dataObjlist = []
        

        for row in dataObj:
            datadict = {}
            datadict['id'] = row[0]
            datadict['DomainName'] = row[1]
            datadict['CompetitorName'] = row[2]
            # datadict['CountryName'] = row[3]
            dataObjlist.append(datadict)
        

        data = {
            'country': dataObjlist,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def domain_uploader_file_download(request):
    print('+++++++++++++++++++++++++++++ domain_uploader_file_download')
    if request.method == 'POST' or request.is_ajax():
        domain_id = request.POST.get('comp_id')
        domain_name=DomainMaster.objects.filter(id=domain_id).first().domainname
        #dir_name = "/var/www/eCube_Hotel_2/eCube_UI_2/static/Crawler_Parser_Files/"
        dir_name = "/var/www/eCube_Hotel_2/eCube_UI_2/static/Crawler_Parser_Files/"
        temp_cpath = dir_name + domain_name +"/"
        bli_id = dict(request.session)['bli_id']

        if not os.path.exists(temp_cpath):            
            os.makedirs(temp_cpath)
        else:            
            shutil.rmtree(temp_cpath)
            try:
                os.remove(dir_name + domain_name + ".zip")
            except Exception as e:
                pass

            os.makedirs(temp_cpath)        

        crawl_file_name=DomainMaster.objects.filter(id=domain_id).first().scrapingscriptname
        
        if crawl_file_name is not None and not crawl_file_name == '':
            if not crawl_file_name.endswith('.py'):
                new_file =crawl_file_name + '.py'
            else:
                new_file =crawl_file_name
                        
            get_crawler_server_details_download(bli_id, temp_cpath, crawl_file_name,new_file,1, 'crawl')
                    
        crawl_config_file=DomainMaster.objects.filter(id=domain_id).first().scrapingconfigscriptname

        if crawl_config_file is not None and not crawl_config_file == '':
            if not crawl_config_file.endswith('.py'):
                new_file_1 =crawl_config_file + '.py'
            else:
                new_file_1 =crawl_config_file
                       
            get_crawler_server_details_download(bli_id, temp_cpath, crawl_config_file,new_file_1,2, 'crawl')
        
        parse_file=DomainMaster.objects.filter(id=domain_id).first().parsingscriptname
        
        if parse_file is not None and not parse_file == '':
            if not parse_file.endswith('.py'):
                new_file_2 =parse_file + '.py'
            else:
                new_file_2 =parse_file
                        
            get_crawler_server_details_download(bli_id, temp_cpath, parse_file,new_file_2,3, 'parse')
        
        parse_config_file=DomainMaster.objects.filter(id=domain_id).first().parsingconfigscriptname

        if parse_config_file is not None and not parse_config_file == '':
            if not parse_config_file.endswith('.py'):
                new_file_3 =parse_config_file + '.py'
            else:
                new_file_3 =parse_config_file
                       
            get_crawler_server_details_download(bli_id, temp_cpath, parse_config_file,new_file_3,4, 'parse')

        shutil.make_archive(temp_cpath,'zip',temp_cpath)
        
        data= {
                'crawl_file': "/static/Crawler_Parser_Files/"+domain_name+".zip" 
                

              }

        print('+++++++++++++++++++++++++++++++++++++ Return')
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)
@csrf_exempt
def domain_uploader_post(request):
    domain = request.POST.get('domain')
    competitor = request.POST.get('competitor')
    update_req = request.POST.get('update_req')
    print("update",update_req)
    
    if not DomainMaster.objects.filter(id=domain).exists():
            return JsonResponse({"detail": "Invalid domain."})

    if not CompetitorMaster.objects.filter(id=competitor).exists():
            return JsonResponse({"detail": "Invalid competitor."})

    domain_object = DomainMaster.objects.get(id=domain)
    domainName = domain_object.domainname
    cleanedDomainName = domainName.replace(" ","_").replace("(","").replace(")","").replace("-","")
    competitor_object = CompetitorMaster.objects.get(id=competitor)
    print("\n\n\n\n\nDOMAIN NAME##############",domainName)
    print("\n\n\n\n\ncleanedDomainName##############", cleanedDomainName)

    crawler_response = []
    parser_response = []
    response = {}
    crawlerFileName = None
    parserFileName = None
    crawlerConfigFileName = None
    parserConfigFileName = None
    bli_id = dict(request.session)['bli_id']
    for upload_name, uploaded_file in request.FILES.items():
        fs = FileSystemStorage()
        files = upload_name
        if (files.find("+1") != -1):
            crawlerFileName = files.replace("+1", "")
            tag = settings.DOMAINTAGS.get(domainName, cleanedDomainName)
            crawlerFileName = 'Scrapper' + tag + 'Python.py'
            temp_cpath = os.path.join(settings.MEDIA_ROOT, "Crawler_Parser_Files/Crawler/", crawlerFileName)
            uploaded_cfilename = fs.save(temp_cpath, uploaded_file)
            
            try:
                crawler_response = get_crawler_server_details(bli_id, temp_cpath, crawlerFileName)
            except Exception as e:
                print(e.args[0])
                
            finally:
                temp_cfile_remove_path = os.path.join(settings.MEDIA_ROOT, "Crawler_Parser_Files/Crawler/",
                                                      uploaded_cfilename)
                fileopretion(temp_cfile_remove_path)

        if (files.find("+2") != -1):
            parserFileName = files.replace("+2", "")
            tag = settings.DOMAINTAGS.get(domainName, cleanedDomainName)
            parserFileName = 'Parser' + tag + 'Python.py'
            temp_pfilepath = os.path.join(settings.MEDIA_ROOT, "Crawler_Parser_Files/Parser/", parserFileName)
            uploaded_pfilename = fs.save(temp_pfilepath, uploaded_file)
            try:
                parser_response = get_parser_server_details(bli_id, temp_pfilepath, parserFileName)
            except Exception as e:
                print(e.args[0])
            
            finally:
                temp_pfile_remove_path = os.path.join(settings.MEDIA_ROOT, "Crawler_Parser_Files/Parser/",
                                                      uploaded_pfilename)
                fileopretion(temp_pfile_remove_path)
        if (files.find("+3") != -1):
            crawlerConfigFileName = files.replace("+3", "")
            tag = settings.DOMAINTAGS.get(domainName, cleanedDomainName)
            crawlerConfigFileName = 'ScrapperConfig' + tag + 'Python.py'
            temp_cpath = os.path.join(settings.MEDIA_ROOT, "Crawler_Parser_Files/Crawler_config/", crawlerConfigFileName)
            uploaded_cfilename = fs.save(temp_cpath, uploaded_file)
            
            try:
                crawler_response = get_crawler_config_server_details(bli_id, temp_cpath, crawlerConfigFileName)
            except Exception as e:
                print(e.args[0])
                
            finally:
                temp_cfile_remove_path = os.path.join(settings.MEDIA_ROOT, "Crawler_Parser_Files/Crawler_config/",
                                                      uploaded_cfilename)
                fileopretion(temp_cfile_remove_path)

        if (files.find("+4") != -1):
            parserConfigFileName = files.replace("+4", "")
            tag = settings.DOMAINTAGS.get(domainName, cleanedDomainName)
            parserConfigFileName = 'ParserConfig' + tag + 'Python.py'
            temp_cpath = os.path.join(settings.MEDIA_ROOT, "Crawler_Parser_Files/Parser_config/", parserConfigFileName)
            uploaded_cfilename = fs.save(temp_cpath, uploaded_file)
            
            try:
                crawler_response = get_parser_config_server_details(bli_id, temp_cpath, parserConfigFileName)
            except Exception as e:
                print(e.args[0])
                
            finally:
                temp_cfile_remove_path = os.path.join(settings.MEDIA_ROOT, "Crawler_Parser_Files/Parser_config/",
                                                      uploaded_cfilename)
                fileopretion(temp_cfile_remove_path)
    
    if update_req != None and update_req != '':

        if crawlerFileName is not None:
            #cfileName = domain_object.scrapingscriptname
            #crawler_response = get_crawler_server_details(temp_cpath, cfileName)
            domain_object.scrapingscriptname = crawlerFileName
            crawler_response.append({"detail": "Files Updated successfully {0}.\n".format(crawlerFileName), "status": "Success"})

        if crawlerConfigFileName is not None:
            #cfileName = domain_object.scrapingconfigscriptname
            domain_object.scrapingconfigscriptname = crawlerConfigFileName
            crawler_response.append({"detail": "Files Updated successfully {0}.\n".format(crawlerConfigFileName), "status": "Success"})

        if parserFileName is not None:
            domain_object.parsingscriptname = parserFileName
            parser_response.append({"detail": "Files Updated successfully {0}.\n".format(parserFileName), "status": "Success"})

        if parserConfigFileName is not None:
            domain_object.parsingconfigscriptname = parserConfigFileName
            parser_response.append({"detail": "Files Updated successfully {0}.\n".format(parserConfigFileName), "status": "Success"})
    else:
        #competitor_object = CompetitorMaster.objects.filter(id__iexact=competitor).first()
        domain_object.scrapingscriptname = crawlerFileName
        domain_object.parsingscriptname = parserFileName
        domain_object.scrapingconfigscriptname = crawlerConfigFileName
        domain_object.parsingconfigscriptname = parserConfigFileName
        domain_object.created_datetime = timezone.now()

        crawler_response.append({"detail": "Domain updated successfully.", "status": "Success"})

    domain_object.competitorid = competitor_object.id
    print('+++++++++++++++++++++++++++++++++, start datetime', datetime.datetime.now())
    domain_object.save()
    print('+++++++++++++++++++++++++++++++++, end datetime', datetime.datetime.now())
    obj = VisibleDomain(bli_id)
    obj.populateDomain(request)
    response.update({'r1': crawler_response})
    response.update({'r2': parser_response})
    return JsonResponse(response, safe=False)


def get_crawler_server_details(bli_id, local_filepath, c_filename):
    print("SQL Database got connected")
    cur = connection.cursor()
    cur.execute(
        "SELECT CrawlingName,CrawlingPath,CrawlingBackUpPath,UserName,Password FROM eCube_Centralized_DB.ScriptsServerDetails where not CrawlingName='';")
    # print("Crawler Records fetched")
    list_server_response = []
    for row in cur.fetchall():
        c_server_name = row[0]
        c_server_path = row[1]
        c_server_bkp_path = row[2]
        c_username = row[3]
        c_password = row[4]
        try:
            crawler_sftp = sftpOpration(c_server_name, c_username, c_password)

        except Exception as e:
            mesg = c_server_name + "-" + e.args[0]
            error1 = {"error": "Crawler servers, " + mesg, "Success": "Failed"}
            list_server_response.append(error1)
            break


        c_file = c_server_path + settings.BLI_SCRIPT_DIR[bli_id] + c_filename
        # print(c_file)
        c_bkp_file = c_server_bkp_path + settings.BLI_SCRIPT_DIR[bli_id] + c_filename

        try:

                # print("remote crawler file exist")
                remote_renamed_cfile_bkppath = os.path.splitext(c_bkp_file)[0] + "_" + datetime.datetime.now().strftime(
                    "%Y-%m-%d_%H:%M") + os.path.splitext(c_bkp_file)[1]
                if crawler_sftp.stat(c_file):
                    crawler_sftp.rename(c_file, remote_renamed_cfile_bkppath)
                
                # print("remote file renamed")
                crawler_sftp.put(local_filepath, c_file)
                # print("renamed and crawler file sent")
                list_server_response.append(
                    {"detail": "Crawler file sent on " + str(c_server_name) + " server successfully.\n",
                     "status": "Success"})
        except IOError:
            crawler_sftp.put(local_filepath, c_file)
            # print("new crawler file sent")
            list_server_response.append(
                {"detail": "Crawler file sent on " + str(c_server_name) + " server successfully.\n",
                 "status": "Success"})

        crawler_sftp.close()
        remove_pyc_files(c_server_name, c_username, c_password, 'AetosQueue/Crawling')

    return list_server_response


def get_crawler_server_details_download(bli_id, local_filepath, c_filename, demo_file_name, row_num, file_type):
    # print("SQL Database got connected")
    cur = connection.cursor()

    if file_type == 'crawl':
        query = "SELECT CrawlingName,CrawlingPath,CrawlingConfigPath,ParsingPath,ParsingConfigPath,UserName,Password FROM eCube_Centralized_DB.ScriptsServerDetails where CrawlingName='{}' LIMIT 1;".format(settings.SCRIPT_DOWNLOAD_SERVER)
    else:
        query = "SELECT ParsingName,CrawlingPath,CrawlingConfigPath,ParsingPath,ParsingConfigPath,UserName,Password FROM eCube_Centralized_DB.ScriptsServerDetails where ParsingName='{}' LIMIT 1;".format(settings.SCRIPT_DOWNLOAD_SERVER)

    cur.execute(query)
    # print("Crawler Records fetched")

    results = cur.fetchall()
    c_server_name = results[0][0]
    c_server_path = results[0][row_num]

    c_username = results[0][5]
    c_password = results[0][6]
    crawler_sftp = sftpOpration(c_server_name, c_username, c_password)

    c_file = c_server_path + settings.BLI_SCRIPT_DIR[bli_id] + c_filename
    local_filepath = local_filepath + demo_file_name
    # print('c_file = ', c_file)
    # print(local_filepath)
    # print('script download server.....', c_server_name)

    try:
        crawler_sftp.get(c_file, local_filepath)
        crawler_sftp.close()
    except Exception as e:
        crawler_sftp.close()

    cur.close()
    connection.close()


def get_crawler_config_server_details(bli_id, local_filepath, c_filename):
    # print("SQL Database got connected")
    cur = connection.cursor()
    cur.execute(
        "SELECT CrawlingName,CrawlingConfigPath,CrawlingConfigBackUpPath,UserName,Password FROM eCube_Centralized_DB.ScriptsServerDetails where not CrawlingName='';")
    # print("Crawler Records fetched")
    list_server_response = []
    for row in cur.fetchall():
        c_server_name = row[0]
        c_server_path = row[1]
        c_server_bkp_path = row[2]
        c_username = row[3]
        c_password = row[4]
        try:
            crawler_sftp = sftpOpration(c_server_name, c_username, c_password)

        except Exception as e:
            mesg = c_server_name + "-" + e.args[0]
            error1 = {"error": "Crawler servers, " + mesg, "Success": "Failed"}
            list_server_response.append(error1)
            break

        c_file = c_server_path + settings.BLI_SCRIPT_DIR[bli_id] + c_filename
        c_bkp_file = c_server_bkp_path + settings.BLI_SCRIPT_DIR[bli_id] + c_filename

        try:

                # print("remote crawler config  file exist")
                remote_renamed_cfile_bkppath = os.path.splitext(c_bkp_file)[0] + "_" + datetime.datetime.now().strftime(
                    "%Y-%m-%d_%H:%M") + os.path.splitext(c_bkp_file)[1]
                if crawler_sftp.stat(c_file):
                    crawler_sftp.rename(c_file, remote_renamed_cfile_bkppath)
                # print("remote file renamed")
                crawler_sftp.put(local_filepath, c_file)
                # print("renamed and crawler file sent")
                list_server_response.append(
                    {"detail": "Crawler   config file sent on " + str(c_server_name) + " server successfully.",
                     "status": "Success"})
        except IOError:
            crawler_sftp.put(local_filepath, c_file)
            # print("new crawler file sent")
            list_server_response.append(
                {"detail": "Crawler file sent on " + str(c_server_name) + " server successfully.",
                 "status": "Success"})

        crawler_sftp.close()
        remove_pyc_files(c_server_name, c_username, c_password, 'AetosQueue/Crawling')

    cur.close()
    return list_server_response




def get_parser_config_server_details(bli_id, local_filepath, c_filename):
    # print("SQL Database got connected")
    cur = connection.cursor()
    cur.execute(
        "SELECT ParsingName,ParsingConfigPath,ParsingConfigBackUpPath,UserName,Password FROM eCube_Centralized_DB.ScriptsServerDetails where not ParsingName='';")
    # print("Crawler Records fetched")
    list_server_response = []
    for row in cur.fetchall():
        c_server_name = row[0]
        c_server_path = row[1]
        c_server_bkp_path = row[2]
        c_username = row[3]
        c_password = row[4]
        try:
            parser_sftp = sftpOpration(c_server_name, c_username, c_password)

        except Exception as e:
            mesg = c_server_name + "-" + e.args[0]
            error1 = {"error": "Crawler servers, " + mesg, "Success": "Failed"}
            list_server_response.append(error1)
            break

        c_file = c_server_path + settings.BLI_SCRIPT_DIR[bli_id] + c_filename
        c_bkp_file = c_server_bkp_path + settings.BLI_SCRIPT_DIR[bli_id] + c_filename
        try:

                # print("remote parser config  file exist")
                remote_renamed_cfile_bkppath = os.path.splitext(c_bkp_file)[0] + "_" + datetime.datetime.now().strftime(
                    "%Y-%m-%d_%H:%M") + os.path.splitext(c_bkp_file)[1]
                if parser_sftp.stat(c_file):
                    parser_sftp.rename(c_file, remote_renamed_cfile_bkppath)
                # print("remote file renamed")
                parser_sftp.put(local_filepath, c_file)
                # print("renamed and parser file sent")
                list_server_response.append(
                    {"detail": "Parser   config file sent on " + str(c_server_name) + " server successfully.",
                     "status": "Success"})
        except IOError:
            parser_sftp.put(local_filepath, c_file)
            # print("new crawler file sent")
            list_server_response.append(
                {"detail": "Parser file sent on " + str(c_server_name) + " server successfully.",
                 "status": "Success"})

        parser_sftp.close()
        remove_pyc_files(c_server_name, c_username, c_password, 'AetosQueue/Parsing')

    cur.close()
    return list_server_response


def get_parser_server_details(bli_id, local_filepath, p_filename):
    # print("SQL Database got connected")
    cur1 = connection.cursor()
    cur1.execute(
        "SELECT ParsingName,ParsingPath,ParserBackUpPath,UserName,Password FROM eCube_Centralized_DB.ScriptsServerDetails where not ParsingName='';")
    from pdb import set_trace as st
    # print("Parser Records fetched")
    list_pserver_response = []
    for row in cur1.fetchall():
        p_server_name = row[0]
        p_server_path = row[1]
        p_server_bkp_path = row[2]
        p_username = row[3]
        p_password = row[4]
        try:
            parser_sftp = sftpOpration(p_server_name, p_username, p_password)
        except Exception as e:
            mesg = p_server_name + "-" + e.args[0]
            error2 = {"error": "Crawler servers, " + mesg, "Success": "Failed"}
            list_pserver_response.append(error2)
            break

        p_file = p_server_path + settings.BLI_SCRIPT_DIR[bli_id] + p_filename
        p_bkp_file = p_server_bkp_path + settings.BLI_SCRIPT_DIR[bli_id] + p_filename
        try:
                # print("remote parser file exist")
                remote_renamed_pfile_bkppath = os.path.splitext(p_bkp_file)[0] + "_" + datetime.datetime.now().strftime(
                    "%Y-%m-%d_%H:%M") + os.path.splitext(p_bkp_file)[1]
                if parser_sftp.stat(p_file):
                    parser_sftp.rename(p_file, remote_renamed_pfile_bkppath)
                # print("remote file renamed")
                parser_sftp.put(local_filepath, p_file)
                # print("renamed and parser file sent")
                list_pserver_response.append(
                    {"detail": "Parser file sent on " + str(p_server_name) + " server successfully.",
                     "status": "Success"})
        except IOError:
            parser_sftp.put(local_filepath, p_file)
            # print("new parser file sent")
            list_pserver_response.append(
                {"detail": "Parser file sent on " + str(p_server_name) + " server successfully.",
                 "status": "Success"})

        parser_sftp.close()
        remove_pyc_files(p_server_name, p_username, p_password, 'AetosQueue/Parsing')

    cur1.close()
    return list_pserver_response


def sftpOpration(host, username, password):
    port = 22
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp_client = paramiko.SFTPClient.from_transport(transport)
    return sftp_client


def fileopretion(temp_filepath_name):
    if os.path.isfile(temp_filepath_name):
        os.remove(temp_filepath_name)
        # print("file removed succefully!!!")


def remove_pyc_files(host,username,password,file_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(host, username=username, password=password)
    client.exec_command("find {0} -name '*.pyc' -type f -delete".format(file_path))
    client.close()
    # print("All pyc files deleted inside {0} on server {1}".format(file_path,host))




# Create your views here.
