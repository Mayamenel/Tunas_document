from __future__ import unicode_literals
import frappe
import datetime
import locale
import json

from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, getdate

# hitung thp berdasarkan salary slip log
# kembaliin pajak yg lebih bayar ketika gaji berkurang

# ptkp tidak berubah kalau employee pindah maka employee akan menghitung sendiri ketika spt tahunan
# ptkp tidak dikalikan dengan sisa bulan

cur_year = datetime.datetime.now().year
cur_month = datetime.datetime.now().month - 1
sisa_bulan = 12 - cur_month

def test():
	print "hello"

def get_prev_thp_tax(emp,fiscal_year):
	thp, tax = 0, 0
	if emp.salary_slip_log:
		for log in emp.salary_slip_log:
			if fiscal_year == log.year :
				# mgkn perlu revisi ini penghitungan tanpa one time frequency
				thp += log.thp
				tax += log.paid_tax

	return thp, tax

@frappe.whitelist()
def get_pph(employee, thp, doc):

	emp = frappe.get_doc("Employee", employee)
	
	paid_thp, paid_tax = get_prev_thp_tax(employee, cur_year)
	
	ptkp = emp.ptkp

	# paid_extra = 0
	# paid_extra_tax = 0

	# if emp.salary_slip_log:
	# 	for log in emp.salary_slip_log:
	# 		if cur_year == log.year:
	# 			if log.payroll_frequency == "Monthly":
	# 				paid_thp += log.thp
	# 				paid_tax += log.paid_tax
	# 			else:
	# 				paid_extra += log.thp
	# 				paid_extra_tax += log.paid_tax

	# total_thp = 0
	total_thp = paid_thp + (float(thp) * sisa_bulan)

	pkp = total_thp - ptkp
	pph21 = 0

	if pkp < 0:
		# tidak bayar pajak
		pph21 = 0
	else:

		tax_pkp = [50000000,250000000,500000000]

		total_pph = 0

		if pkp <= tax_pkp[0]:
			total_pph = pkp * 5/100;
		elif pkp > tax_pkp[0] and pkp <= tax_pkp[1]:
			total_pph = (tax_pkp[0] * 5/100) + ((pkp - tax_pkp[0]) * 15/100)
		elif pkp > tax_pkp[1] and pkp <= tax_pkp[2]:
			total_pph = (tax_pkp[0] * 5/100) + (tax_pkp[1] * 15/100) + ((pkp - tax_pkp[1] - tax_pkp[0]) * 25/100)
		else:
			total_pph = (tax_pkp[0] * 5/100) + (tax_pkp[1] * 15/100) + (tax_pkp[2] * 25/100) + ((pkp - tax_pkp[2] - tax_pkp[1] - tax_pkp[0]) * 30/100)
		
		if doc.payroll_frequency == "Monthly":
			pph21 = (total_pph - paid_tax)/sisa_bulan
		else:
			pph21 = total_pph

	return float(pph21)

def calculate_pph(doc, method):
	
	frappe.msgprint(doc.name)
	pph21 = 0
	thp = 0

	doc.reload()

	for income in doc.earnings:
		if income.is_tax_applicable:
			thp += income.amount

	if doc.payroll_frequency == "Monthly":
		pph21 = get_pph(doc.employee, thp, doc)
	else:
		# for komisi, thr, bonus, etc ; get latest thp
		# cur_month = datetime.datetime.now().month - 1
		# sisa_bulan = 12 - cur_month

		normal_pph = get_pph(doc.employee, thp, doc)

		onetime_pph21 = get_pph(doc.employee, thp, doc)
		
		pph21 = onetime_pph21 - normal_pph

	is_pph_exist = False
	for deduct in doc.deductions:
		if deduct.salary_component == "Income Tax":
			deduct.amount = pph21
			is_pph_exist = True

	if not is_pph_exist:
		row = doc.append("deductions",{})
		row.salary_component = "Income Tax"
		row.amount = pph21

	doc.save()
	doc.reload()

def update_salary_slip_log(doc,method):

	if doc.payroll_entry:
		doc.is_regular = 1

	cur_year = datetime.datetime.now().year
	cur_month = datetime.datetime.strptime((doc.posting_date), "%Y-%m-%d").month - 1
	months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

	thp = 0

	for income in doc.earnings:
		if income.is_tax_applicable:
			thp += income.amount

	pph21 = 0
	for deduct in doc.deductions:
		if deduct.salary_component == "Income Tax":
			pph21 = deduct.amount

	emp = frappe.get_doc("Employee", doc.employee)

	# check if log already created
	logs = frappe.db.sql(""" 
		SELECT * FROM `tabSalary Slip Log` 
		where year = "{}"
		and month = "{}"
		and parent = "{}"
		and payroll_frequency = "{}
		""".format(cur_year, months[cur_month], doc.employee, doc.payroll_frequency))

	if not logs:
		row = emp.append("salary_slip_log",{})
		row.year = cur_year
		row.month = months[cur_month]
		row.thp_amount = thp
		row.payroll_frequency = doc.payroll_frequency
		row.paid_tax = pph21
		row.salary_slip = doc.name

		emp.save()


def delete_salary_slip_log(doc,method):
	result = frappe.db.sql("""SELECT * from `tabSalary Slip Log` where salary_slip = "{}"  """.format(doc.name))
	if result:
		frappe.db.sql(""" delete from `tabSalary Slip Log` where salary_slip = "{}"  """.format(doc.name))