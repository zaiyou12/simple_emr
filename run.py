# !/usr/bin/python3
import tkinter as tk
from functools import partial

# 구현 요구사항이 간단하므로 DB를 사용하지 않고 리스트로 데이터를 저장 및 관리
patient_list = []
chart_list = []


# 환자의 class, 환자의 기본적인 정보인 이름, 나이, 성별, 주소를 저장 및 관리
class Patient:
    """ Basic information of patient """
    count = 0 # 클래스 변수, 환자들간 변수를 공유하여 환자 번호가 중복되는 일을 방지함. 또한 추후 환자수의 변화에 따른 확장 가능성을 대비하여, 쉽게 총 환자수를 확인하고 관리할수 있음.

    def __init__(self): # 환자 객체 생성시 번호만 입력하고, 그외 정보들은 초기화만 진행함.
        Patient.count += 1
        self.num = Patient.count
        self.name, self.age, self.gender, self.address = '', '', '', ''
        self.charts = []

    def set_data(self, name, age, gender, address): # 환자 객체에 데이터를 입력
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address

    def set_charts(self, charts): # 차트 객체를 리스트 형태로 받아 환자 객체에 입력함. 현재는 차트 객체의 갯수가 적어 전체 차트 리스트를 통해 차트 객체에 접근 하지만,
        self.charts = charts      # 환자 객체로도 차트에 접근할 수 있어, 추후 차트 데이터가 많이 늘었을때 전체 차트 리스트 없이도 차트 객체에 접근 할 수 있음.

    def get_data_by_num(self, num): # for 구문으로 쉽게 데이터를 입력할 수 있게, num을 구분자로 하여 데이터를 입력할 수 있게 함.
        if num == 0:                # 꼭 필요한 함수는 아니지만, 아래 코드의 간결하게 관리할 수 있게 도와줌.
            return self.name
        elif num == 1:
            return self.age
        elif num == 2:
            return self.gender
        elif num == 3:
            return self.address


# 진단 결과의 class, 진단 결과인 내원일, 호소증상, 환자평가, 진단, 치료 및 계획을 저장 및 관리
class Chart:
    """ Simple chart that record the patient's diagnostic history """
    count = 0 # 클래스 변수, 환자 객체에 count 클래스 변수를 생성한 것과 동일한 이유.

    def __init__(self): # 차트 객체 생성시 번호만 입력하고, 그외 정보들은 초기화만 진행함.
        Chart.count += 1
        self.num = Chart.count
        self.date, self.symptom, self.evaluation, self.diagnosis, self.treatment = '', '', '', '', ''
    
    def set_data(self, date, symptom, evaluation, diagnosis, treatment): # 차트 객체에 데이터를 입력
        self.date = date
        self.symptom = symptom
        self.evaluation = evaluation
        self.diagnosis = diagnosis
        self.treatment = treatment

    def get_date(self): # 내원일 버튼들을 생성시, 버튼 text로 호출. 내원일의 기록이 없을시, 내원일이 아닌 차트의 번호를 출력하여 각 버튼들을 구분함.
        if self.date == '':
            return '의무 기록 #' + str(self.num)
        return self.date

    def get_data_by_num(self, num): # for 구문으로 쉽게 데이터를 입력할 수 있게, num을 구분자로 하여 데이터를 입력할 수 있게 함.
        if num == 0:                # 환자 객체의 get_data_by_num 함수와 같이 꼭 필요한 함수는 아니지만, 아래 코드의 간결하게 관리할 수 있게 도와줌.
            return self.date
        elif num == 1:
            return self.symptom
        elif num == 2:
            return self.evaluation
        elif num == 3:
            return self.diagnosis
        elif num == 4:
            return self.treatment


# 환자 정보에 접근할수 있는 프로젝트의 메인 화면 class
# 기존의 환자 버튼과 환자 데이터가 같이 있는 화면을 환자와 데이터로 각각 구분하여, 동시에 여러 환자의 정보를 볼 수 있게 함.
class MainWindow(tk.Frame):
    """ Main screen with access to patients data """
    def __init__(self, *args, **kwargs): # 메인 화면 생성시 GUI 생성
        tk.Frame.__init__(self, *args, **kwargs)
        self.create_buttons(rows=2, columns=5) # 환자 버튼을 5개씩 2줄로 생성
    
    def create_buttons(self, rows, columns): # 환자의 버튼을 생성하여 새로운 화면으로 연결
        """ Create 10 buttons """
        num = 0
        for r in range(rows):
            for c in range(columns):
                num = num + 1
                new_window = SubWindow(num)
                # 환자 정보에 접근하는 버튼에 lambda 대신 partial로 함수를 만들어 전달
                # lambda와 partial은 비슷하지만 lambda는 버튼이 클릭되어야 비로서 코드가 생성되기 떄문에, 모든 함수의 변수인 num에 loop의 마지막 값이 들어가는 문제가 발생
                # 반면 partial에 의한 함수는 생성될때 값이 입력되므로, loop가 돌아가면서 값을 입력.
                # 따라서 lambda로 하게 되면 모든 함수의 num 값에 10이 들어가지만, partial로 하게되면 의도한대로 1~10값이 num 값에 입력됨.
                func = partial(new_window.create_window, main_window=self, num=num)
                button = tk.Button(self, text='환자'+str(num), command=func)
                button.grid(row=r+1, column=c+1, padx=10, pady=20) # 중요한 내용은 아니지만 버튼간의 간격을 늘려 실수로 다른 환자를 클릭하는 것을 방지


