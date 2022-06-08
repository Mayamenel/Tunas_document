# -*- coding: utf-8 -*-
# Copyright (c) 2019, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CostCalculation(Document):
	pass


	# first_invoice = frappe.db.sql(""" 
	# 		SELECT
	# 		sinv.`name`
	# 		FROM `tabSales Invoice` sinv
	# 		WHERE sinv.`docstatus` = "1"
	# 		{}
	# 		ORDER BY sinv.`name` ASC
	# 		LIMIT 1
							
	# 	""".format(temp_statement), as_list=1)

	# self.section_1_gross_profit = []
	# pp_so = self.append('section_1_gross_profit', {})
	# pp_so.keterangan = "Total Selling"
	# pp_so.value = total_selling
	# pp_so.plus_minus = "Plus"


	def generate_data(self):
		self.cek_customer_territory()
		self.show_field = 1

		# ====================== generate zona 1 ======================
		self.cost_cal_zona_1 = []

		zona1 = self.append('cost_cal_zona_1', {})
		zona1.biaya = "Gaji Pokok"
		data_date = str(self.date).split("-")[0]
		data_ump = frappe.db.sql(""" 
			SELECT ur.`name`, ur.`ump_rp` FROM `tabUMP Regional` ur
			WHERE ur.`fiscal_year` = "{}"
			AND ur.`territory` = "{}"
			ORDER BY ur.`creation` DESC
			LIMIT 1		
		""".format(data_date, self.territory), as_list=1)
		if data_ump :
			zona1.kelas_a = data_ump[0][1]
			zona1.kelas_b = data_ump[0][1]
		else :
			zona1.kelas_a = 0
			zona1.kelas_b = 0

		zona1 = self.append('cost_cal_zona_1', {})
		zona1.biaya = "Tunjangan Meal"
		zona1.kelas_a = 0
		zona1.kelas_b = 0

		zona1 = self.append('cost_cal_zona_1', {})
		zona1.biaya = "Tunjangan Transport"
		zona1.kelas_a = 0
		zona1.kelas_b = 0

		zona1 = self.append('cost_cal_zona_1', {})
		zona1.biaya = "Tunjangan Skill"
		zona1.kelas_a = 0
		zona1.kelas_b = 0

		zona1 = self.append('cost_cal_zona_1', {})
		zona1.biaya = "Tunjangan"
		zona1.kelas_a = 0
		zona1.kelas_b = 0

		# ====================== generate zona 2 ======================
		self.cost_cal_zona_2 = []

		zona2 = self.append('cost_cal_zona_2', {})
		zona2.biaya = "Bpjs Kesehatan"
		zona2.persen = 0
		zona2.dari_biaya = "Gaji Pokok"
		zona2.kelas_a = 0
		zona2.kelas_b = 0

		zona2 = self.append('cost_cal_zona_2', {})
		zona2.biaya = "Bpjs Ketenagakerjaan - Jaminan Kecelakaan kerja"
		zona2.persen = 0
		zona2.dari_biaya = "Gaji Pokok"
		zona2.kelas_a = 0
		zona2.kelas_b = 0

		zona2 = self.append('cost_cal_zona_2', {})
		zona2.biaya = "Bpjs Ketenagakerjaan - Jaminan Kematian"
		zona2.persen = 0
		zona2.dari_biaya = "Gaji Pokok"
		zona2.kelas_a = 0
		zona2.kelas_b = 0

		zona2 = self.append('cost_cal_zona_2', {})
		zona2.biaya = "Bpjs Ketenagakerjaan - Jaminan Hari Tua"
		zona2.persen = 0
		zona2.dari_biaya = "Gaji Pokok"
		zona2.kelas_a = 0
		zona2.kelas_b = 0

		zona2 = self.append('cost_cal_zona_2', {})
		zona2.biaya = "Bpjs Ketenagakerjaan - Jaminan Pensiun"
		zona2.persen = 0
		zona2.dari_biaya = "Gaji Pokok"
		zona2.kelas_a = 0
		zona2.kelas_b = 0

		zona2 = self.append('cost_cal_zona_2', {})
		zona2.biaya = "Seragam"
		zona2.persen = 0
		zona2.dari_biaya = ""
		zona2.kelas_a = 0
		zona2.kelas_b = 0

		zona2 = self.append('cost_cal_zona_2', {})
		zona2.biaya = "Training"
		zona2.persen = 0
		zona2.dari_biaya = ""
		zona2.kelas_a = 0
		zona2.kelas_b = 0

		# ====================== generate zona 3 ======================

		self.jasa_pengelolaan = 0
		self.akun_pengelolaan = "4320.000 - Pendapatan Pengelolaan - T"
		self.ppn = 10
		self.akun_ppn = "1150.001 - PPN Masukan - T"

		# frappe.throw(data_date)



	def validate(self):
		self.cek_customer_territory()
		self.hitung_amount_cost_cal()


	def cek_customer_territory(self) :
		if not self.customer :
			frappe.throw("Please input Customer")

		if not self.territory :
			frappe.throw("Please input Territory")


	def hitung_amount_cost_cal(self) :
		data_zona_1_a = {}
		data_zona_1_b = {}

		if self.cost_cal_zona_1 :

			total_a = 0
			total_b = 0

			self.total_amount_zona_1_a = 0
			self.total_amount_zona_1_b = 0

			for i in self.cost_cal_zona_1 :
				if i.kelas_a :
					total_a += i.kelas_a

				if i.kelas_b :
					total_b += i.kelas_b

				data_zona_1_a.update({i.biaya : i.kelas_a})
				data_zona_1_b.update({i.biaya : i.kelas_b})


			self.total_amount_zona_1_a = total_a
			self.total_amount_zona_1_b = total_b


		if self.cost_cal_zona_2 :


			total_a = 0
			total_b = 0

			for i in self.cost_cal_zona_2 :
				if i.persen and i.dari_biaya :
					if data_zona_1_a[i.dari_biaya] :
						i.kelas_a = float(i.persen) * float(data_zona_1_a[i.dari_biaya]) / 100
					else :
						i.kelas_a = float(i.persen) * 0

					if data_zona_1_b[i.dari_biaya] :
						i.kelas_b = float(i.persen) * float(data_zona_1_b[i.dari_biaya]) / 100
					else :
						i.kelas_b = float(i.persen) * 0

					total_a += i.kelas_a
					total_b += i.kelas_b

				else :
					if i.kelas_a :
						total_a += i.kelas_a

					if i.kelas_b :
						total_b += i.kelas_b

			self.total_amount_zona_2_a = total_a
			self.total_amount_zona_2_b = total_b


		# zona 3

		self.total_dpp_hpp_a = self.total_amount_zona_1_a + self.total_amount_zona_2_a
		self.total_dpp_hpp_b = self.total_amount_zona_1_b + self.total_amount_zona_2_b

		if self.jasa_pengelolaan :
			self.total_jasa_pengelolaan_a = self.jasa_pengelolaan * self.total_dpp_hpp_a / 100
			self.total_jasa_pengelolaan_b = self.jasa_pengelolaan * self.total_dpp_hpp_b / 100

		self.total_dpp_a = self.total_dpp_hpp_a + self.total_jasa_pengelolaan_a
		self.total_dpp_b = self.total_dpp_hpp_b + self.total_jasa_pengelolaan_b

		if self.ppn :
			self.total_ppn_a = self.ppn * self.total_dpp_a / 100
			self.total_ppn_b = self.ppn * self.total_dpp_b / 100

		self.total_harga_pengemudi_a = self.total_dpp_a + self.total_ppn_a
		self.total_harga_pengemudi_b= self.total_dpp_b + self.total_ppn_b


		# if self.cost_cal_zona_4 :

		# 	total_a = 0
		# 	total_b = 0

		# 	self.total_amount_zona_4_a = 0
		# 	self.total_amount_zona_4_b = 0

		# 	for i in self.cost_cal_zona_1 :
		# 		if i.kelas_a :
		# 			total_a += i.kelas_a

		# 		if i.kelas_b :
		# 			total_b += i.kelas_b

		# 	self.total_amount_zona_4_a = total_a
		# 	self.total_amount_zona_4_b = total_b


		# if self.cost_cal_zona_5 :
		# 	total_a = 0
		# 	total_b = 0

		# 	self.total_amount_zona_5_a = 0
		# 	self.total_amount_zona_5_b = 0

		# 	for i in self.cost_cal_zona_1 :
		# 		if i.kelas_a :
		# 			total_a += i.kelas_a

		# 		if i.kelas_b :
		# 			total_b += i.kelas_b

		# 	self.total_amount_zona_5_a = total_a
		# 	self.total_amount_zona_5_b = total_b


		# self.total_amount_a = self.total_harga_pengemudi_a + self.total_amount_zona_4_a + self.total_amount_zona_5_a
		# self.total_amount_b = self.total_harga_pengemudi_b + self.total_amount_zona_4_b + self.total_amount_zona_5_b



