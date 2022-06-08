# -*- coding: utf-8 -*-
# Copyright (c) 2015, erpx and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document



class CustomMethodTunas(Document):
	pass




@frappe.whitelist()
def create_quotation_kelas_a(name):

	# return name

	cost_cal_name = name
	dcc = frappe.get_doc("Cost Calculation", cost_cal_name)

	# create new quotation
	new_qtn = frappe.new_doc("Quotation")
	new_qtn.cost_calculation = cost_cal_name
	new_qtn.kelas = "Kelas A"
	new_qtn.naming_series = "QTN-"
	new_qtn.quotation_to = "Customer"
	new_qtn.order_type = "Sales"
	new_qtn.transaction_date = dcc.date
	new_qtn.customer = dcc.customer

	new_qtn.show_button = 1

	new_qtn.items = []
	new_qtn.taxes = []

	# zona 1
	if dcc.cost_cal_zona_1 :
		for i in dcc.cost_cal_zona_1 :

			zona1 = new_qtn.append('items', {})
			zona1.item_code = i.biaya
			zona1.item_name = i.biaya
			zona1.description = i.biaya
			zona1.qty = 1
			zona1.rate = i.kelas_a

	# zona 2
	if dcc.cost_cal_zona_2 :
		for i in dcc.cost_cal_zona_2 :

			zona2 = new_qtn.append('items', {})
			zona2.item_code = i.biaya
			zona2.item_name = i.biaya
			zona2.description = i.biaya
			zona2.qty = 1
			zona2.rate = i.kelas_a

	# zona 3 - masuk ke taxes and charges
	if dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
		zona3 = new_qtn.append('taxes', {})
		zona3.charge_type = "On Net Total"
		zona3.account_head = dcc.akun_pengelolaan
		zona3.cost_center = "Main - T"
		zona3.description = "Jasa Pengelolaan"
		zona3.rate = dcc.jasa_pengelolaan

		if dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
			zona3 = new_qtn.append('taxes', {})
			zona3.charge_type = "On Previous Row Total"
			zona3.row_id = 1
			zona3.account_head = dcc.akun_ppn
			zona3.cost_center = "Main - T"
			zona3.description = "PPN"
			zona3.rate = dcc.ppn

	elif dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
			zona3 = new_qtn.append('taxes', {})
			zona3.charge_type = "On Net Total"
			zona3.account_head = dcc.akun_ppn
			zona3.cost_center = "Main - T"
			zona3.description = "PPN"
			zona3.rate = dcc.ppn


	new_qtn.flags.ignore_permissions = True
	new_qtn.save()

	respon = "Quotation "+str(new_qtn.name)+" untuk kelas A telah terbuat"

	return respon

@frappe.whitelist()
def create_quotation_kelas_b(name):

	# return name

	cost_cal_name = name
	dcc = frappe.get_doc("Cost Calculation", cost_cal_name)

	# create new quotation
	new_qtn = frappe.new_doc("Quotation")
	new_qtn.cost_calculation = cost_cal_name
	new_qtn.kelas = "Kelas B"
	new_qtn.naming_series = "QTN-"
	new_qtn.quotation_to = "Customer"
	new_qtn.order_type = "Sales"
	new_qtn.transaction_date = dcc.date
	new_qtn.customer = dcc.customer

	new_qtn.show_button = 1

	new_qtn.items = []
	new_qtn.taxes = []

	# zona 1
	if dcc.cost_cal_zona_1 :
		for i in dcc.cost_cal_zona_1 :

			zona1 = new_qtn.append('items', {})
			zona1.item_code = i.biaya
			zona1.item_name = i.biaya
			zona1.description = i.biaya
			zona1.qty = 1
			zona1.rate = i.kelas_b

	# zona 2
	if dcc.cost_cal_zona_2 :
		for i in dcc.cost_cal_zona_2 :

			zona2 = new_qtn.append('items', {})
			zona2.item_code = i.biaya
			zona2.item_name = i.biaya
			zona2.description = i.biaya
			zona2.qty = 1
			zona2.rate = i.kelas_b

	# zona 3 - masuk ke taxes and charges
	if dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
		zona3 = new_qtn.append('taxes', {})
		zona3.charge_type = "On Net Total"
		zona3.account_head = dcc.akun_pengelolaan
		zona3.cost_center = "Main - T"
		zona3.description = "Jasa Pengelolaan"
		zona3.rate = dcc.jasa_pengelolaan

		if dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
			zona3 = new_qtn.append('taxes', {})
			zona3.charge_type = "On Previous Row Total"
			zona3.row_id = 1
			zona3.account_head = dcc.akun_ppn
			zona3.cost_center = "Main - T"
			zona3.description = "PPN"
			zona3.rate = dcc.ppn

	elif dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
			zona3 = new_qtn.append('taxes', {})
			zona3.charge_type = "On Net Total"
			zona3.account_head = dcc.akun_ppn
			zona3.cost_center = "Main - T"
			zona3.description = "PPN"
			zona3.rate = dcc.ppn


	new_qtn.flags.ignore_permissions = True
	new_qtn.save()

	respon = "Quotation "+str(new_qtn.name)+" untuk kelas B telah terbuat"

	return respon



