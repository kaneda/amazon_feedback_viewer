from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from josh.amazon_unraveler import getPages
import re

class Amazon(TemplateView):
    p = re.compile("(http(s?)://(([a-zA-Z0-9]*)\.)?([a-zA-Z0-9]*)\.(([a-zA-Z0-9]{2,3})\.)?([a-zA-Z0-9]{2,3})([^\s\),$\n'\";])*)")

    def get(self,request):
        response_dict = {}
        base = "amazon.html"
        err = ""
        context = RequestContext(request,response_dict)
        return render_to_response(base, context_instance=context)

    def post(self,request):
        response_dict = {}
        base = "amazon_results.html"
        err = ""
        u = ""
        retEarly = False
        if('url' in request.POST):
                r = re.search(self.p,request.POST['url'])
                if(r): u = r.group(0)
                else:
                        err = "Invalid url, stop that"
                        retEarly = True
        else:
                err = "No url given"
                retEarly = True

        if(retEarly):
                response_dict['error'] = err
                response_dict['hasErr'] = True
                context = RequestContext(request, response_dict)
                return render_to_response(base, context_instance=context)

        usMode = True
        response_dict['mode'] = 'us'
        if('mode' in request.POST):
                if(request.POST['mode'] == "ca"):
                        usMode = False
                        response_dict['mode'] = 'ca'
        else:
                response_dict['error'] = "Stop that"
                response_dict['hasErr'] = True
                context = RequestContext(request, response_dict)
                return render_to_response(base, context_instance=context)

        n = 0
        if('pages' in request.POST):
                try: n = abs(int(request.POST['pages']))
                except Exception:
                        err = "Invalid number of pages, stop that"
                        retEarly = True
        else:
                err = "No number of pages given"
                retEarly = True

        if(retEarly):
                response_dict['error'] = err
                response_dict['hasErr'] = True
                context = RequestContext(request, response_dict)
                return render_to_response(base, context_instance=context)

        r = 10
        if('rate' in request.POST):
                try: r = abs(int(request.POST['rate']))
                except Exception:
                        pass

        (pages,pages_len) = getPages(u,usMode,n,r)
        response_dict['comments'] = pages
        response_dict['num_entries'] = pages_len
        context = RequestContext(request, response_dict)
        return render_to_response(base, context_instance=context)

