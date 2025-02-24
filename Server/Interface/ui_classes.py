from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import user_management, query_management, client_authentication, submissions_management, report_management
import json, time
  
class ui_widgets:
	def create_table_widget(col = 1, row = 1, headers = []):
		table = QTableWidget()
		table.setColumnCount(col)
		table.setRowCount(row)
		table.setHorizontalHeaderLabels(headers)
		# fit view to whole space
		table.resizeColumnsToContents()
		# Make table non-editable
		table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		# Enable Alternate row colors for readablity
		table.setAlternatingRowColors(True)
		# Select whole row when clicked
		table.setSelectionBehavior(QAbstractItemView.SelectRows)
		# Allow only one row to be selected
		table.setSelectionMode(QAbstractItemView.SingleSelection)
		# Enable Sorting
		table.setSortingEnabled(True)
		
		vertical_header = table.verticalHeader()
		vertical_header.setVisible(False)
		horizontal_header = table.horizontalHeader()
		horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
		return table

	def accounts_ui(self):
		heading = QLabel('Manage Accounts')
		heading.setObjectName('main_screen_heading')

		ie_accounts_button = QPushButton('Import/Export', self)
		ie_accounts_button.setFixedSize(200, 50)
		ie_accounts_button.clicked.connect(self.import_export_accounts)
		ie_accounts_button.setObjectName("topbar_button")

		create_accounts_button = QPushButton('Generate', self)
		create_accounts_button.setFixedSize(200, 50)
		create_accounts_button.clicked.connect(self.create_accounts)
		create_accounts_button.setObjectName("topbar_button")

		delete_account_button = QPushButton('Delete', self)
		delete_account_button.setFixedSize(200, 50)
		delete_account_button.clicked.connect(
			lambda:self.delete_account(accounts_model.selectionModel().selectedRows())
			)
		delete_account_button.setObjectName("topbar_button")
		delete_account_button.setToolTip('Delete account.\nCan be used when contest is \nnot RUNNING')

		accounts_model = ui_widgets.create_table_widget(3, 1, ['Username', 'Password', 'Type'])
		accounts_model.doubleClicked.connect(
			lambda:self.edit_account(accounts_model.selectionModel().selectedRows())
		)
 
		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(ie_accounts_button)
		head_layout.addWidget(create_accounts_button)
		head_layout.addWidget(delete_account_button)

		
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 10)
		head_layout.setStretch(2, 10)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)


		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(accounts_model)
		
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, accounts_model, delete_account_button
 
	def submissions_ui(self):
		heading = QLabel('All Runs')
		heading.setObjectName('main_screen_heading')

		edit_submission_button = QPushButton('Review', self)
		edit_submission_button.setFixedSize(200, 50)
		edit_submission_button.clicked.connect(
			lambda:self.manage_submission(submission_model.selectionModel().currentIndex().row())
		)
		edit_submission_button.setObjectName("topbar_button")
		edit_submission_button.setToolTip('Review selected submission')

		rejudge_problem_button = QPushButton('Group Rejudge', self)
		rejudge_problem_button.setFixedSize(200, 50)
		rejudge_problem_button.clicked.connect(
			lambda:self.rejudge_problem()
		)
		rejudge_problem_button.setObjectName("topbar_button")
		rejudge_problem_button.setToolTip('Rejudge all submissions for a problem for selected client.\nThis is a costly operation!')

		headers = ['Run ID', 'Client ID', 'Problem Code', 'Language', 'Time', 'Verdict', 'Status', 'Judge']
		submission_model = ui_widgets.create_table_widget(8, 1, headers)
		
		submission_model.doubleClicked.connect(
			lambda:self.manage_submission(submission_model.selectionModel().currentIndex().row())
		)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(edit_submission_button)
		head_layout.addWidget(rejudge_problem_button)
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 10)
		head_layout.setStretch(2, 10)

		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(submission_model)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		main.show()
		return main, submission_model


	def client_ui(self):
		headers = ['Client ID', 'Username', 'Password', 'IP Address', 'State']
		client_model = ui_widgets.create_table_widget(5, 1, headers)

		client_model.doubleClicked.connect(
			lambda:self.edit_client(client_model.selectionModel().currentIndex().row())
		)

		heading = QLabel('Connected Clients')
		heading.setObjectName('main_screen_heading')

		edit_client_button = QPushButton('Edit State', self)
		edit_client_button.setFixedSize(200, 50)
		edit_client_button.clicked.connect(
			lambda:self.edit_client(client_model.selectionModel().currentIndex().row())
		)
		edit_client_button.setObjectName("topbar_button")
		edit_client_button.setToolTip('Change client status.')

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(edit_client_button)
		head_layout.setStretch(0, 90)
		head_layout.setStretch(1, 10)
		
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(client_model)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)		

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, client_model

	def judge_ui(self):
		heading = QLabel('Connected Judges')
		heading.setObjectName('main_screen_heading')

		headers = ['Judge ID', 'Username', 'Password', 'IP Address', 'State']
		judge_model = ui_widgets.create_table_widget(5, 1, headers)

		judge_model.doubleClicked.connect(
			lambda:self.view_judge(judge_model.selectionModel().currentIndex().row())
		)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.setStretch(0, 100)
		
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(judge_model)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)		

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, judge_model


	def query_ui(self):
		heading = QLabel('All Clarifications')
		heading.setObjectName('main_screen_heading')

		reply_button = QPushButton('Reply')
		reply_button.setFixedSize(200, 50)
		reply_button.clicked.connect(
			lambda: self.query_reply(query_model.selectionModel().currentIndex().row())
			)
		reply_button.setObjectName("topbar_button")

		announcement_button = QPushButton('Announcement')
		announcement_button.setFixedSize(200, 50)
		announcement_button.clicked.connect(
			lambda: self.announcement()
		)
		announcement_button.setObjectName("topbar_button")

		headers = ['Query ID', 'Client ID', 'Query', 'Response']
		query_model = ui_widgets.create_table_widget(4, 1, headers)

		query_model.doubleClicked.connect(
			lambda:self.query_reply(query_model.selectionModel().currentIndex().row())
		)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(announcement_button)
		# head_layout.addWidget(reply_button)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(query_model)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)	
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, query_model


	def leaderboard_ui(self):
		heading = QLabel('Contest Standings')
		heading.setObjectName('main_screen_heading')

		scoring_num = self.data_changed_flags[17]
		if scoring_num == 1:
			# ACM Style ranking
			scoring_type = 'ACM'
			headers = ['Team', 'Problems Solved', 'Score', 'Total Time']
			col_count = 4
		elif scoring_num == 2:
			# IOI Style ranking
			scoring_type = 'IOI'
			headers = ['Team', 'Problems Solved', 'Score', 'Total Time']
			col_count = 4
		else:
			scoring_type = 'LONG'
			headers = ['Team', 'Problems Solved', 'Score', 'Total Time']
			col_count = 4

		scoring_label = QLabel('Scoring Type: ' + scoring_type)

		score_model = ui_widgets.create_table_widget(col_count, 1, headers)

		update_button = QPushButton('Broadcast Scoreboard')
		update_button.setToolTip('Manually send scoreboard to all clients.')
		update_button.setFixedSize(200, 50)
		update_button.clicked.connect(
			lambda: self.manual_broadcast_scoreboard()
		)
		update_button.setObjectName("topbar_button")

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(scoring_label)
		head_layout.addWidget(update_button)

		head_layout.setAlignment(heading, Qt.AlignLeft)
		head_layout.setAlignment(scoring_label, Qt.AlignCenter)
		head_layout.setAlignment(update_button, Qt.AlignRight)

		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(score_model)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		scoring_label.setObjectName('main_screen_content')
		main.show()
		return main, score_model, scoring_label

	def problem_ui(self):
		heading = QLabel('Manage Problems')
		heading.setObjectName('main_screen_heading')

		headers = ['Problem Name', 'Code', 'Test Files', 'Time Limit']
		problem_model = ui_widgets.create_table_widget(4, 1, headers)

		view_problem_button = QPushButton('Manage Problem', self)
		view_problem_button.setFixedSize(200, 50)
		view_problem_button.clicked.connect(
			lambda:self.view_problem(problem_model.selectionModel().currentIndex().row()) 
		)
		view_problem_button.setObjectName("topbar_button")
		view_problem_button.setToolTip('View/Edit Problems')

 
		problem_model.doubleClicked.connect(
			lambda:self.view_problem(problem_model.selectionModel().currentIndex().row())
		)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(view_problem_button)
		
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 10)
		head_layout.setStretch(2, 10)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(problem_model)
		
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, problem_model
		
	def get_stats_widget():
		contest_problems_subheading = QLabel('Problems: ')

		contest_problems_number = QLabel('Number of Problems: ')
		contest_problems_number_answer = QLabel('')	# Label Index 2
		contest_problems_layout = QHBoxLayout()
		contest_problems_layout.addWidget(contest_problems_number)
		contest_problems_layout.addWidget(contest_problems_number_answer)
		contest_problems_layout.addStretch(1)
		contest_problems_number_widget = QWidget()
		contest_problems_number_widget.setLayout(contest_problems_layout)

		participants_number = QLabel('Number of Teams with 1 or more submissions: ')
		participants_number_answer = QLabel('')	# Label Index 4
		participants_layout = QHBoxLayout()
		participants_layout.addWidget(participants_number)
		participants_layout.addWidget(participants_number_answer)
		participants_layout.addStretch(1)
		participants_number_widget = QWidget()
		participants_number_widget.setLayout(participants_layout)

		participants_pro_number = QLabel('Number of Teams with 1 or more Correct submissions: ')
		participants_pro_number_answer = QLabel('')	# Label Index 6
		participants_pro_layout = QHBoxLayout()
		participants_pro_layout.addWidget(participants_pro_number)
		participants_pro_layout.addWidget(participants_pro_number_answer)
		participants_pro_layout.addStretch(1)
		participants_pro_number_widget = QWidget()
		participants_pro_number_widget.setLayout(participants_pro_layout)

		problem_solved_table = QTableWidget()
		problem_solved_table.setColumnCount(4)
		problem_solved_table.setHorizontalHeaderLabels(
			("Problem", "Correct Submissions", "Total Submissions", "Accuracy")
		)

		problem_solved_table.resizeColumnsToContents()
		problem_solved_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		problem_solved_table.setAlternatingRowColors(True)
		vertical_header = problem_solved_table.verticalHeader()
		vertical_header.setVisible(False)
		horizontal_header = problem_solved_table.horizontalHeader()
		horizontal_header.setSectionResizeMode(QHeaderView.Stretch)

		main_layout = QVBoxLayout()
		main_layout.addWidget(contest_problems_subheading)
		main_layout.addWidget(contest_problems_number_widget)
		main_layout.addWidget(participants_number_widget)
		main_layout.addWidget(participants_pro_number_widget)
		main_layout.addWidget(problem_solved_table)
		main_layout.setStretch(4, 50)
		

		main = QWidget()
		main.setLayout(main_layout)
		contest_problems_subheading.setObjectName('main_screen_sub_heading')
		contest_problems_number.setObjectName('main_screen_content')
		contest_problems_number_answer.setObjectName('main_screen_content')
		participants_number.setObjectName('main_screen_content')
		participants_number_answer.setObjectName('main_screen_content')
		participants_pro_number.setObjectName('main_screen_content')
		participants_pro_number_answer.setObjectName('main_screen_content')
		problem_solved_table.setObjectName('inner_table')
		return main

	def update_stats(self, stats_widget):
		accuracy = 0
		child_list = stats_widget.findChildren(QLabel)
		table_list = stats_widget.findChildren(QTableWidget)
		# 2nd QLabel in this list is contest_problems_number_answer
		number_of_problems = self.config['Number Of Problems']
		child_list[2].setText(str(number_of_problems))
		number_of_problems = int(number_of_problems)

		# table_list[0] contains problem_solved_table
		table_list[0].setRowCount(int(number_of_problems))

		code_tuple = self.config['Problem Codes']
		for i in range(0, number_of_problems ):

			table_list[0].setItem(i, 0, QTableWidgetItem(code_tuple[i]))
			# Get how many clients solved this problem
			solve_count = report_management.get_ac_count(code_tuple[i])
			table_list[0].setItem(i, 1, QTableWidgetItem(str(solve_count)))

			# Get how many clients submitted a code for this problem
			submit_count = report_management.get_submission_count(code_tuple[i])
			table_list[0].setItem(i, 2, QTableWidgetItem(str(submit_count)))

			if submit_count == 0:
				accuracy = '{0:.2f}'.format(0)
			else:
				accuracy = float(solve_count*100/submit_count)
				accuracy = '{0:.2f}'.format(accuracy)
			table_list[0].setItem(i, 3, QTableWidgetItem(str(accuracy) + "%"))

		# Get number of active participants
		participant_count = report_management.get_participant_count()
		child_list[4].setText(str(participant_count))

		# Get number of active pro participants
		participant_pro_count = report_management.get_participant_pro_count()
		child_list[6].setText(str(participant_pro_count))

		return

	def stats_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Contest Stats')
		heading.setObjectName('main_screen_heading')

		stats_widget = ui_widgets.get_stats_widget()

		update_button = QPushButton('Update Stats')
		update_button.clicked.connect(
			lambda:ui_widgets.update_stats(self, stats_widget)
		)
		update_button.setFixedSize(200, 50)

		top_layout = QHBoxLayout()
		top_layout.addWidget(heading)
		top_layout.addWidget(update_button)
		top_layout.setStretch(0, 80)
		top_layout.setStretch(1, 20)
		top_widget = QWidget()
		top_widget.setLayout(top_layout)

		main_layout.addWidget(top_widget)
		main_layout.addWidget(stats_widget)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		update_button.setObjectName('topbar_button')
		# Update stats UI first time
		ui_widgets.update_stats(self, stats_widget)
		return main

	def time_limit_updater(self, text):
		print('[ SETTING ] Contest submission time limit set to: ' + str(text) + ' minutes.')
		self.data_changed_flags[21] = int(text)
		return

	def contest_time_settings(self):
		# Contest Time Management
		## Contest Time Settings Label:
		contest_time_label = QLabel('Contest Time Settings:')
		contest_time_label.setObjectName('main_screen_sub_heading')

		# Set contest time 
		contest_duration_label = QLabel('> Contest Duration: ')
		contest_duration_label.setObjectName('main_screen_content')
		contest_duration_label.setFixedSize(200, 20)

		contest_time_entry = QLineEdit()
		contest_time_entry.setText(self.config["Contest Duration"])
		contest_time_entry.setPlaceholderText('HH:MM:SS')
		contest_time_entry.setFixedSize(80, 30)
		contest_time_entry.setToolTip(
			'Set Contest duration. Press Set to confirm.' + 
			'\nYou will not be able to edit this when contest starts.'
		)

		contest_time_layout = QHBoxLayout()
		contest_time_layout.addWidget(contest_duration_label)
		contest_time_layout.addWidget(contest_time_entry)
		contest_time_layout.addStretch(1)
		contest_time_layout.setSpacing(5)
		contest_time_layout.setContentsMargins(5, 0, 10, 0)
		contest_time_widget = QWidget()
		contest_time_widget.setLayout(contest_time_layout)

		contest_extension_label = QLabel("> Extend/Shorten contest by: ")
		contest_extension_label.setObjectName('main_screen_content')
		minutes_label = QLabel(" Minutes")
		minutes_label.setObjectName('main_screen_content')

		change_time_entry = QSpinBox()
		change_time_entry.setMinimum(-60)
		change_time_entry.setMaximum(60)
		change_time_entry.setValue(0)
		change_time_entry.setReadOnly(True)
		change_time_entry.setToolTip(
			'Extend the contest in minutes.' + 
			'\nYou will be able to use it when contest is STARTED'
		)

		change_time_layout = QHBoxLayout()
		change_time_layout.addWidget(contest_extension_label)
		change_time_layout.addWidget(change_time_entry)
		change_time_layout.addWidget(minutes_label)
		change_time_layout.addStretch(1)
		change_time_layout.setSpacing(5)
		change_time_layout.setContentsMargins(5, 0, 10, 0)
		change_time_widget = QWidget()
		change_time_widget.setLayout(change_time_layout)

		submission_limit_label = QLabel("> Submission Time Limit: ")
		submission_limit_label.setObjectName('main_screen_content')
		submission_limit_label.setToolTip(
			'Set Time limit before a Client\nis allowed to send a new solution.'
			+
			'\nIncrease this when Server is under load'
		)
		submission_limit = QSpinBox()
		submission_limit.setMinimum(0)
		submission_limit.setMaximum(5)
		submission_limit.setValue(self.data_changed_flags[21])
		submission_limit.setToolTip('Set Submission per N minute rule.\nIncrease/Decrease works instantly.')
		submission_limit.valueChanged.connect(
			lambda:ui_widgets.time_limit_updater(self, submission_limit.text())
		)
		minutes1_label = QLabel(" Minutes")
		minutes1_label.setObjectName('main_screen_content')
		submission_limit_layout = QHBoxLayout()
		submission_limit_layout.addWidget(submission_limit_label)
		submission_limit_layout.addWidget(submission_limit)
		submission_limit_layout.addWidget(minutes1_label)
		submission_limit_layout.addStretch(1)
		submission_limit_layout.setSpacing(5)
		submission_limit_widget = QWidget()
		submission_limit_widget.setLayout(submission_limit_layout)

		# Start, Stop, Pause contest
		set_button = QPushButton('Set')
		set_button.setFixedSize(70, 25)
		set_button.setObjectName('interior_button')
		set_button.setToolTip('Set contest time.\nThis does NOT broadcast to clients.')
		set_button.clicked.connect(
			lambda: ui_widgets.preprocess_contest_broadcasts(self, 'SET', contest_time_entry.text())
		)

		start_button = QPushButton('Start', self)
		start_button.setFixedSize(70, 25)
		start_button.setObjectName('interior_button')
		start_button.setToolTip('START the contest and broadcast to all clients.')
		start_button.clicked.connect(
			lambda: ui_widgets.preprocess_contest_broadcasts(self, 'START', contest_time_entry.text())
		)

		update_button = QPushButton('Update', self)
		update_button.setEnabled(False)
		update_button.setFixedSize(70, 25)
		update_button.setObjectName('interior_button')
		update_button.setToolTip(
			'UPDATE contest time and broadcast to all clients.\nDisabled until contest Starts'
		)
		update_button.clicked.connect(
			lambda: ui_widgets.preprocess_contest_broadcasts(self, 'UPDATE', change_time_entry.value())
		)	

		stop_button = QPushButton('Stop', self)
		stop_button.setEnabled(False)
		stop_button.setFixedSize(70, 25)
		stop_button.setObjectName('interior_button')
		stop_button.setToolTip(
			'STOP the contest and broadcast to all clients.\nDisabled until contest Starts'
		)
		stop_button.clicked.connect(
			lambda: ui_widgets.preprocess_contest_broadcasts(self, 'STOP')
		)
		
		contest_buttons_layout = QHBoxLayout()
		contest_buttons_layout.addWidget(set_button)
		contest_buttons_layout.addWidget(start_button)
		contest_buttons_layout.addWidget(update_button)
		contest_buttons_layout.addWidget(stop_button)

		contest_buttons_layout.addStretch(1)
		contest_buttons_layout.setSpacing(10)
		contest_buttons_widget = QWidget()
		contest_buttons_widget.setLayout(contest_buttons_layout)

		time_management_layout = QVBoxLayout()
		time_management_layout.addWidget(contest_time_label)
		time_management_layout.addWidget(contest_time_widget)
		time_management_layout.addWidget(change_time_widget)
		time_management_layout.addWidget(submission_limit_widget)
		time_management_layout.addWidget(contest_buttons_widget)
		time_management_layout.addStretch(1)
		time_management_widget = QWidget()
		time_management_widget.setLayout(time_management_layout)
		time_management_widget.setObjectName('content_box')
		return (
			time_management_widget, contest_time_entry, change_time_entry, 
			set_button, start_button, update_button, stop_button
			)

	def preprocess_contest_broadcasts(self, signal, extra_data = 'NONE'):
		#process_event() is defined in interface package
		if signal == 'SET':
			#Validate extra data to be time
			if ui_widgets.validate_date(self, extra_data) == True:
				self.process_event('SET', extra_data)
			else:
				return
		elif signal == 'START':
			#Validate extra data to be time
			if ui_widgets.validate_date(self, extra_data) == True:
				self.process_event('START', extra_data)	
			else:
				return
			
		elif signal == 'UPDATE':
			status = self.password_verification()
			if status == 1:
				self.process_event('UPDATE', extra_data)
			elif status == 2: 
				return
			else:
				QMessageBox.about(self, "Access Denied!", "Authentication failed!")
			
		elif signal == 'STOP':
			status = self.password_verification()
			if status == 2: 
				# Cancel pressed
				return
			elif status == 1:
				self.process_event('STOP', extra_data)
			else:
				QMessageBox.about(self, "Access Denied!", "Authentication failed!")
		return
		
	def validate_date(self, data):
		#Check that data is a valid date in HH:MM:SS format
		try:
			h, m, s = data.split(':')
			if len(h) != 2 or len(m) != 2 or len(s) != 2:
				print('[ ERROR ] Enter time in HH:MM:SS format only!')
				return False
			h = int(h)
			m = int(m)
			s = int(s)
			if h < 0 or h > 24 or m < 0 or m > 59 or s < 0 or s > 59:
				QMessageBox.about(self, "Error!", "Enter time in HH:MM:SS format only!")
				return False
			return True
		except:
			QMessageBox.about(self, "Error!", "Enter time in HH:MM:SS format only!")
			return False



	def contest_reset_settings(self):
		contest_reset_label = QLabel('Reset Contest:')
		contest_reset_label.setObjectName('main_screen_sub_heading')

		# Reset contest labels and buttons
		account_reset_label = QLabel('> Reset Accounts ')
		account_reset_label.setObjectName('main_screen_content')
		account_reset_label.setFixedSize(200, 25)
		account_reset_button = QPushButton('RESET')
		account_reset_button.setFixedSize(70, 25)
		account_reset_button.setObjectName('interior_button')
		account_reset_button.setToolTip(
			'DELETE all accounts.\nConnected clients will NOT be disconnected.'
			)
		account_reset_button.clicked.connect(self.reset_accounts)
		account_reset_layout = QHBoxLayout()
		account_reset_layout.addWidget(account_reset_label)
		account_reset_layout.addWidget(account_reset_button)
		account_reset_layout.addStretch(1)
		account_reset_widget = QWidget()
		account_reset_widget.setLayout(account_reset_layout)


		submission_reset_label = QLabel('> Reset Submissions ')
		submission_reset_label.setObjectName('main_screen_content')
		submission_reset_label.setFixedSize(200, 25)
		submission_reset_button = QPushButton('RESET')
		submission_reset_button.setFixedSize(70, 25)
		submission_reset_button.setObjectName('interior_button')
		submission_reset_button.setToolTip('DELETE all submissions.')
		submission_reset_button.clicked.connect(self.reset_submissions)
		submission_reset_layout = QHBoxLayout()
		submission_reset_layout.addWidget(submission_reset_label)
		submission_reset_layout.addWidget(submission_reset_button)
		submission_reset_layout.addStretch(1)
		submission_reset_widget = QWidget()
		submission_reset_widget.setLayout(submission_reset_layout)

		query_reset_label = QLabel('> Reset Queries ')
		query_reset_label.setObjectName('main_screen_content')
		query_reset_label.setFixedSize(200, 25)
		query_reset_button = QPushButton('RESET')
		query_reset_button.setFixedSize(70, 25)
		query_reset_button.setObjectName('interior_button')
		query_reset_button.setToolTip('DELETE all queries')
		query_reset_button.clicked.connect(self.reset_queries)
		query_reset_layout = QHBoxLayout()
		query_reset_layout.addWidget(query_reset_label)
		query_reset_layout.addWidget(query_reset_button)
		query_reset_layout.addStretch(1)
		query_reset_widget = QWidget()
		query_reset_widget.setLayout(query_reset_layout)

		client_reset_label = QLabel('> Disconnect All ')
		client_reset_label.setObjectName('main_screen_content')
		client_reset_label.setFixedSize(200, 25)
		client_reset_button = QPushButton('RESET')
		client_reset_button.setFixedSize(70, 25)
		client_reset_button.setObjectName('interior_button')
		client_reset_button.setToolTip('Disconnect all clients and judges.')
		client_reset_button.clicked.connect(self.disconnect_all)
		client_reset_layout = QHBoxLayout()
		client_reset_layout.addWidget(client_reset_label)
		client_reset_layout.addWidget(client_reset_button)
		client_reset_layout.addStretch(1)
		client_reset_widget = QWidget()
		client_reset_widget.setLayout(client_reset_layout)

		timer_reset_label = QLabel('> Reset Timer ')
		timer_reset_label.setObjectName('main_screen_content')
		timer_reset_label.setFixedSize(200, 25)
		timer_reset_button = QPushButton('RESET')
		timer_reset_button.setFixedSize(70, 25)
		timer_reset_button.setObjectName('interior_button')
		timer_reset_button.setToolTip('Reset contest timer and state.\nCan be used when contest is STOPPED.')
		timer_reset_button.clicked.connect(self.reset_timer)
		timer_reset_layout = QHBoxLayout()
		timer_reset_layout.addWidget(timer_reset_label)
		timer_reset_layout.addWidget(timer_reset_button)
		timer_reset_layout.addStretch(1)
		timer_reset_widget = QWidget()
		timer_reset_widget.setLayout(timer_reset_layout)

		server_reset_label = QLabel('> Reset SERVER ')
		server_reset_label.setObjectName('main_screen_content')
		server_reset_label.setFixedSize(200, 25)
		server_reset_button = QPushButton('CONFIRM')
		server_reset_button.setEnabled(True)
		server_reset_button.setFixedSize(70, 25)
		server_reset_button.setObjectName('interior_button')
		server_reset_button.setToolTip('Reset the Server.\nCan not be used in RUNNING state.')
		server_reset_button.clicked.connect(self.reset_server)
		server_reset_layout = QHBoxLayout()
		server_reset_layout.addWidget(server_reset_label)
		server_reset_layout.addWidget(server_reset_button)
		server_reset_layout.addStretch(1)
		server_reset_widget = QWidget()
		server_reset_widget.setLayout(server_reset_layout)

		button_layout = QGridLayout()
		button_layout.addWidget(account_reset_widget, 0, 0)
		button_layout.addWidget(submission_reset_widget, 0, 1)
		button_layout.addWidget(query_reset_widget, 1, 0)
		button_layout.addWidget(client_reset_widget, 1, 1)
		button_layout.addWidget(timer_reset_widget, 2, 0)
		button_layout.addWidget(server_reset_widget, 2, 1)
		button_layout.setColumnStretch(0,1)
		button_layout.setColumnStretch(1,3)

		button_widget = QWidget()
		button_widget.setLayout(button_layout)

		contest_reset_layout = QVBoxLayout()
		contest_reset_layout.addWidget(contest_reset_label)
		contest_reset_layout.addWidget(button_widget)
		contest_reset_layout.addStretch(1)
		contest_reset_widget = QWidget()
		contest_reset_widget.setLayout(contest_reset_layout)
		contest_reset_widget.setObjectName('content_box')
		return (
			contest_reset_widget, 
			account_reset_button, 
			submission_reset_button, 
			query_reset_button, 
			client_reset_button, 
			server_reset_button,
			timer_reset_button
		)

	def contest_flag_settings(self):
		contest_reset_label = QLabel('Contest Flags:')
		contest_reset_label.setObjectName('main_screen_sub_heading')

		allow_client_login_label = QLabel('Allow Logins')
		allow_client_login_label.setObjectName('main_screen_content')
		tooltip = ('Allow clients to Login.')
		allow_client_login_label.setToolTip(tooltip)
		allow_client_login_flag = self.check_login_allowed()
		allow_client_login_button = QCheckBox('')
		allow_client_login_button.setFixedSize(30, 30)
		allow_client_login_button.setChecked(allow_client_login_flag)
		allow_client_login_button.stateChanged.connect(self.allow_login_handler)
		allow_client_login_widget = ui_widgets.get_horizontal_widget(allow_client_login_button, allow_client_login_label)

		allow_judge_login_label = QLabel('Allow Judge Logins')
		allow_judge_login_label.setObjectName('main_screen_content')
		tooltip = ('Allow judges to Login.')
		allow_judge_login_label.setToolTip(tooltip)
		allow_judge_login_flag = self.check_judge_login_allowed()
		allow_judge_login_button = QCheckBox('')
		allow_judge_login_button.setFixedSize(30, 30)
		allow_judge_login_button.setChecked(allow_judge_login_flag)
		allow_judge_login_button.stateChanged.connect(self.allow_judge_login_handler)
		allow_judge_login_widget = ui_widgets.get_horizontal_widget(allow_judge_login_button, allow_judge_login_label)

		submission_allowed_flag = self.check_submission_allowed()
		allow_submission_label = QLabel('Allow Submissions')
		allow_submission_label.setObjectName('main_screen_content')
		allow_submission_label.setToolTip('Allow/Disallow client submissions.')
		allow_submission_button = QCheckBox('')
		allow_submission_button.setFixedSize(30, 30)
		allow_submission_button.setChecked(submission_allowed_flag)
		allow_submission_button.stateChanged.connect(self.allow_submissions_handler)
		allow_submission_widget = ui_widgets.get_horizontal_widget(allow_submission_button, allow_submission_label)

		manual_review_flag = self.check_manual_review_allowed()
		manual_review_label = QLabel('Manual Review')
		manual_review_label.setObjectName('main_screen_content')
		manual_review_label.setToolTip(
			'Review each submission before updating Leaderboard and sending client response.' +
			'\nWhen disbled, you can choose to release all under Review submissions.'
		)
		manual_review_button = QCheckBox('')
		manual_review_button.setFixedSize(30, 30)
		manual_review_button.setChecked(manual_review_flag)
		manual_review_button.stateChanged.connect(self.manual_reviews_handler)
		manual_review_widget = ui_widgets.get_horizontal_widget(manual_review_button, manual_review_label)

		ip_checker_label = QLabel('Users can change IP') 
		tooltip = (
			'When enabled, clients will be able to login with same' +
			'\ncredentials on different machines.'
		)
		ip_checker_label.setToolTip(tooltip)
		ip_checker_label.setObjectName('main_screen_content')
		ip_checker_button = QCheckBox('')
		ip_checker_button.setFixedSize(30, 30)
		ip_checker_button.setChecked(False)
		ip_checker_button.stateChanged.connect(self.allow_ip_change_handler)
		ip_checker_widget = ui_widgets.get_horizontal_widget(ip_checker_button, ip_checker_label)

		same_ip_label = QLabel('One client per IP')
		tooltip = ('When enabled, participants will not be able to open two clients on same machine' +
			'\nThis may cause issues when clients are on a shared network.'
		)
		same_ip_label.setToolTip(tooltip)
		same_ip_label.setObjectName('main_screen_content')
		same_ip_button = QCheckBox('')
		same_ip_button.setFixedSize(30, 30)
		same_ip_button.setChecked(False)
		same_ip_button.stateChanged.connect(self.allow_same_ip_handler)
		same_ip_widget = ui_widgets.get_horizontal_widget(same_ip_button, same_ip_label)

		update_scoreboard_label = QLabel('Allow Scoreboard Broadcast')
		update_scoreboard_label.setObjectName('main_screen_content')
		update_scoreboard_flag = self.check_scoreboard_update_allowed()
		update_scoreboard_button = QCheckBox('')
		update_scoreboard_button.setFixedSize(30, 30)
		update_scoreboard_button.setChecked(update_scoreboard_flag)
		update_scoreboard_button.stateChanged.connect(self.allow_scoreboard_update_handler)
		update_scoreboard_widget = ui_widgets.get_horizontal_widget(update_scoreboard_button, update_scoreboard_label)

		button_layout = QGridLayout()
		button_layout.addWidget(allow_client_login_widget, 0, 0)
		button_layout.addWidget(allow_judge_login_widget, 0, 1)
		button_layout.addWidget(allow_submission_widget, 1, 0)
		button_layout.addWidget(manual_review_widget, 1, 1)
		button_layout.addWidget(ip_checker_widget, 2, 0)
		button_layout.addWidget(same_ip_widget, 2, 1)
		button_layout.addWidget(update_scoreboard_widget, 3, 0)
		button_layout.setColumnStretch(0,1)
		button_layout.setColumnStretch(1,3)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)

		contest_reset_layout = QVBoxLayout()
		contest_reset_layout.addWidget(contest_reset_label)
		contest_reset_layout.addWidget(button_widget)
		contest_reset_layout.addStretch(1)
		contest_reset_widget = QWidget()
		contest_reset_widget.setLayout(contest_reset_layout)
		contest_reset_widget.setObjectName('content_box')
		return contest_reset_widget
		
	def settings_ui(self):
		heading = QLabel('Server Settings')
		heading.setObjectName('main_screen_heading')

		generate_report_button = QPushButton('Reports', self)
		generate_report_button.setFixedSize(200, 50)
		generate_report_button.clicked.connect(
			self.generate_report
		) 
		generate_report_button.setObjectName("topbar_button")
		generate_report_button.setToolTip('Generate contest reports')

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(generate_report_button)
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 10)
		head_layout.setStretch(2, 10)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		(
			time_management_widget, 
			contest_time_entry, 
			change_time_entry, 
			set_button, 
			start_button, 
			update_button, 
			stop_button
		) = ui_widgets.contest_time_settings(self)

		(
			contest_reset_widget, 
			account_reset_button, 
			submission_reset_button, 
			query_reset_button, 
			client_reset_button, 
			server_reset_button, 
			timer_reset_button
		) = ui_widgets.contest_reset_settings(self)

		contest_flag_widget = ui_widgets.contest_flag_settings(self)
		
		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(time_management_widget)
		main_layout.addWidget(contest_reset_widget)
		main_layout.addWidget(contest_flag_widget)
		main_layout.setStretch(0, 10)
		main_layout.setStretch(1, 30)
		main_layout.setStretch(2, 30)
		main_layout.setStretch(3, 30)


		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return (
			main, 
			contest_time_entry, 
			change_time_entry, 
			set_button, 
			start_button, 
			update_button, 
			stop_button, 
			account_reset_button, 
			submission_reset_button, 
			query_reset_button, 
			client_reset_button, 
			server_reset_button,
			timer_reset_button
		)

	def about_us_ui(self):
		head1 = QLabel('Made with <3 by Team Bitwise')
		head1.setObjectName('about_screen_heading')
		
		head2 = QLabel('Guess what? The BitsOJ project is open source!')
		head2.setObjectName('main_screen_content')
		
		head3 = QLabel('Contribute ')
		head3.setObjectName('main_screen_content')

		link = QLabel("<a href='https://github.com/peeesspee/BitsOJ' style = 'color: #23B2EE'>Here</a>")
		link.setObjectName('main_screen_content')
		link.setToolTip(
			'Opens github repository link in web browser.'
		)
		link.setTextInteractionFlags(Qt.TextBrowserInteraction)
		link.setOpenExternalLinks(True)

		link_widget = ui_widgets.get_horizontal_widget(head3, link)
		
		sub_head1 = QLabel('Team BitsOJ')
		sub_head1.setObjectName('about_screen_heading_2')

		mentor_widget = ui_widgets.get_profile_widget(
			'Mentor',
			'@rast_7',
			'Rajat Asthana',
			'rast-7',
			'rast7'
		)
		server_dev_widget = ui_widgets.get_profile_widget(
			'Server Dev',
			'@valiant1',
			'Prakhar Pandey',
			'valiant1011',
			'valiant1011'
		)
		client_dev_widget = ui_widgets.get_profile_widget(
			'Client/Setup Dev',
			'@sachinam',
			'Sachinam Srivastava',
			'sachinam1397',
			'sachinam1397'
		)
		judge_dev_widget = ui_widgets.get_profile_widget(
			'Judge Dev',
			'@ps',
			'Prashant Singh',
			'ps0798',
			'ps0798'
		)

		cards_widget = QWidget()
		cards_layout = QHBoxLayout(cards_widget)
		cards_layout.addStretch(5)
		cards_layout.addWidget(mentor_widget)
		cards_layout.addStretch(2)
		cards_layout.addWidget(server_dev_widget)
		cards_layout.addStretch(2)
		cards_layout.addWidget(client_dev_widget)
		cards_layout.addStretch(2)
		cards_layout.addWidget(judge_dev_widget)
		cards_layout.addStretch(5)

		cards_layout.setContentsMargins(0, 10, 0, 10)
		
		main_layout = QVBoxLayout()
		main_layout.addStretch(5)
		
		main_layout.addWidget(sub_head1)
		main_layout.addStretch(1)
		main_layout.addWidget(cards_widget)
		main_layout.addStretch(5)

		main_layout.addWidget(head1)
		main_layout.addWidget(head2)
		main_layout.addWidget(link_widget)

		main_layout.addStretch(5)

		main_layout.setAlignment(head1, Qt.AlignCenter)
		main_layout.setAlignment(head2, Qt.AlignCenter)
		main_layout.setAlignment(link_widget, Qt.AlignCenter)
		main_layout.setAlignment(sub_head1, Qt.AlignCenter)

		main = QWidget()
		main.setLayout(main_layout)
		return main

	def get_profile_widget(
			title = 'None',
			username = 'None',
			name = 'None',
			github_id = 'None', 
			linkedin_id = 'None'
		):
		# Shadow effect initialisation
		shadow_effect = QGraphicsDropShadowEffect()
		shadow_effect.setBlurRadius(15)
		shadow_effect.setOffset(0)
		shadow_effect.setColor(QColor(0, 0, 0, 255))

		# Get cards for team members
		top_layout = QVBoxLayout()

		title_widget = QLabel(title)
		title_widget.setObjectName('role_text')

		banner_widget = QLabel(username)
		banner_widget.setObjectName('banner_text')
		banner_overlay_layout = QHBoxLayout()
		banner_overlay_layout.addWidget(banner_widget)
		banner_overlay_widget = QWidget()
		banner_overlay_widget.setLayout(banner_overlay_layout)
		banner_overlay_widget.setObjectName('banner_overlay')
		# banner_widget.setGraphicsEffect(shadow_effect)

		name_widget = QLabel(name)
		name_widget.setObjectName('card_content')

		github_link = "https://www.github.com/" + github_id
		linkedin_link = "https://www.linkedin.com/in/" + linkedin_id
		
		github_id_heading = QLabel('Github')
		github_pixmap = QPixmap('./Elements/github.png')
		# github_pixmap = github_pixmap.scaledToWidth(32)
		github_id_heading.setPixmap(github_pixmap)
		github_id_heading.setFixedSize(48, 48)
		github_id_widget = QLabel(
			"<a href='" + github_link + "' style = 'color: #23B2EE'>" + github_id + "</a>"
		)
		github_id_widget.setTextInteractionFlags(Qt.TextBrowserInteraction)
		github_id_widget.setOpenExternalLinks(True)
		github_id_widget.setObjectName('card_content')
		github_hwidget = ui_widgets.get_horizontal_widget(github_id_heading, github_id_widget)
	
		linkedin_id_heading = QLabel('LinkedIn')
		linkedin_pixmap = QPixmap('./Elements/linkedin.png')
		linkedin_id_heading.setPixmap(linkedin_pixmap)
		linkedin_id_heading.setFixedSize(48, 48)
		linkedin_id_widget = QLabel(
			"<a href='" + linkedin_link + "' style = 'color: #23B2EE'>" + linkedin_id + "</a>"
		)
		linkedin_id_widget.setTextInteractionFlags(Qt.TextBrowserInteraction)
		linkedin_id_widget.setOpenExternalLinks(True)
		linkedin_id_widget.setObjectName('card_content')
		linkedin_hwidget = ui_widgets.get_horizontal_widget(linkedin_id_heading, linkedin_id_widget)
		
		top_layout.addWidget(title_widget)
		top_layout.addWidget(banner_overlay_widget)
		top_layout.addWidget(name_widget)
		top_layout.addWidget(github_hwidget)
		top_layout.addWidget(linkedin_hwidget)
		top_layout.addStretch(1)
		top_layout.setAlignment(title_widget, Qt.AlignCenter)
		top_widget = QWidget()
		top_widget.setLayout(top_layout)
		top_widget.setFixedWidth(270)
		top_widget.setObjectName('card')
		top_widget.setGraphicsEffect(shadow_effect)
		# top_widget.setMinimumSize(320, 300)
		return top_widget

	def get_horizontal_widget(widget_1, widget_2):
		layout = QHBoxLayout()
		layout.addWidget(widget_1)
		layout.addWidget(widget_2)
		layout.addStretch(1)
		widget = QWidget()
		widget.setLayout(layout)
		return widget

	def lock_ui(self):
		head1 = QLabel('SERVER LOCKED')
		head1.setObjectName('about_screen_heading')
		head1.setAlignment(Qt.AlignCenter)
		head2 = QLabel('Please Enter Admin Password to unlock server')
		head2.setObjectName('main_screen_content')
		head2.setAlignment(Qt.AlignCenter)
		
		password_input = QLineEdit()
		password_input.setFixedSize(200, 35)
		password_input.setAlignment(Qt.AlignCenter)
		password_input.setPlaceholderText('Admin Password')
		password_input.setEchoMode(QLineEdit.Password)
		password_input.setText('')
		submit_button = QPushButton('Confirm')
		submit_button.setFixedSize(100, 33)
		submit_button.setObjectName('interior_button')
		submit_button.clicked.connect(lambda: ui_widgets.unlock_ui(self, password_input, head1))
		submit_button.setDefault(True)
		password_layout = QHBoxLayout()
		password_layout.addStretch(50)
		password_layout.addWidget(password_input)
		password_layout.addWidget(submit_button)
		password_layout.addStretch(50)
		password_widget = QWidget()
		password_widget.setLayout(password_layout)
		
		main_layout = QVBoxLayout()
		main_layout.addStretch(50)
		main_layout.addWidget(head1)
		main_layout.addWidget(head2)
		main_layout.addWidget(password_widget)
		main_layout.addStretch(50)
		
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main

	def unlock_ui(self, password_input, heading_1):
		entry = password_input.text()
		password_input.setText('')
		status = self.validate_password(entry)
		if status:
			# Password verified
			self.data_changed_flags[24] = 0		# Set unlock flag
			# heading_1.setText('SERVER UNLOCKED')
			# heading_1.setObjectName('')
			print('[ GUI ][ LOCK ] Server GUI has been unlocked.')
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Information)
			info_box.setWindowTitle('Success')
			info_box.setText('Server Unlocked!')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
		else:
			heading_1.setText('SERVER LOCKED')
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Failure')
			info_box.setText('Password verification failed!')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()


