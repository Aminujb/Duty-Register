import sys
from datetime import datetime
from bootstrap_datepicker_plus import DatePickerInput
import xlrd
from django.forms import Form, forms, ModelForm
from register.models import Employee, Rank, Tcomm, State, Unit, Speciality, UnitType, Country, Pass


class PassForm(ModelForm):
    class Meta:
        model = Pass
        fields = '__all__'
        widgets = {
            'start': DatePickerInput(),
            'end': DatePickerInput(),
        }


def can_create(data):
    return True if not data.strip() == '' else False


def extract_data(rows, datemode):
    import_cols = [
        "RANK", "INITIAL", "NAME", "P/NUMBER", "SPECIALITY", "APPT/DEPT", "DATE TOS", "SENIORITY", "STATE",
        "T/COMM", "PHONE NO", "REMARKS"
    ]

    headers = [col.upper() for col in rows[0]]

    # check that the headings are good.
    unknown = set(headers).difference(import_cols)
    if unknown:
        raise Exception('unknown headers')

    # get the indices for each header
    rank_idx, initial_idx, name_idx, p_num_idx, speciality_idx, dept_idx, date_tos_idx, seniority_idx, state_idx, \
    t_comm_idx, phone_idx, remarks_index = [
        headers.index(name) for name in import_cols
    ]

    # everything great, continue
    country, created = Country.objects.get_or_create(name='Nigeria')
    # country.save()

    u_type, created = UnitType.objects.get_or_create(name='General')

    result = []

    for row_data in rows[1:]:
        if can_create(row_data[rank_idx]):
            rank, created = Rank.objects.get_or_create(name=row_data[rank_idx].strip())
        else:
            rank = None
        if can_create(row_data[t_comm_idx]):
            t_comm, created = Tcomm.objects.get_or_create(name=row_data[t_comm_idx].strip())
        else:
            t_comm = None
        if can_create(row_data[dept_idx]):
            dept, created = Unit.objects.get_or_create(name=row_data[dept_idx].strip(), type=u_type)
        else:
            dept = None
        if can_create(row_data[state_idx]):
            state, created = State.objects.get_or_create(country=country, name=row_data[state_idx].strip())
        else:
            state = None
        if can_create(row_data[speciality_idx]):
            speciality, created = Speciality.objects.get_or_create(name=row_data[speciality_idx].strip())
        else:
            speciality = None

        try:
            date_tos = row_data[date_tos_idx]
            date_tos = datetime(*xlrd.xldate_as_tuple(date_tos, datemode))
        except Exception:
            date_tos = None

        try:
            seniority = row_data[seniority_idx]
            seniority = datetime(*xlrd.xldate_as_tuple(seniority, datemode))
        except Exception:
            seniority = None

        result.append(
            {
                'rank': rank,
                'initials': row_data[initial_idx].strip(),
                'last_name': row_data[name_idx].strip(),
                'p_number': row_data[p_num_idx].strip(),
                'speciality': speciality,
                'dept': dept,
                'date_tos': date_tos,
                'seniority': seniority,
                'state': state,
                't_comm': t_comm,
                'phone': row_data[phone_idx].strip(),
                'remarks': row_data[remarks_index].strip(),
            })

    return result


class UploadRecords(Form):
    employees_data = forms.FileField()

    def clean_employees_data(self):
        wb = xlrd.open_workbook(file_contents=self.cleaned_data['employees_data'].read())
        ws = wb.sheet_by_index(0)
        if ws.nrows == 0:
            raise Exception('Unable to process empty sheet')
        rows = []
        for row_idx in range(ws.nrows):
            row = []
            for col_idx in range(ws.ncols):
                cell = ws.cell(row_idx, col_idx)
                cell_value = cell.value
                if cell.ctype == 2:  # float. convert to str
                    cell_value = str(int(cell.value))
                row.append(cell_value)
            rows.append(row)
        try:
            data = extract_data(rows, wb.datemode)
        except Exception:
            raise forms.ValidationError('o fail ma ni')
        return data

    def save(self):
        data = self.cleaned_data['employees_data']

        for d in data:
            Employee.objects.update_or_create(
                p_number=d['p_number'],
                defaults={
                    "initials": d['initials'],
                    "last_name": d['last_name'],
                    "speciality": d['speciality'],
                    "t_comm": d['t_comm'],
                    "rank": d['rank'],
                    "unit": d['dept'],
                    "state_of_origin": d['state'],
                    "phone": d['phone'],
                    "date_tos": d['date_tos'],
                    "seniority": d['seniority'],
                    "remarks": d['remarks']
                }
            )

        return


def extract_pass_data(rows, datemode):
    import_cols = [
        "P/NUMBER", "DESCRIPTION", "START DATE", "END DATE", "REMARKS"
    ]

    headers = [col.upper() for col in rows[0]]

    # check that the headings are good.
    unknown = set(headers).difference(import_cols)
    if unknown:
        raise Exception('unknown headers')

    # get the indices for each header
    p_num_idx, description_idx, start_date_idx, end_date_idx, remarks_index = [
        headers.index(name) for name in import_cols
    ]


    result = []

    for row_data in rows[1:]:

        try:
            start_date = datetime(*xlrd.xldate_as_tuple(row_data[start_date_idx], datemode))
        except Exception:
            start_date = None

        try:
            end_date = datetime(*xlrd.xldate_as_tuple(row_data[end_date_idx], datemode))
        except Exception:
            end_date = None

        if start_date > end_date:
            raise Exception('Start Date and End Date for %s is invalid', row_data[p_num_idx].strip())
        result.append(
            {
                'p_number': row_data[p_num_idx].strip(),
                'description': row_data[description_idx].strip(),
                'start_date': start_date,
                'end_date': end_date,
                'remarks': row_data[remarks_index].strip(),
            })

    return result


class UploadPassRecords(Form):
    pass_data = forms.FileField()

    def clean_pass_data(self):
        wb = xlrd.open_workbook(file_contents=self.cleaned_data['pass_data'].read())
        ws = wb.sheet_by_index(0)
        if ws.nrows == 0:
            raise Exception('Unable to process empty sheet')
        rows = []
        for row_idx in range(ws.nrows):
            row = []
            for col_idx in range(ws.ncols):
                cell = ws.cell(row_idx, col_idx)
                cell_value = cell.value
                if cell.ctype == 2:  # float. convert to str
                    cell_value = str(int(cell.value))
                row.append(cell_value)
            rows.append(row)
        try:
            data = extract_pass_data(rows, wb.datemode)
        except Exception:
            raise forms.ValidationError('o fail ma ni')
        return data

    def save(self):
        data = self.cleaned_data['pass_data']
        for d in data:
            emp = Employee.objects.get(p_number=d['p_number'])
            Pass.objects.create(employee=emp,
                                description=d['description'],
                                start=d['start_date'],
                                end=d['end_date'],
                                remarks=d['remarks'])

        return
