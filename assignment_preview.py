import re

from PyQt6 import QtWidgets, QtCore, QtGui

from clickable_labels import QLabelClickableUnderline


class AssignmentPreview(QtWidgets.QFrame):
    def __init__(self, data):
        super(AssignmentPreview, self).__init__()
        self.setObjectName('AssignmentPreviewParentFrame')
        self.setStyleSheet('QFrame#AssignmentPreviewParentFrame {'
                           'border: 2px solid black;'
                           'border-radius: 6px;'
                           'background-color: #ffebcd;'
                           '}')

        assgn_title_label = QLabelClickableUnderline(self.temp_func)
        assgn_title_label.setText(data['title'])
        assgn_title_label.setFont(QtGui.QFont('Arial', 14))

        assgn_type_label = QtWidgets.QLabel()
        assgn_type_label.setText(data['assgn_type'])
        assgn_type_label_background_variants = {'Onsite': '#8166a7', 'Online': '#007bbd', 'Archived': '#264b6a'}
        assgn_type_label_background_color = assgn_type_label_background_variants[data['assgn_type']]
        assgn_type_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        assgn_type_label.setObjectName('AssignmentTypeLabel')
        assgn_type_label.setStyleSheet('QLabel#AssignmentTypeLabel {'
                                       'border-radius: 8px;'
                                       'padding: 3px;'
                                       'color: white;'
                                       f'background-color: {assgn_type_label_background_color};'
                                       '}')

        title_and_type_hbox = QtWidgets.QHBoxLayout()
        title_and_type_hbox.addWidget(assgn_title_label)
        title_and_type_hbox.addStretch()
        title_and_type_hbox.addWidget(assgn_type_label)

        host_entity_label = QtWidgets.QLabel()
        host_entity_label.setText(f'<span style="color: #007fc4">{data["host_entity"]}</span>')

        territory_label = QtWidgets.QLabel()
        territory_label.setText(f'<span style="color: #ff4c00">{data["territory"]}</span>')

        vol_category_label = QtWidgets.QLabel()
        if data['vol_category'] is not None:
            vol_category_label.setText(f'<i>{data["vol_category"]}</i>')

        territory_and_category_hbox = QtWidgets.QHBoxLayout()
        territory_and_category_hbox.addWidget(territory_label)
        territory_and_category_hbox.addSpacing(20)
        territory_and_category_hbox.addWidget(vol_category_label)
        territory_and_category_hbox.addStretch()

        age_range = QtWidgets.QLabel()
        age_range.setText(f'<span style="color: #006241">Age:</span> {data["age"]}')

        languages_label = QtWidgets.QLabel()
        languages = []
        for lang, req in data['languages'].items():
            if req:
                lang = f'<b>{lang}</b>'
            languages.append(lang)
        languages_label.setText(f'<span style="color: #006241">Languages:</span> {", ".join(languages)}')

        assgn_expires_label = QtWidgets.QLabel()
        assgn_expires_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        assgn_expires_label.setText(f'<span style="color: #006241">Apply before: </span> {data["assgn_expires"]}')

        langs_and_expiration_hbox = QtWidgets.QHBoxLayout()
        langs_and_expiration_hbox.addWidget(languages_label)
        langs_and_expiration_hbox.addWidget(assgn_expires_label)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(title_and_type_hbox)
        vbox.addWidget(host_entity_label)
        vbox.addLayout(territory_and_category_hbox)
        vbox.addWidget(age_range)
        vbox.addLayout(langs_and_expiration_hbox)

        self.setLayout(vbox)

    def change_background_color(self, new_color):
        original_stylesheet = self.styleSheet()
        new_stylesheet = re.sub('(?<=background-color: ).*?(?=;)', new_color, original_stylesheet)
        self.setStyleSheet(new_stylesheet)

    @staticmethod
    def temp_func():
        print('Clicked!')


if __name__ == '__main__':
    import sys

    data1 = {'title': 'Community youth and adolescent engagement Officer', 'assgn_type': 'Onsite',
             'territory': 'India', 'vol_category': 'International UN Volunteer Specialist',
             'host_entity': 'MONUSCO', 'languages': {'French': False, 'English': True},
             'age': '27 - 80', 'assgn_expires': '10 April 2023'}

    data2 = {'title': 'Community youth and adolescent engagement Officer', 'assgn_type': 'Online',
             'territory': 'Democratic Republic of the Congo', 'vol_category': 'National UN Volunteer Specialist',
             'host_entity': 'UNICEF', 'languages': {'French': False, 'English': False},
             'age': '27 - 80', 'assgn_expires': '10 April 2023'}

    data3 = {'title': 'Community youth and adolescent engagement Officer', 'assgn_type': 'Archived',
             'territory': 'Germany', 'vol_category': None,
             'host_entity': 'UNMISS', 'languages': {'French': True, 'English': False},
             'age': '27 - 80', 'assgn_expires': '10 April 2023'}

    app = QtWidgets.QApplication(sys.argv)
    contents1 = AssignmentPreview(data1)
    contents2 = AssignmentPreview(data2)
    contents3 = AssignmentPreview(data3)
    contents2.change_background_color('#b7dffd')
    vbox1 = QtWidgets.QVBoxLayout()
    vbox1.addWidget(contents1)
    vbox1.addWidget(contents2)
    vbox1.addWidget(contents3)
    vbox1.addStretch()
    window = QtWidgets.QWidget()
    window.setLayout(vbox1)
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec())
