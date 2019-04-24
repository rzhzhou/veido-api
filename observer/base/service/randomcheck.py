import random
import openpyxl
from io import BytesIO
from observer.base.service.abstract import Abstract
from observer.base.models import RandomCheckTask, RandomCheckEnterpriseList


class RandomCheckTaskData(Abstract):

    def __init__(self, params):
        super(RandomCheckTaskData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'name', 'perform_number', 'delegate', 'check_agency', 'enterprise_number')

        cond = {
            'name': getattr(self, 'name', None),
            'perform_number': getattr(self, 'perform_number', None),
            'delegate': getattr(self, 'delegate', None),
            'check_agency': getattr(self, 'check_agency', None),
            'enterprise_number': getattr(self, 'enterprise_number', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)
        queryset = RandomCheckTask.objects.filter(**args).values(*fields)

        # print('----', [random.randint(0,100) for _ in range(10)])

        return queryset


class RandomCheckEnterprise(Abstract):

    def __init__(self, params):
        super(RandomCheckEnterprise, self).__init__(params)

    def get_by_id(self, tid):
        fields = ('id', 'product_name', 'enterprise_name', 'enterprise_address', 'contacts', 'phone', 'area', 'status', )

        cond = {
            'product_name': getattr(self, 'product_name', None),
            'enterprise_name': getattr(self, 'enterprise_name', None),
            'enterprise_address': getattr(self, 'enterprise_address', None),
            'contacts': getattr(self, 'contacts', None),
            'phone': getattr(self, 'phone', None),
            'area': getattr(self, 'area', None),
            'status': getattr(self, 'status', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)
        queryset = RandomCheckEnterpriseList.objects.filter(**args, task_id=tid).values(*fields)

        return queryset


class RandomCheckTaskUpload(Abstract):

    def __init__(self, params):
        super(RandomCheckTaskUpload, self).__init__(params)

    def upload(self, filename, enterprise_number, file_obj):
        # ModelWeight
        model = {'序号': 0, '产品名称': 0, '生产企业名称': 0, '生产企业地址': 0, '联系人': 0, '联系电话': 0,
                 '所属区': 0}

        # sheet values
        def sv(x, y, z): return z.cell(row=x, column=y).value

        try:
            xlsx_book = openpyxl.load_workbook(
                BytesIO(file_obj.read()), read_only=True)
            sheet = xlsx_book.active
            rows = sheet.rows
        except Exception as e:
            return {
                'status': 0,
                'message': '操作失败！请检查文件是否有误。详细错误信息：%s！' % e
            }

        total = 0
        dupli = 0
        data_list = []
        task_name = sheet['A1'].value.strip()
        perform_number = sheet['A2'].value.strip()
        delegate = sheet['A3'].value.strip()
        check_agency = sheet['A4'].value.strip()

        try:
            random_task = RandomCheckTask(
                name=task_name,
                perform_number=perform_number,
                delegate=delegate,
                check_agency=check_agency,
                enterprise_number=enterprise_number,
            )
            random_task.save()
        except Exception as e:
            return {
                'status': 0,
                'message': '操作失败！请检查文件是否有误。详细错误信息：%s！' % e
            }

        for i, row in enumerate(rows):
            i += 1
            if i < 5:
                pass
            elif i == 5:
                line = [cell.value for cell in row]
                for k in model.keys():
                    model[k] = line.index(k) + 1
            else:
                number = sv(i, model['序号'], sheet)

                product_name = sv(i, model['产品名称'], sheet)
                if not product_name:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行"产品名称"有误！' % (i + 1, )
                    }

                enterprise_name = sv(i, model['生产企业名称'], sheet)
                if not enterprise_name:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行"生产企业名称"有误！' % (i + 1, )
                    }

                enterprise_address = sv(i, model['生产企业地址'], sheet)
                if not enterprise_address:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行"生产企业地址"有误！' % (i + 1, )
                    }

                contacts = sv(i, model['联系人'], sheet)
                if not contacts:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行"联系人"有误！' % (i + 1, )
                    }

                phone = sv(i, model['联系电话'], sheet)
                if not phone:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行"联系电话"有误！' % (i + 1, )
                    }

                area = sv(i, model['所属区'], sheet)
                if not area:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行"所属区"有误！' % (i + 1, )
                    }

                total += 1

                bulk_enterprise = RandomCheckEnterpriseList(
                    product_name=product_name,
                    enterprise_name=enterprise_name,
                    enterprise_address=enterprise_address,
                    contacts=contacts,
                    phone=phone,
                    area=area,
                    task_id=random_task.id,
                    status=0,
                )
                data_list.append(bulk_enterprise)

        RandomCheckEnterpriseList.objects.bulk_create(data_list)

        queryset = RandomCheckEnterpriseList.objects.filter(task_id=random_task.id)
        enterprise_first_id = queryset.values_list('id', flat=True).order_by('id')[0]
        enterprise_last_id = queryset.count() + enterprise_first_id - 1

        selected_ids = [random.randint(enterprise_first_id, enterprise_last_id) for _ in range(enterprise_number)]
        print(selected_ids)

        RandomCheckEnterpriseList.objects.filter(id__in=selected_ids).update(status=1)

        return {
            'status': 1,
            'message': '操作成功！成功导入%s条数据！' % (total)
        }