# 환자 정보를 입력하고 볼수 있는 서브 화면 class
class SubWindow:
    """ Secondary screen for entering and viewing patient data """
    patient_info_labels = ['환자 이름', '환자 나이', '환자 성별', '환자 주소']           # GUI 생성시 라벨을 for구문으로 깔끔하게 생성하기 위하여, 라벨 내용을 리스트로 관리
    medical_record_labels = ['내원일', '호소 증상', '환자 평가', '진단', '치료 및 계획']  # 추후 라벨 내용이 변경되거나 수가 늘었을때도, 내용을 입력하는 entry도 같이 변경되기에 우지보수에 용이
    
    def __init__(self, num): # 서브 화면 객체 생성시 환자의 번호만 입력하고, 그외의 값들은 초기화만 진행
        self.patient_num = num - 1
        self.info_entries, self.record_entries = [], []
        self.current_chart_num = 0

    def create_window(self, main_window, num): # GUI 생성
        """ Build windows in three sections """
        print('환자 #', num, '이 클릭되었습니다.')

        window = tk.Toplevel(main_window) # 서브 화면을 메인 화면과 연결
        # 기존에는 환자 번호를 라벨로 보여주었으나, 서브 화면 상단 타이틀로 환자 번호로 표기
        # 또한 유저가 실수로 환자 번호를 변경하여, 클릭한 환자 정보와 나타나는 환자 정보가 다른 오류 발생을 방지
        window.wm_title('환자 #%s 정보' % str(num))

        # set Label at the top
        tk.Label(window, text='환자 정보', bg="light cyan").grid(row=0, columnspan=4, sticky=tk.W+tk.E)
        tk.Label(window, text='내원일', bg="light cyan").grid(row=0, column=4, sticky=tk.W+tk.E)
        tk.Label(window, text='환자 의무 기록', bg="light cyan").grid(row=0, column=5, columnspan=2, sticky=tk.W+tk.E)

        # set patient information section on left
        self.info_entries = [] # entry 리스트는 창을 닫았다가 새로 여는 상황을 대비하여 꼭 초기화 하여함
        # GUI 생성시 필요한 라벨 정보들을 list로 관리하기에, for구문으로 편하게 라벨 생성
        # for구문에서 enumerate를 사용하기에 별도로 loop 횟수를 기록하는 변수를 생성할 필요가 없음. python스러운 방법.
        for index, value in enumerate(self.patient_info_labels): 
            tk.Label(window, text=value).grid(row=index+1, column=0)
            if index < 4:
                entry = tk.Entry(window, width=10)
            else:
                entry = tk.Entry(window, width=30)
            entry.grid(row=index+1, column=1)
            entry.insert(0, patient_list[self.patient_num].get_data_by_num(index)) # 기존 데이터가 있을시 정보가 입력된 상태로 entry 생성
            self.info_entries.append(entry) # 정보 저장시 entry 객체에 접근할수 있도록 entry 리스트에 추가

        # set date button section on center
        for index in range(10):
            # MainWindow에서 버튼 생성했을때와 같이, partial에 의한 함수는 생성될때 값이 입력되므로 loop가 돌아가면서 값을 입력
            func = partial(self.get_record_by_chart_num, button_num=index)
            date_button = tk.Button(window, text=chart_list[self.patient_num * 10+index].get_date(),
                                    command=func)
            date_button.grid(row=index+1, column=4)

        # set medical record section on right
        self.record_entries = [] # entry 리스트는 창을 닫았다가 새로 여는 상황을 대비하여 꼭 초기화 하여함
        # GUI 생성시 필요한 라벨 정보들을 list로 관리하기에, for구문으로 편하게 라벨 생성
        # for구문에서 enumerate를 사용하기에 별도로 loop 횟수를 기록하는 변수를 생성할 필요가 없음. python스러운 방법.
        for index, value in enumerate(self.medical_record_labels):
            tk.Label(window, text=value).grid(row=index+1, column=5)
            if index > 1:
                entry = tk.Entry(window, width=50)
            else:
                entry = tk.Entry(window, width=10)
            entry.grid(row=index+1, column=6)
            entry.insert(0, chart_list[self.patient_num*10].get_data_by_num(index)) # 기존 데이터가 있을시 정보가 입력된 상태로 entry 생성
            self.record_entries.append(entry) # 정보 저장시 entry 객체에 접근할수 있도록 entry 리스트에 추가

        # set save buttons
        save_info_button = tk.Button(window, text='환자 정보 저장', command=self.save_patient_info)
        save_info_button.grid(row=11, column=1, pady=20)
        save_record_button = tk.Button(window, text='의무 기록 저장', command=self.save_medical_record)
        save_record_button.grid(row=11, column=6, pady=20)

        # initialize current chart num
        self.current_chart_num = 0

    def save_patient_info(self): # 환자 정보 저장 버튼 클릭시 호출
        print('환자 #', self.patient_num+1, '의 정보가 저장되었습니다.')
        patient = patient_list[self.patient_num]
        e = self.info_entries # 바로 아래 한줄 코드를 간결하게 하기 위해 짧은 변수인 e에 리스트를 할당. e변수르 지우고 리스트에 직접 접근하여도 무방
        patient.set_data(e[0].get() or '', e[1].get() or '', e[2].get() or '', e[3].get() or '') # entry가 비어있을때도 에러가 발생하지 않게, 데이터가 없을시 빈 값을 데이터로 전달

    def save_medical_record(self):
        print('의무 기록 #',  self.get_patient_chart_num()+1, '이 저장되었습니다.')
        chart = chart_list[self.get_patient_chart_num()]
        r = self.record_entries # 바로 아래 한줄 코드를 간결하게 하기 위해 짧은 변수인 e에 리스트를 할당. e변수르 지우고 리스트에 직접 접근하여도 무방
        chart.set_data(r[0].get() or '', r[1].get() or '', r[2].get() or '', r[3].get() or '', r[4].get() or '') # entry가 비어있을때도 에러가 발생하지 않게, 데이터가 없을시 빈 값을 데이터로 전달

    def get_patient_chart_num(self):
        # 차트에 편하게 접근할수 있도록, 전체 차트리스트에서 원하는 차트 번호를 계산.
        # 원칙적으로는 chart의 번호가 아니라 차트 객체를 반환해야하고, self.patient_num으로 차트에 접근해야 유지 보수에 용이.
        # 그러나 현재 단계에서는 한번이라도 더 함수를 호출하여 코드 줄을 줄일수 있게 차트의 번호를 반환하게 작성.
        # 추후 환자나 차트의 갯수가 변한다면, 함수명을 get_patient_chart로 바꾸고, 아래 코드와 같이 차트 객체를 반환해야함.
        # return patient_list[self.patient_num].charts[self.current_chart_num]
        return self.patient_num * 10 + self.current_chart_num 

    def get_record_by_chart_num(self, button_num): # 내원일 버튼을 클릭할시, 의무 기록 정보를 변경하기 위해 호출
        self.current_chart_num = button_num
        print('의무 기록 #', self.get_patient_chart_num()+1, '이 클릭 되었습니다.')
        chart = chart_list[self.get_patient_chart_num()]
        for index, entry in enumerate(self.record_entries): # for구문에서 enumerate를 사용하기에 별도로 loop 횟수를 기록하는 변수를 생성할 필요가 없음. python스러운 방법.
            entry.delete(0, 'end') # 기존 entry에 있는 정보를 삭제
            entry.insert(0, chart.get_data_by_num(index) # entry에 보유한 데이터를 입력


# 시작시 데이터를 저장할 환자 객체 10개를 생성하고, 각각의 환자 객체에 10개의 차트 객체를 할당
def set_up_models():
    """ Create 10 patient objects and assign 10 charts to each patient """
    for _ in range(10): # loop의 순서를 기록할 필요가 없는 것을 _를 활용하여 암시. python스러운 방법.
        patient = Patient()
        chart_to_add = []
        for _ in range(10): # loop의 순서를 기록할 필요가 없는 것을 _를 활용하여 암시. python스러운 방법.
            chart = Chart()
            chart_to_add.append(chart)
        patient.set_charts(chart_to_add) # 환자 객체에 차트 객체들을 할당하여, 추후 차트 객체 접근 및 관리에 용이
        patient_list.append(patient)
        chart_list.extend(chart_to_add)


if __name__ == "__main__": # 모듈이 직접적으로 호출되는 경우에만 아래 코드를 호출. 추후 해당 파일을 import하여 사용할 상황을 대비.
    set_up_models() # 데이터 저장소 생성
    root = tk.Tk() # tkinter 호출
    root.title("3rd-EMR") # 상단 타이틀 생성
    main = MainWindow(root) # tkinter를 MainWindow 클래스로 관리하여, 코드의 가독성을 높이고 추후 유지보수 및 관리를 대비
    main.pack(side="top", fill="both", expand=True)
    root.mainloop() # 화면 표시
