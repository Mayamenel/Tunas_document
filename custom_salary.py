from __future__ import unicode_literals
import frappe
import datetime
import locale
import json

from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, getdate

# hitung thp berdasarkan salary slip log
# kembaliin pajak yg lebih bayar ketika gaji berkurang

# check paid ptkp


@frappe.whitelist()
def get_pph(employee, thp_amount, doc, is_one_time=0):
	
	thp = 0
	cur_year = datetime.datetime.now().year
	cur_month = datetime.datetime.now().month - 1
	sisa_bulan = 12 - cur_month

	thp = thp_amount	
	emp = frappe.get_doc("Employee", employee)
	
	paid_thp = 0
	paid_tax = 0

	ptkp = (float(emp.ptkp)/12) * sisa_bulan

	paid_extra = 0
	paid_extra_tax = 0

	if emp.salary_slip_log:
		for log in emp.salary_slip_log:
			if cur_year == log.year:
				if log.is_regular:
					paid_thp += log.thp_amount
					paid_tax += log.paid_tax
					ptkp = log.paid_ptkp + ptkp
				else:
					paid_extra += log.thp_amount
					paid_extra_tax += log.paid_tax

	total_thp = 0
	if is_one_time > 0:
		total_thp = paid_thp + (float(thp) * sisa_bulan) + float(is_one_time) + float(paid_extra)
	else:
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
			total_pph = (tax_pkp[0] * 5/100) + (tax_pkp[1] * 15/100) + ((pkp - tax_pkp[1]) * 25/100)
		else:
			total_pph = (tax_pkp[0] * 5/100) + (tax_pkp[1] * 15/100) + (tax_pkp[2] * 25/100) + ((pkp - tax_pkp[2]) * 30/100)
		
		if is_one_time > 0:
			pph21 = total_pph
		else:
			pph21 = (total_pph - paid_tax)/sisa_bulan

	return float(pph21)

def calculate_pph(doc, method):
	
	pph21 = 0
	thp = 0

	doc.reload()

	for income in doc.earnings:
		if income.is_tax_applicable:
			thp += income.amount

	if doc.payroll_entry:
		pph21 = get_pph(doc.employee, thp, doc)
	else:
		# for komisi, thr, bonus, etc ; get latest thp
		cur_month = datetime.datetime.now().month - 1
		sisa_bulan = 12 - cur_month
		
		latest_thp = get_latest_thp(doc.employee)

		normal_pph = get_pph(doc.employee, latest_thp, doc) * sisa_bulan
		onetime_pph21 = get_pph(doc.employee, latest_thp, doc, thp)
		
		pph21 = onetime_pph21 - normal_pph

	is_pph_exist = False
	for deduct in doc.deductions:
		if deduct.salary_component == "PPH21":
			deduct.amount = pph21
			is_pph_exist = True

	if not is_pph_exist:
		row = doc.append("deductions",{})
		row.salary_component = "PPH21"
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
		if deduct.salary_component == "PPH21":
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


@frappe.whitelist()
def get_latest_thp(employee):
	latest_thp = 0
	logs = frappe.db.sql(""" 
		select * from `tabSalary Slip Log` WHERE parent = "{}" ORDER BY modified DESC LIMIT 1;
		""".format(employee), as_dict= 1)
	
	if logs:
		latest_thp = logs[0].thp_amount
	else:
		base = frappe.db.sql("""
			select * from `tabSalary Structure Assignment` where employee = '{}';
			""".format(employee), as_dict=1)
		if base:
			latest_thp = base[0].base
		else:
			frappe.throw("No Salary Structure Assignment on this employee.")
	return latest_thp