@frappe.whitelist()
def create_quotation_kelas_a_b(name):

	# return name

	cost_cal_name = name
	dcc = frappe.get_doc("Cost Calculation", cost_cal_name)


	# create new quotation kelas A ==========================
	new_qtn_a = frappe.new_doc("Quotation")
	new_qtn_a.cost_calculation = cost_cal_name
	new_qtn_a.kelas = "Kelas A"
	new_qtn_a.naming_series = "QTN-"
	new_qtn_a.quotation_to = "Customer"
	new_qtn_a.order_type = "Sales"
	new_qtn_a.transaction_date = dcc.date
	new_qtn_a.customer = dcc.customer

	new_qtn_a.show_button = 1

	new_qtn_a.items = []
	new_qtn_a.taxes = []

	# zona 1
	if dcc.cost_cal_zona_1 :
		for i in dcc.cost_cal_zona_1 :

			zona1 = new_qtn_a.append('items', {})
			zona1.item_code = i.biaya
			zona1.item_name = i.biaya
			zona1.description = i.biaya
			zona1.qty = 1
			zona1.rate = i.kelas_a

	# zona 2
	if dcc.cost_cal_zona_2 :
		for i in dcc.cost_cal_zona_2 :

			zona2 = new_qtn_a.append('items', {})
			zona2.item_code = i.biaya
			zona2.item_name = i.biaya
			zona2.description = i.biaya
			zona2.qty = 1
			zona2.rate = i.kelas_a

	# zona 3 - masuk ke taxes and charges
	if dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
		zona3 = new_qtn_a.append('taxes', {})
		zona3.charge_type = "On Net Total"
		zona3.account_head = dcc.akun_pengelolaan
		zona3.cost_center = "Main - T"
		zona3.description = "Jasa Pengelolaan"
		zona3.rate = dcc.jasa_pengelolaan

		if dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
			zona3 = new_qtn_a.append('taxes', {})
			zona3.charge_type = "On Previous Row Total"
			zona3.row_id = 1
			zona3.account_head = dcc.akun_ppn
			zona3.cost_center = "Main - T"
			zona3.description = "PPN"
			zona3.rate = dcc.ppn

	elif dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
			zona3 = new_qtn_a.append('taxes', {})
			zona3.charge_type = "On Net Total"
			zona3.account_head = dcc.akun_ppn
			zona3.cost_center = "Main - T"
			zona3.description = "PPN"
			zona3.rate = dcc.ppn


	new_qtn_a.flags.ignore_permissions = True
	new_qtn_a.save()


	# create new quotation kelas B =========================
	new_qtn_b = frappe.new_doc("Quotation")
	new_qtn_b.cost_calculation = cost_cal_name
	new_qtn_b.kelas = "Kelas B"
	new_qtn_b.naming_series = "QTN-"
	new_qtn_b.quotation_to = "Customer"
	new_qtn_b.order_type = "Sales"
	new_qtn_b.transaction_date = dcc.date
	new_qtn_b.customer = dcc.customer

	new_qtn_b.show_button = 1

	new_qtn_b.items = []
	new_qtn_b.taxes = []

	# zona 1
	if dcc.cost_cal_zona_1 :
		for i in dcc.cost_cal_zona_1 :

			zona1 = new_qtn_b.append('items', {})
			zona1.item_code = i.biaya
			zona1.item_name = i.biaya
			zona1.description = i.biaya
			zona1.qty = 1
			zona1.rate = i.kelas_b

	# zona 2
	if dcc.cost_cal_zona_2 :
		for i in dcc.cost_cal_zona_2 :

			zona2 = new_qtn_b.append('items', {})
			zona2.item_code = i.biaya
			zona2.item_name = i.biaya
			zona2.description = i.biaya
			zona2.qty = 1
			zona2.rate = i.kelas_b

	# zona 3 - masuk ke taxes and charges
	if dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
		zona3 = new_qtn_b.append('taxes', {})
		zona3.charge_type = "On Net Total"
		zona3.account_head = dcc.akun_pengelolaan
		zona3.cost_center = "Main - T"
		zona3.description = "Jasa Pengelolaan"
		zona3.rate = dcc.jasa_pengelolaan

		if dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
			zona3 = new_qtn_b.append('taxes', {})
			zona3.charge_type = "On Previous Row Total"
			zona3.row_id = 1
			zona3.account_head = dcc.akun_ppn
			zona3.cost_center = "Main - T"
			zona3.description = "PPN"
			zona3.rate = dcc.ppn

	elif dcc.akun_pengelolaan and dcc.jasa_pengelolaan :
			zona3 = new_qtn_b.append('taxes', {})
			zona3.charge_type = "On Net Total"
			zona3.account_head = dcc.akun_ppn
			zona3.cost_center = "Main - T"
			zona3.description = "PPN"
			zona3.rate = dcc.ppn


	new_qtn_b.flags.ignore_permissions = True
	new_qtn_b.save()

	respon = "Quotation "+str(new_qtn_a.name)+" untuk kelas A dan "+str(new_qtn_b.name)+" untuk kelas B telah terbuat"

	return respon