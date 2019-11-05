import os
import time

class ProductModel:

	def __init__(self, raw_supplier, product, raw_material,
			time_supplied, refurbishment_meth, 
			redesign_method, inventory, storage_center,
			distribution_center, disassembly_center, 
			manufacture_method, severity,market_price,
			assembly_cost, shipping_storage_cost,
			transp_storage_cost,distance_storage,
			shipping_distribution_cost, transp_distribution_cost,
			distance_distribution, hours_raw, labor_cost,
			manufacture_raw_cost, variable_raw_cost,
			raw_capacity, manufacture_raw_cost, number_raw,
			order_raw_cost, market_price_refurb,
			variable_refurbished_cost, shipping_disassembly_cost,
			transp_disassembly_cost, distance_disassembly,
			defective_percentage, hours_refurbished,
			manufacture_refurbished_cost, refurbish_method_capacity,
			order_refurbish_cost, market_price_redesign,
			hours_redesigned,redesign_method_capacity, order_redesign_cost,
			penalty_excess, initial_inventory, demand,
			final_inventory, inventory_cost, pollution_shipping_dissasembly,
			pollution_manufacturing, pollution_shipping_storage,
			pollution_refuribshed, pollution_dissasembly, pollution_shipping_distribution,
			severity_function_new, severity_function_refurbished, severity_function_redesign,
			capacity_storage, capacity_distribution, capacity_disassembly, 
			returning_goal, uncertain_demand, up_bound, bound):
		self.raw_supplier = raw_supplier
		self.time_supplied = time_supplied
		self.redesign_method = redesign_method
		self.distribution_center = distribution_center
		self.manufacture_method = manufacture_method
		self.assembly_cost = assembly_cost
		self.transp_storage_cost = transp_storage_cost
		self.shipping_distribution_cost = shipping_distribution_cost
		self.distance_distribution = distance_distribution
		self.manufacture_raw_cost = manufacture_raw_cost
		self.raw_capacity = raw_capacity
		self.order_raw_cost = order_raw_cost
		self.variable_refurbished_cost = variable_refurbished_cost
		self.transp_disassembly_cost = transp_disassembly_cost
		self.defective_percentage = defective_percentage
		self.manufacture_refurbished_cost = manufacture_refurbished_cost
		self.order_refurbish_cost = order_refurbish_cost
		self.hours_redesigned = hours_redesigned
		self.redesign_method_capacity = redesign_method_capacity
		self.penalty_excess = penalty_excess
		self.final_inventory = final_inventory
		self.pollution_manufacturing = pollution_manufacturing
		self.pollution_refuribshed = pollution_refuribshed
		self.severity_function_new = severity_function_new
		self.capacity_storage = capacity_storage
		self.returning_goal = returning_goal
		self.product = product
		self.refurbishment_meth = refurbishment_meth
		self.inventory = inventory
		self.disassembly_center = disassembly_center
		self.severity = severity
		self.shipping_storage_cost = shipping_storage_cost
		self.distance_storage = distance_storage
		self.transp_distribution_cost = transp_distribution_cost
		self.hours_raw = hours_raw
		self.variable_raw_cost = variable_raw_cost
		self.market_price_refurb = market_price_refurb
		self.shipping_disassembly_cost = shipping_disassembly_cost
		self.distance_disassembly = distance_disassembly
		self.hours_refurbished = hours_refurbished
		self.refurbish_method_capacity = refurbish_method_capacity
		self.market_price_redesign = market_price_redesign
		self.order_redesign_cost = order_redesign_cost
		self.initial_inventory = initial_inventory
		self.inventory_cost = inventory_cost
		self.pollution_shipping_storage = pollution_shipping_storage
		self.pollution_dissasembly = pollution_dissasembly
		self.severity_function_refurbished = severity_function_refurbished
		self.capacity_distribution = capacity_distribution
		self.uncertain_demand = uncertain_demand
		self.raw_material = raw_material
		self.storage_center = storage_center
		self.market_price = market_price
		self.labor_cost = labor_cost
		self.number_raw = number_raw
		self.demand = demand
		self.pollution_shipping_dissasembly = pollution_shipping_dissasembly
		self.pollution_shipping_distribution = pollution_shipping_distribution
		self.severity_function_redesign = severity_function_redesign
		self.capacity_disassembly = capacity_disassembly
		self.up_bound = up_bound
		self.bound = bound


class DescisionVariables:

	def __init__(self, supplier_selected, interval_selected,
				 refurbishment_selected, redesign_selected,
				 portion_raw, portion_refurb, portion_redesign,
				 manufacture_selected, storage_selected, distribution_selected,
				 disassembly_selected):
		self.supplier_selected = supplier_selected
		self.interval_selected = interval_selected
		self.refurbishment_selected = refurbishment_selected
		self.redesign_selected = redesign_selected
		self.portion_raw = portion_raw
		self.portion_refurb = portion_refurb
		self.portion_redesign = portion_redesign
		self.manufacture_selected = manufacture_selected
		self.storage_selected = storage_selected
		self.distribution_selected = distribution_selected
		self.disassembly_selected = disassembly_selected


def get_sum_of_storage_centers(models):
	sum_of_storage_centers = 0
	for y in models:
		sum_of_storage_centers = sum_of_storage_centers + \
								 ((y.shipping_storage_cost +
								   y.transp_storage_cost * y.distance_storage)
								  * descison_variables.storage_selected)
	return sum_of_storage_centers


def get_sum_of_distribution_centers(models):
	sum_of_distribution_centers = 0
	for y in models:
		sum_of_distribution_centers = sum_of_distribution_centers + \
									  ((y.shipping_distribution_cost +
										y.transp_distribution_cost
										* y.distance_distribution)
									   * descison_variables.
									   distribution_selected)
	return sum_of_distribution_centers


def get_sum_of_manufacture_method(models):
	sum_of_manufacture_method = 0
	for y in models:
		sum_of_manufacture_method = sum_of_manufacture_method + \
									(y.hours_raw * y.labor_cost *
									 descison_variables.manufacture_selected)
	return sum_of_manufacture_method

if __name__=='__main__':
	models = [ProductModel(), ProductModel(), ProductModel()]
	descison_variables = DescisionVariables()

	sum_of_product = 0
	for i in models:
		sum_of_manufacture_method = 0
		sum_of_storage_centers = get_sum_of_storage_centers(models)
		sum_of_distribution_centers = get_sum_of_distribution_centers(models)
		sum_of_manufacture_method = get_sum_of_manufacture_method(models)

		sum_of_product = sum_of_product + ( i.market_price - i.assembly_cost - \
			sum_of_storage_centers - sum_of_distribution_centers - \
			sum_of_manufacture_method -i.manufacture_raw_cost - \
			i.variable_raw_cost )



