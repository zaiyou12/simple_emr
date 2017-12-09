# !/usr/bin/python3
import tkinter as tk
from functools import partial


patient_list = []
chart_list = []


class Patient:
    """ Basic information of patient """

    def __init__(self, num):
        self.num = num
        self.name, self.age, self.gender, self.address = '', '', '', ''
        self.charts = []

    def set_data(self, name, age, gender, address):
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address

    def set_charts(self, charts):
        self.charts = charts

    def get_data_by_num(self, num):
        if num == 0:
            return self.name
        elif num == 1:
            return self.age
        elif num == 2:
            return self.gender
        elif num == 3:
            return self.address


class Chart:
    """ Simple chart that record the patient's diagnostic history """
    count = 0

    def __init__(self):
        Chart.count += 1
        self.num = Chart.count
        self.date, self.symptom, self.evaluation, self.diagnosis, self.treatment = '', '', '', '', ''
    
    def set_data(self, date, symptom, evaluation, diagnosis, treatment):
        self.date = date
        self.symptom = symptom
        self.evaluation = evaluation
        self.diagnosis = diagnosis
        self.treatment = treatment

    def get_date(self):
        if self.date == '':
            return '의무 기록 #' + str(self.num)
        return self.date

    def get_data_by_num(self, num):
        if num == 0:
            return self.date
        elif num == 1:
            return self.symptom
        elif num == 2:
            return self.evaluation
        elif num == 3:
            return self.diagnosis
        elif num == 4:
            return self.treatment


class MainWindow(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.create_buttons(rows=2, columns=5)
    
    def create_buttons(self, rows, columns):
        """ Create 10 buttons """

        num = 0
        for r in range(rows):
            for c in range(columns):
                num = num + 1
                new_window = SubWindow(num)
                func = partial(new_window.create_window, main_window=self, num=num)
                button = tk.Button(self, text='환자'+str(num), command=func)
                button.grid(row=r+1, column=c+1, padx=10, pady=20)


class SubWindow:
    patient_info_labels = ['환자 이름', '환자 나이', '환자 성별', '환자 주소']
    medical_record_labels = ['내원일', '호소 증상', '환자 평가', '진단', '치료 및 계획']
    
    def __init__(self, num):
        self.patient_num = num - 1
        self.info_entries, self.record_entries = [], []
        self.current_chart_num = 0

    def create_window(self, main_window, num):
        """ Build windows in three sections """

        print('환자 #', num, '이 클릭되었습니다.')

        window = tk.Toplevel(main_window)
        window.wm_title('환자 #%s 정보' % str(num))

        # set Label at the top
        tk.Label(window, text='환자 정보', bg="light cyan").grid(row=0, columnspan=4, sticky=tk.W+tk.E)
        tk.Label(window, text='내원일', bg="light cyan").grid(row=0, column=4, sticky=tk.W+tk.E)
        tk.Label(window, text='환자 의무 기록', bg="light cyan").grid(row=0, column=5, columnspan=2, sticky=tk.W+tk.E)

        # set patient information section on left
        self.info_entries = []
        for index, value in enumerate(self.patient_info_labels):
            tk.Label(window, text=value).grid(row=index+1, column=0)
            if index < 4:
                entry = tk.Entry(window, width=10)
            else:
                entry = tk.Entry(window, width=30)
            entry.grid(row=index+1, column=1)
            entry.insert(0, patient_list[self.patient_num].get_data_by_num(index))
            self.info_entries.append(entry)

        # set date button section on center
        for index in range(10):
            func = partial(self.get_record_by_chart_num, button_num=index)
            date_button = tk.Button(window, text=chart_list[self.patient_num * 10+index].get_date(),
                                    command=func)
            date_button.grid(row=index+1, column=4)

        # set medical record section on right
        self.record_entries = []
        for index, value in enumerate(self.medical_record_labels):
            tk.Label(window, text=value).grid(row=index+1, column=5)
            if index > 1:
                entry = tk.Entry(window, width=50)
            else:
                entry = tk.Entry(window, width=10)
            entry.grid(row=index+1, column=6)
            entry.insert(0, chart_list[self.patient_num*10].get_data_by_num(index))
            self.record_entries.append(entry)

        # set save buttons
        save_info_button = tk.Button(window, text='환자 정보 저장', command=self.save_patient_info)
        save_info_button.grid(row=11, column=1, pady=20)
        save_record_button = tk.Button(window, text='의무 기록 저장', command=self.save_medical_record)
        save_record_button.grid(row=11, column=6, pady=20)

        # initialize current chart num
        self.current_chart_num = 0

    def save_patient_info(self):
        print('환자 #', self.patient_num+1, '의 정보가 저장되었습니다.')
        patient = patient_list[self.patient_num]
        e = self.info_entries
        patient.set_data(e[0].get() or '', e[1].get() or '', e[2].get() or '', e[3].get() or '')

    def save_medical_record(self):
        print('의무 기록 #',  self.get_patient_chart_num()+1, '이 저장되었습니다.')
        chart = chart_list[self.get_patient_chart_num()]
        r = self.record_entries
        chart.set_data(r[0].get() or '', r[1].get() or '', r[2].get() or '', r[3].get() or '', r[4].get() or '')

    def get_patient_chart_num(self):
        return self.patient_num * 10 + self.current_chart_num

    def get_record_by_chart_num(self, button_num):
        self.current_chart_num = button_num
        print('의무 기록 #', self.get_patient_chart_num()+1, '이 클릭 되었습니다.')
        chart = chart_list[self.get_patient_chart_num()]
        for index, entry in enumerate(self.record_entries):
            entry.delete(0, 'end')
            entry.insert(0, chart.get_data_by_num(index))


def set_up_models():
    """ Create 10 patient objects and assign 10 charts to each patient """
    for index in range(10):
        patient = Patient(index)
        chart_to_add = []
        for _ in range(10):
            chart = Chart()
            chart_to_add.append(chart)
        patient.set_charts(chart_to_add)
        patient_list.append(patient)
        chart_list.extend(chart_to_add)


if __name__ == "__main__":
    set_up_models()
    root = tk.Tk()
    root.title("3rd-EMR")
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
