import datetime

import pymysql

import client_config


class DatabaseHandler:
    @staticmethod
    def connection_info():
        connection = pymysql.connect(
            host=client_config.db_ip,
            port=3306,
            user=client_config.db_client_user,
            password=client_config.db_client_pwd,
            database=client_config.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        return connection

    @classmethod
    def get_previews_info(cls):
        with cls.connection_info() as connection:
            query = 'SELECT title, isonsite AS assgn_type, host_entity, territory, vol_category, min_age, max_age, ' \
                    'assgn_expires, GROUP_CONCAT(CONCAT_WS(":", lang, isrequired)) AS languages FROM assignments ' \
                    'INNER JOIN languages ' \
                    'INNER JOIN assignments_languages ON assignments.assgn_id = assignments_languages.assgn_id AND ' \
                    'languages.lang_id = assignments_languages.lang_id ' \
                    'GROUP BY assignments.assgn_id ORDER BY doarequestno DESC LIMIT 20'
            with connection.cursor() as cursor:
                cursor.execute(query)
                previews_info = cursor.fetchall()

        now_utc0 = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        for assgn in previews_info:
            if assgn['assgn_expires'] < now_utc0:
                assgn['assgn_type'] = 'Archived'
            elif assgn['assgn_type'] == 0:
                assgn['assgn_type'] = 'Online'
            elif assgn['assgn_type'] == 1:
                assgn['assgn_type'] = 'Onsite'

            assgn['assgn_expires'] = assgn['assgn_expires'].strftime('%d %B %Y')

            assgn['languages'] = [tuple(lang_req.split(':')) for lang_req in assgn['languages'].split(',')]

        return previews_info

    @classmethod
    def get_distinct_values(cls, column):
        with cls.connection_info() as connection:
            query = f'SELECT DISTINCT {column} FROM assignments'
            with connection.cursor() as cursor:
                cursor.execute(query)
                dist_values = cursor.fetchall()
        dist_values_sorted = sorted([key[column].strip() for key in dist_values])

        return dist_values_sorted


if __name__ == '__main__':
    import sys
    from PyQt6 import QtWidgets
    from clickable_labels import QLabelClickableUnderline
    app = QtWidgets.QApplication(sys.argv)
    label1 = QLabelClickableUnderline(DatabaseHandler.get_previews_info, 'HAHA')
    label2 = QLabelClickableUnderline(lambda: print('Clicked'), 'HOHO')
    vbox = QtWidgets.QVBoxLayout()
    vbox.addWidget(label1)
    vbox.addWidget(label2)
    window = QtWidgets.QWidget()
    window.setLayout(vbox)
    window.show()
    sys.exit(app.exec())
