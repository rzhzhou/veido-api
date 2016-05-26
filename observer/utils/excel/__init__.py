from django.http import HttpResponse


def xls_to_response(wb=None, fname=None, format=None, source=None):
    if source is None:
        response = HttpResponse(content_type="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=%s' % fname
        wb.save(response)
    else:
        response = HttpResponse(source.read(
        ), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response[
            'Content-Disposition'] = "attachment; filename=%s.%s" % (fname, format)
    return response
